from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode
from block import BlockType
import re

def block_to_block_type(block):

    if re.search(r"^#{1,6}\s", block):

        return BlockType.HEADING
    
    elif re.search(r"^```.*```$", block, re.DOTALL):

        return BlockType.CODE

    elif re.search(r"^>", block, re.M):

        return BlockType.QUOTE

    elif re.search(r"^-\s", block):

        return BlockType.UNORDERED_LIST

    elif re.search(r"^\d+\.\s", block, re.M):

        return BlockType.ORDERED_LIST

    else:

        return BlockType.PARAGRAPH

def extract_markdown_images(text):

    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches

def extract_markdown_links(text):

    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches

def markdown_text_to_blocks(text):

    new_blocks = []

    blocks = text.split("\n\n")

    for block in blocks:

        if block == "":

            continue

        new_blocks.append(block.strip())

    return new_blocks

def markdown_to_html_node(markdown):

    html_nodes = []

    for block in markdown_text_to_blocks(markdown):

        block_type = block_to_block_type(block)

        match block_type:

            case BlockType.CODE:

                lines = block.split("\n")

                block = "\n".join(lines[1:-1])

                node = text_node_to_html_node(TextNode(block, TextType.CODE, None))

                html_nodes.append(ParentNode("pre", [node], None))

            case BlockType.HEADING:

               matched = re.match(r"^#+\s", block)

               if matched:

                   matched_text = matched.group(0)

                   heading_level = matched_text.count("#")

                   heading_text = block[len(matched_text):]

                   sub_nodes = []

                   for node in text_to_text_nodes(heading_text):

                       sub_nodes.append(text_node_to_html_node(node))

                    html_nodes.append(ParentNode(f"h{heading_level}", sub_nodes, None))

            case BlockType.QUOTE:

                lines = block.split("\n")

                cleaned_block = ""

                for line in lines:

                    cleaned_line = line.lstrip(">").lstrip()

                    cleaned_block += cleaned_line + "\n"

                cleaned_block = cleaned_block.rstrip("\n")

                sub_nodes = []

                for node in text_to_text_nodes(cleaned_block):

                    sub_nodes.append(text_node_to_html_node(node))

                html_nodes.append(ParentNode("blockquote", sub_nodes, None))

            case BlockType.ORDERED_LIST:

                sub_nodes = []

                for line in block.split("\n"):

                    match = re.match(r"^\d+\.\s", line)

                    if match:

                        matched_text = match.group(0)

                        line_text = line[len(matched_text):]

                        children = []

                        for node in text_to_text_nodes(line_text):

                            child_node = text_node_to_html_node(node)
                            children.append(child_node)

                        sub_nodes.append(HTMLNode("li", None, children, None))

                html_nodes.append(ParentNode("ol", sub_nodes, None))

            case BlockType.UNORDERED_LIST:

                sub_nodes = []

                for line in block.split("\n"):

                    match = re.match(r"^-\s", line)

                    if match:

                        matched_text = match.group(0)

                        line_text = line[len(matched_text):]

                        children = []

                        for node in text_to_text_nodes(line_text):

                            child_node = text_node_to_html_node(node)

                            children.append(child_node)

                        sub_nodes.append(HTMLNode("li", None, children, None))

                html_nodes.append(ParentNode("ul", sub_nodes, None))

            case BlockType.PARAGRAPH:

                sub_nodes = []

                for node in text_to_text_nodes(block):

                    sub_nodes.append(text_node_to_html_node(node))

                html_nodes.append(ParentNode("p", sub_nodes, None))

            case _:

                raise Exception("Invalid BlockType.")

    return ParentNode("div", html_nodes, None)

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

            if chunk == "":

                continue

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

    new_text_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:

            new_text_nodes.append(node)

            continue

        text = node.text

        markdown_sets = extract_markdown_links(text)

        if not markdown_sets:

            new_text_nodes.append(node)

            continue

        working = text

        for alt_text, url in markdown_sets:

            literal = f"[{alt_text}]({url})"

            before, sep, after = working.partition(literal)

            if before:

                new_text_nodes.append(TextNode(before, TextType.TEXT, None))
                                      
            new_text_nodes.append(TextNode(alt_text, TextType.LINK, url))

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

def text_to_text_nodes(text):

    node = TextNode(text, TextType.TEXT, None)

    nodes = split_text_nodes_delimiter([node], "**", TextType.BOLD)

    nodes = split_text_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_text_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_text_nodes_images(nodes)

    nodes = split_text_nodes_links(nodes)

    return nodes
