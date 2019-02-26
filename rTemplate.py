import sys
import re
import binascii
#
class sta (dict):
    def __init__(self, initial_sta=None):

        if initial_sta is None:
            self.initial_sta = {}
        else:
            self.initial_sta=initial_sta

        super(sta,self).__init__(initial_sta)

    def __getitem__(self, key):
        try:

            val = dict.__getitem__(self, key)
        except KeyError as e:
            # Whenever you get a key error, that means the
            # substitution name is not defined. Therefore,
            # define it as itself. Using the ${form} because
            # reconstructing the original form isn't worth it
            # and using the more verbose form works no matter
            # how it was used in the original text

            key = e.args[0]
            val = "${%s}" % key
            self.__setitem__(key, val)
            # print "matched --", matched

        return val

class rTemplate(object):

    def __init__ (self, template='', indent=0, identifiers=None):
        #super(rTemplate,self).__init__("")

        self.identifiers = sta(identifiers)
        self.template_name = None
        self.template = template
        self.indent = indent

        # internal function: perform substitution substitute can
        # either perform identifier replacement or can also perform
        # escape handling.  do not use escape handling if the output
        # will be passed into another template.

    def substitute(self, indent = 0):
        """ public interface for substitute
        """
        result = self.__substitute(self.template, indent)
        return result

    def __substitute(self, given_body, indent):

        # perform substitution substitute can either perform
        # identifier replacement or can also perform escape handling.
        # do not use escape handling if the output will be passed into
        # another template.
        # out_list is a list of post pocessed template segments.
        out_list = [" "*indent,]

        # tokenise text.
        y = re.split(r"(\n|\$\$|\$[a-zA-Z0-9_]+|\$\{[a-zA-Z0-9_]+\})", given_body)
        #print(y)
        # iterate over tokens
        for i in y:
            #print ("i == %s, %s", (len(i), i))
            # look for Identifiers
            matchit = re.match(r'\$([a-zA-Z0-9_]+)|\$\{([a-zA-Z0-9_]+)\}', i)
            if matchit is not None:
                #It looks like we found something of either $form or ${form}
                found_identifier = matchit.group(1) or matchit.group(2)

                # See if we found the identifier before. If yes, see
                #if it needs expansion recursively or, if not, define
                #it using the ${form}

                matched = self.identifiers[found_identifier]
                #print(found_identifier, matched)
                # recursion test
                if '${'+found_identifier+'}' != matched:
                    # invoke recursion
                    if '$' in matched:
                        # print ("matched >> %s" % matched)
                        matched = self.__substitute(matched, indent)

            elif '\n' == i:
                # add indentation
                # print '|', (1,i),
                matched = i +" "*indent
                # print '^', (2,matched), '|'

            else:
                matched = i

                # At the end of this chain, matched contains the
                # fragment of the original template that has been
                # processed through template handling. Add it to the
                # end of the list

            #print "appended", matched
            out_list.append(matched)

        # Slam them altogether
        try:
            out_join = ''.join(out_list)
        except:
            print(str(out_list))

        return out_join

    def last_pass_cleanup(self,body):
        #print("==++==",body,"==++==")
        return body.replace('$$','$')


# The goal of this module is to read a file and create a dictionary. The format
# of the file is:
#:name
#<data lines>
#:name
#
# The name is the dictionary key, The data lines are the values for that
# dictionary key. The data ends at the starting with a colon or end of
# file. The block ends on the next colon name.  special case when
# the opening and closing colon name are the same. all text between
# the closing colon name and the next colon name is ignored.second
# special case is all text between the start of the file and the
# first :name is also ignored.
# remember, no protection against duplicate names or any line starting
# with colon. maybe someday I'll put in an escape character.
#


def colon_parser(filename, starter_dict=None, EOL=True):
    key = "0000"
    if starter_dict:
        returning=starter_dict.copy()
    else:
        returning={}
    line_list=[]
    last_key=None
    block_line_collection=True

    with open (filename) as fp:
        for line in fp:
            result = re.match("^:(.*)$", line)
            #print (line, result)
            #print (line, binascii.b2a_hex(line))
            # start line capture on first :name, stop on second or another :name
            # if closing :name, eat lines till next new :name
            if result:
                # strip off any trailing EOL is told to
                if not EOL and last_key in returning:
                    returning[last_key] = returning[last_key].rstrip()

                key=result.group(1)
                # are we in the same name block
                if key == last_key:
                    # in same name block so block collection
                    block_line_collection=True
                    #strip of eol at start
                else:
                    # new key
                    returning[key]=""
                    last_key=key
                    block_line_collection=False

            else:
                if not block_line_collection:
                    returning[key] = returning[key] + line

                # otherwise eat lines till next :name

    return returning
