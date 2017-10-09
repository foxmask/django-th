# coding: utf-8
import re
import html.entities as htmlentities


class HtmlEntities:

    def __init__(self, my_string):
        self.my_string = my_string

    def html_entity_decode_char(self, m, defs=htmlentities.entitydefs):
        """
            decode html entity into one of the html char
        """
        try:
            char = defs[m.group(1)]
            return "&{char};".format(char=char)
        except ValueError:
            return m.group(0)
        except KeyError:
            return m.group(0)

    def html_entity_decode_codepoint(self, m,
                                     defs=htmlentities.codepoint2name):
        """
            decode html entity into one of the codepoint2name
        """
        try:
            char = defs[m.group(1)]
            return "&{char};".format(char=char)
        except ValueError:
            return m.group(0)
        except KeyError:
            return m.group(0)

    @property
    def html_entity_decode(self):
        """
            entry point of this set of tools
            to decode html entities
        """
        pattern = re.compile(r"&#(\w+?);")
        string = pattern.sub(self.html_entity_decode_char, self.my_string)
        return pattern.sub(self.html_entity_decode_codepoint, string)
