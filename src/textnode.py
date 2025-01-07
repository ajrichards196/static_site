from enum import Enum
from htmlnode import *
import re

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

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
        print(node.text_type)
        print(node.text_type.value)
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue
        split = node.text.split(delimiter) 
        if len(split) == 2:
            raise Exception("No closing delimiter, invalid markdown")
        if len(split) < 2:
            new_nodes.append(node)
            continue
        new_nodes.append(TextNode(split[0], TextType.TEXT))
        new_nodes.append(TextNode(split[1], text_type))
        new_nodes.append(TextNode(split[2], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            text = node.text
            prev_end = 0
            for match in re.finditer(r"!\[(.*?)\]\((.*?)\)", text):
                alt_text, image_url = match.groups()
                start, end = match.span()
                if start > prev_end:
                    new_nodes.append(TextNode(text=text[prev_end:start], text_type=TextType.TEXT))
                new_nodes.append(TextNode(text=alt_text, text_type=TextType.IMAGE, url=image_url))
                prev_end = end
            if prev_end < len(text):
                new_nodes.append(TextNode(text=text[prev_end:], text_type=TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            text = node.text
            prev_end = 0
            for match in re.finditer(r"\[(.*?)\]\((.*?)\)", text):
                alt_text, url = match.groups()
                start, end = match.span()
                if start > prev_end:
                    new_nodes.append(TextNode(text=text[prev_end:start], text_type=TextType.TEXT))
                new_nodes.append(TextNode(text=alt_text, text_type=TextType.LINK, url=url))
                prev_end = end
            if prev_end < len(text):
                new_nodes.append(TextNode(text=text[prev_end:], text_type=TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    print('splitting bold')
    split_bold = split_nodes_delimiter([node], '**', TextType.BOLD)
    print(split_bold)
    print('splitting italics')
    split_italic = split_nodes_delimiter(split_bold, '*', TextType.ITALIC)
    print(split_italic)
    print('splitting code')
    split_code = split_nodes_delimiter(split_italic, '`', TextType.CODE)
    print('splitting images')
    split_image = split_nodes_image(split_code)
    print('splitting links')
    split_links = split_nodes_link(split_image)
    return split_links