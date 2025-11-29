from enum import Enum

class BlockType(Enum):

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):

        if self.tag is None:

            return self.value

        else:
            
            html_string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

            if self.children is not None:

                children_html = ""

                for child in self.children:

                    children_html += child.to_html()

                html_string = f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

            return html_string

    def props_to_html(self):

        formatted_string = ""

        if self.props == None or self.props == {}:

            return formatted_string
        
        for i in self.props.items():

            formatted_string += (f' {i[0]}="{i[1]}"')

        return formatted_string

    def __eq__(self, HTMLNode_2):

        return (
                self.tag == HTMLNode_2.tag and
                self.value == HTMLNode_2.value and
                self.children == HTMLNode_2.children and
                self.props == HTMLNode_2.props
                )

    def __repr__(self):

        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):

        super().__init__(tag, value, props=None)

        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):

        if not self.value:

            raise ValueError("LeafNode must have a value")
        
        if not self.tag:

            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):

        super().__init__(tag, children, props=None)

        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):

        if not self.tag:

            raise ValueError("ParentNode must have a tag.")

        if self.children is None:

            raise ValueError("ParentNode must have children.")

        formatted_string = f""

        for child in self.children:

            formatted_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{formatted_string}</{self.tag}>"


class TextType(Enum):

    TEXT = "plain"
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

        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
