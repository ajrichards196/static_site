import unittest

from htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):

    def test_props(self):
        props = {
                "href": "https://www.google.com", 
                "target": "_blank",
            }
        text_props =  'href="https://www.google.com" target="_blank"'
        node1 = HTMLNode(props=props)
        self.assertEqual(node1.props_to_html(), text_props)

    def test_leaf(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        rend1 = '<p>This is a paragraph of text.</p>'
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        rend2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node1.to_html(), rend1)
        self.assertEqual(node2.to_html(), rend2)

    def test_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), html)

    def test_nest_parent(self):
        # This is just a structure example
        nested_node = ParentNode("div", [
            ParentNode("section", [
                LeafNode("p", "text")
            ])
        ])
        html = '<div><section><p>text</p></section></div>'
        self.assertEqual(nested_node.to_html(), html)

    def test_func_text(self):
        text_node = TextNode('hello world', TextType.TEXT)
        html = text_node_to_html_node(text_node)
        text = 'hello world'
        self.assertEqual(text, html.to_html())

    def test_func_bold(self):
        text_node = TextNode('hello bold world', TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        text = '<b>hello bold world</b>'
        self.assertEqual(text, html_node.to_html())

    def test_func_link(self):
        text_node = TextNode('tha beeb', TextType.LINK, url='www.bbc.co.uk')
        html_node = text_node_to_html_node(text_node)
        text = '<a href="www.bbc.co.uk">tha beeb</a>'
        self.assertEqual(text, html_node.to_html())

    def test_func_image(self):
        text_node = TextNode('Girl in a jacket', TextType.IMAGE, url="img_girl.jpg")
        html_node = text_node_to_html_node(text_node)
        text = '<img src="img_girl.jpg" alt="Girl in a jacket"></img>'
        self.assertEqual(text, html_node.to_html())

    
