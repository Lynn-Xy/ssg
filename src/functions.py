from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode

def split_text_nodes_delimiter(old_text_nodes, delimiter, text_type):

    new_text_nodes = []

    for node in old_text_nodes:

        if node.text_type != TextType.PLAIN:

            new_text_nodes.append(node)

            continue

        text_chunks = node.text.split(delimiter)

        if len(text_chunks) % 2 == 0:

            raise Exception("Invalid markdown - missing matching delimiter.")

        for index, chunk in enumerate(text_chunks):

            if index % 2 == 0:

                new_text_nodes.append(TextNode(chunk, TextType.PLAIN, None))

            else:

                new_text_nodes.append(TextNode(chunk, text_type, None))

    return new_text_nodes

def text_node_to_leaf_node(textnode):

    match textnode.text_type:

        case TextType.PLAIN:

            return LeafNode(None, textnode.text, None)

        case TextType.BOLD:

            return LeafNode("b", textnode.text, None)

        case TextType.ITALIC:

            return LeafNode("i", textnode.text, None)

        case TextType.CODE:

            return LeafNode("code", textnode.text, None)

        case TextType.LINK:

            if textnode.url is None:

                raise Exception("Link node is missing url.")

            return LeafNode("a", textnode.text, {"href": textnode.url})

        case TextType.IMAGE:

            if textnode.url is None:

                raise Exception("Image node is missing url.")

            return LeafNode("img", "", {"src": textnode.url, "alt":textnode.text})

        case _:

            raise Exception("Invalid htmlnode text type.")


def text_node_to_html_node(textnode):

    match textnode.text_type:

        case TextType.PLAIN:

            return HTMLNode(None, textnode.text, None, None)

        case TextType.BOLD:

            return HTMLNode("b", textnode.text, None, None)

        case TextType.ITALIC:

            return HTMLNode("i", textnode.text, None, None)

        case TextType.CODE:

            return HTMLNode("code", textnode.text, None, None)

        case TextType.LINK:

            if textnode.url is None:

                raise Exception("Link node is missing url.")

            return HTMLNode("a", textnode.text, None, {"href": textnode.url})

        case TextType.IMAGE:

            if textnode.url is None:

                raise Exception("Image node is missing url.")

            return HTMLNode("img", "", None, {"src": textnode.url, "alt":textnode.text})

        case _:

            raise Exception("Invalid htmlnode text type.")


def text_node_to_parent_node(textnode):

    match textnode.text_type:

        case TextType.PLAIN:

            return ParentNode(None, textnode.text, None)

        case TextType.BOLD:

            return ParentNode("b", textnode.text, None)

        case TextType.ITALIC:

            return ParentNode("i", textnode.text, None)

        case TextType.CODE:

            return ParentNode("code", textnode.text, None)

        case TextType.LINK:

            if textnode.url is None:

                raise Exception("Link node is missing url.")

            return ParentNode("a", textnode.text, {"href": textnode.url})

        case TextType.IMAGE:

            if textnode.url is None:

                raise Exception("Image node is missing url.")

            return ParentNode("img", "", {"src": textnode.url, "alt":textnode.text})

        case _:

            raise Exception("Invalid htmlnode text type.")


