from proto_formatter.comment import CommentParser
from proto_formatter.proto import Message
from proto_formatter.proto import MessageElement
from proto_formatter.object_parser import ObjectParser
from proto_formatter.proto import ProtoBufStructure
from proto_formatter.proto import Syntax


class MessageParser(ObjectParser):

    def __init__(self):
        obj = Message(name='name', elements=[], comments=[])
        super(MessageParser, self).__init__(obj=obj)

    def parse_obj_field(self, line, top_comments=[]):
        line = line.strip()
        equal_sign_index = line.index(self.EQUAL_SIGN)
        semicolon_index = line.index(self.SEMICOLON)
        str_before_equqal_sign = line[:equal_sign_index]
        parts = str_before_equqal_sign.split(' ')
        parts = list(filter(None, parts))
        value = line[equal_sign_index + 1:semicolon_index].strip().replace('"', "").replace("'", "")
        comments = CommentParser.create_comment(line, top_comments)
        if len(parts) == 2:
            return MessageElement(label=None, type=parts[0], name=parts[1], number=value, comments=comments)
        if len(parts) == 3:
            return MessageElement(label=parts[0], type=parts[1], name=parts[2], number=value, comments=comments)

        return None
