import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):

    def setUp(self):

        self.node_1 = HTMLNode("p", "This is an html node", None, None)
        self.node_2 = HTMLNode("p", "This is also an html node", None, None)
        self.node_3 = HTMLNode("strong", "This is a bolded html node", None, None)
        self.node_4 = HTMLNode("i", "This is an italicized html node", None, None)
        self.node_5 = HTMLNode("a", "This is a linked html node", None, {"href":"https://www.boot.dev"})
        self.node_6 = LeafNode("img", "This is an image leaf node", {"href":"https://www.boot.dev"})
        self.node_7 = HTMLNode("p", "This is an html node", None, None)
        self.node_8 = HTMLNode("h1", "This is a parent html header node", [self.node_2], None)
        self.node_9 = HTMLNode("fake", "This is an html node that shouldn't exist", [self.node_8], {"href":"https://www.boot.dev"})
        self.node_10 = LeafNode("em", "This is a leaf node.", None)

    def test_not_eq_different_tag(self):
                                                                                                          self.assertNotEqual(self.node_2, self.node_8)

    def test_not_eq_invalid_node(self):

        self.assertNotEqual(self.node_5, self.node_9)

    def test_not_eq_different_text(self):

        self.assertNotEqual(self.node_3, self.node_4)
    
    def test_not_eq_different_props(self):
        
        self.assertNotEqual(self.node_6, self.node_10)

    def test_eq(self):

        self.assertEqual(self.node_1, self.node_7)

    def test_eq_props_to_html(self):

        self.assertEqual(self.node_5.props_to_html(), ' href="https://www.boot.dev"')
        self.assertEqual(self.node_6.props_to_html(), self.node_9.props_to_html())

    def test_eq_leafnode(self):

        self.assertEqual(self.node_10.to_html(), "<em>This is a leaf node.</em>")
        self.assertEqual(self.node_6.to_html(), '<img href="https://www.boot.dev">This is an image leaf node</img>')


if __name__ == "__main__":
    unittest.main()
