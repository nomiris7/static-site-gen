from enum import Enum
from htmlnode import LeafNode

class TEXT_TYPE(Enum):
    TEXT = "normal text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINKS = "links"
    IMAGES = "images"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})")
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TEXT_TYPE.TEXT:
            return LeafNode(None, text_node.text)
        case TEXT_TYPE.BOLD:
            return LeafNode("b", text_node.text)
        case TEXT_TYPE.ITALIC:
            return LeafNode("i", text_node.text)
        case TEXT_TYPE.CODE:
            return LeafNode('code', text_node.text)
        case TEXT_TYPE.LINKS:
            return LeafNode('a', text_node.text, {"href": text_node.url})
        case TEXT_TYPE.IMAGES:
            return LeafNode('img', "" ,{"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")