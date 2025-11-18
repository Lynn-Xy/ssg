from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode
import re

def extract_markdown_images(text):

    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches

def extract_markdown_links(text):

    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches

def split_text_nodes_delimiter(old_text_nodes, delimiter, text_type):

    new_text_nodes = []

    for node in old_text_nodes:

        if node.text_type != TextType.TEXT:

            new_text_nodes.append(node)

            continue

        text_chunks = node.text.split(delimiter)

        if len(text_chunks) % 2 == 0:

            raise Exception("Invalid markdown - missing matching delimiter.")

        for index, chunk in enumerate(text_chunks):

            if index % 2 == 0:

                new_text_nodes.append(TextNode(chunk, TextType.TEXT, None))

            else:

                new_text_nodes.append(TextNode(chunk, text_type, None))

    return new_text_nodes

def split_text_nodes_images(old_nodes):

    new_text_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:

            new_text_nodes.append(node)

            continue

        text = node.text

        markdown_sets = extract_markdown_images(text)

        if not markdown_sets:

            new_text_nodes.append(node)

            continue

        working = text

        for alt_text, url in markdown_sets:

            literal = f"![{alt_text}]({url})"

            before, sep, after = working.partition(literal)

            if before:

                new_text_nodes.append(TextNode(before, TextType.TEXT, None))

            new_text_nodes.append(TextNode(alt_text, TextType.IMAGE, url))


            working = after

        if working:

            new_text_nodes.append(TextNode(working, TextType.TEXT, None))

    return new_text_nodes

def split_text_nodes_links(old_nodes):

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:

            new_text_nodes.append(node)

            continue

        text = node.text

        markdown_sets = extract_markdown_images(text)

        if not markdown_sets:

            new_text_nodes.append(node)

            continue

        working = text

        for alt_text, url in markdown_sets:

            literal = f"![{alt_text}]({url})"

            before, sep, after = working.partition(literal)

            if before:

                new_text_nodes.append(TextNode(before, TextType.TEXT, None))
                                      
                new_text_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

                working = after

            if working:

                new_text_nodes.append(TextNode(working, TextType.TEXT, None))

    return new_text_nodes

def text_node_to_leaf_node(textnode):

    match textnode.text_type:

        case TextType.TEXT:

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

        case TextType.TEXT:

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

        case TextType.TEXT:

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


