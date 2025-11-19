import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from block import BlockType
from functions import *

class TestTextNode(unittest.TestCase):

    def setUp(self):

        self.node_1 = TextNode("This is a text node", TextType.TEXT)
        self.node_2 = TextNode("This is also a text node", TextType.TEXT)
        self.node_3 = TextNode("This is a bolded text node", TextType.BOLD)
        self.node_4 = TextNode("This is an italicized text node", TextType.ITALIC)
        self.node_5 = TextNode("This is a linked text node", TextType.LINK, "https://www.boot.dev")
        self.node_6 = TextNode("This is an image text node", TextType.IMAGE, "https://www.boot.dev")
        self.node_7 = TextNode("This is a text node", TextType.TEXT)
        self.node_8 = TextNode("This is a text node", TextType.BOLD)
        self.node_9 = TextNode("This is a text node that shouldn't exist", TextType.TEXT, "https://www.boot.dev")
        self.node_10 = TextNode("This is the last text node.", TextType.BOLD)
        self.node_11 = TextNode("This is a text node with an ![image](https://www.boot.dev", TextType.TEXT, None)
        self.node_12 = TextNode("This is a text node with a [link](https://www.boot.dev", TextType.TEXT, None)
        self.text_1 = "This is **some** text _with_ a `code block` and a [link](https://www.boot.dev) with an ![image](https://www.boot.dev)."
        self.text_2 = """

This is a block.

This is a block.

This is also a block.

"""
        self.text_3 = """

###### This is a header block.

```
This is a code block.
```

> This is a quote block.

- This is an unordered list.

1. This is an ordered list.

This is a paragraph block.
"""

    def test_not_eq_different_type(self):

        self.assertNotEqual(self.node_2, self.node_8)

    def test_not_eq_invalid_node(self):

        self.assertNotEqual(self.node_5, self.node_9)

    def test_not_eq_different_text(self):

        self.assertNotEqual(self.node_3, self.node_4)

    def test_not_eq_no_url(self):

        self.assertNotEqual(self.node_6, self.node_10)

    def test_eq(self):

        self.assertEqual(self.node_1, self.node_7)

    def text_eq_split_text_node_images(self):

        self.assertEqual(split_text_nodes_images(self.node), [TextNode("This is a text node with an ", TextType.Text, None), TextNode("image", TextType.IMAGE, "https://www.boot.dev")])

    def text_eq_split_text_node_images(self):

        self.assertEqual(split_text_nodes_links(self.node), [TextNode("This is a text node with a ", TextType.Text, None), TextNode("link", TextType.LINK, "https://www.boot.dev")])

    def test_eq_text_to_text_nodes(self):

        self.assertEqual(text_to_text_nodes(self.text_1), [TextNode("This is ", TextType.TEXT, None), TextNode("some", TextType.BOLD, None), TextNode(" text ", TextType.TEXT, None), TextNode("with", TextType.ITALIC, None), TextNode(" a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" and a ", TextType.TEXT, None), TextNode("link", TextType.LINK, "https://www.boot.dev"), TextNode(" with an ", TextType.TEXT, None), TextNode("image", TextType.IMAGE, "https://www.boot.dev"), TextNode(".", TextType.TEXT, None)])

    def test_eq_markdown_text_to_blocks(self):

        self.assertEqual(markdown_text_to_blocks(self.text_2), ["This is a block.", "This is a block.", "This is also a block."])

    def test_eq_block_to_block_type(self):

        blocks = markdown_text_to_blocks(self.text_3)

        self.assertEqual(block_to_block_type(blocks[0]), BlockType.H)


if __name__ == "__main__":
    unittest.main()
