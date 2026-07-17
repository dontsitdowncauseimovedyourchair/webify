from enum import Enum

class TextType(Enum):
    text = "text"
    bold = "**Bold text**"
    italic = "_Italic text_"
    code = "`Code text`"
    link = "[anchor text](url)"
    image = "![alt text](url)"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url:str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode):
        return self.text == other.text and  self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"