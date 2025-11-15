class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):

        raise NotImplementedError()

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

        if self.value is None:

            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:

            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
