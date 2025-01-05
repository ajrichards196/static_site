import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, 'www.bbc.co.uk')
        node2 = TextNode("This is a text node", TextType.BOLD, 'www.bbc.co.uk')
        self.assertEqual(node, node2)

    def test_diff_type(self):
        node1 = TextNode("textnode", TextType.ITALIC)
        node2 = TextNode("textnode", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_diff_text(self):
        node1 = TextNode("textnode1", TextType.BOLD)
        node2 = TextNode("textnode2", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_diff_url(self):
        node1 = TextNode("textnode1", TextType.BOLD, 'www.bbc.co.uk')
        node2 = TextNode("textnode1", TextType.BOLD)
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()