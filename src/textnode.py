from enum import Enum

class TextType(Enum):

    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    
    def __init__(self, text, text_type, url=None):

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, TextNode_2):

        return (
                self.text_type == TextNode_2.text_type and
                self.text == TextNode_2.text and
                self.url == TextNode_2.url
                )

    def __repr__(self):

        return f"TextNode({self.text}, {self.text_type.values}, {self.url})"
