from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, TextNode):
        if (self.text == TextNode.text 
            and self.text_type == TextNode.text_type 
            and self.url == TextNode.url
            ):
            return True
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node:TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag='code', value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag='img',value='',props={'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception("incorrect text type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
        split = node.text.split(delimiter) 
        if len(split) == 2:
            raise Exception("No closing delimiter, invalid markdown")
        new_nodes.append(TextNode(split[0], TextType.TEXT))
        new_nodes.append(TextNode(split[1], text_type))
        new_nodes.append(TextNode(split[2], TextType.TEXT))
    return new_nodes
