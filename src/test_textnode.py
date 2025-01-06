import unittest

from textnode import *

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

class TestSplitText(unittest.TestCase):

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        node_list = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                ]
        self.assertEqual(new_nodes, node_list)

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        node_list = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" word", TextType.TEXT),
                ]
        self.assertEqual(new_nodes, node_list)

    def test_split_italic(self):
        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        node_list = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word", TextType.TEXT),
                ]
        self.assertEqual(new_nodes, node_list)

    def test_split_no_closing(self):
        node = TextNode("Text with **one delimiter", TextType.TEXT)
        args = ([node], "**", TextType.BOLD)
        self.assertRaises(Exception, split_nodes_delimiter, args=args)

if __name__ == "__main__":
    unittest.main()