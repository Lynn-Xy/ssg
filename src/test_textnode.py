import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):

    def setUp(self):

        self.node_1 = TextNode("This is a text node", TextType.PLAIN)
        self.node_2 = TextNode("This is also a text node", TextType.PLAIN)
        self.node_3 = TextNode("This is a bolded text node", TextType.BOLD)
        self.node_4 = TextNode("This is an italicized text node", TextType.ITALIC)
        self.node_5 = TextNode("This is a linked text node", TextType.LINK, "https://www.boot.dev")
        self.node_6 = TextNode("This is an image text node", TextType.IMAGE, "https://www.boot.dev")
        self.node_7 = TextNode("This is a text node", TextType.PLAIN)
        self.node_8 = TextNode("This is a text node", TextType.BOLD)
        self.node_9 = TextNode("This is a text node that shouldn't exist", TextType.PLAIN, "https://www.boot.dev")
        self.node_10 = TextNode("This is the last text node.", TextType.BOLD)

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

if __name__ == "__main__":
    unittest.main()
