import re
from enum import Enum
from htmlnode import HTLMNode,ParentNode,LeafNode
from textnode import TEXT_TYPE, text_node_to_html_node, TextNode
from inlilne_markdown import text_to_textnodes


class BLOCKTYPE(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if len(block) > 0:
            text = block.strip()
            stripped_blocks.append(text)
    return stripped_blocks

def block_to_block_type(markdown):
    if re.search(r"^\#{1,6}[ ]", markdown):
        return BLOCKTYPE.HEADING
    if re.search(r"\`{3}([\s\S]*?)`{3}",markdown):
        return BLOCKTYPE.CODE
    
    lines = markdown.split("\n")
    if markdown[0] == ">":
        for line in lines:
            if line[0] != ">":
                return BLOCKTYPE.PARAGRAPH
        return BLOCKTYPE.QUOTE
    
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BLOCKTYPE.PARAGRAPH
        return BLOCKTYPE.UNORDERED_LIST
    
    if re.search(r"^(1. )", markdown):
        for i, line in enumerate(lines):
            if not re.search(f"^({i+1}. )", line):
                return BLOCKTYPE.PARAGRAPH
            return BLOCKTYPE.ORDERED_LIST
    return BLOCKTYPE.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        node = block_to_html_node(block)
        children.append(node)
    return ParentNode("div",children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BLOCKTYPE.PARAGRAPH:
            return block_to_paragraph(block)
        case BLOCKTYPE.HEADING:
            return block_to_heading(block)
        case BLOCKTYPE.QUOTE:
            return block_to_quotes(block)
        case BLOCKTYPE.CODE:
            return block_to_code(block)
        case BLOCKTYPE.UNORDERED_LIST:
            return block_to_ulist(block)
        case BLOCKTYPE.ORDERED_LIST:
            return block_to_olist(block)
        case _:
            raise ValueError("invalid md block type")

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def block_to_paragraph(block) -> ParentNode:
    lines = block.split("\n")
    lines = " ".join(lines)
    nodes = text_to_children(lines)
    return ParentNode("p", nodes)

def block_to_heading(block) -> ParentNode:
    i = 0
    while block[i] == "#":
        i += 1
    heading_text = block[i+1:]
    nodes = text_to_children(heading_text)
    return ParentNode(f"h{i}", nodes)

def block_to_code(block) -> ParentNode:
    blocks = block[4:-3]
    node = TextNode(blocks, TEXT_TYPE.CODE)
    nodes = text_node_to_html_node(node)
    return ParentNode('pre', [nodes])

def block_to_quotes(block) -> ParentNode:
    lines = block.split("\n")
    sanitized_lines = []
    for line in lines:
        line_ = line.lstrip(">").strip()
        if len(line_) > 0:
            sanitized_lines.append(line_)
    text = " ".join(sanitized_lines)
    nodes = text_to_children(text)
    return ParentNode("blockquote", nodes)

def block_to_olist(block) -> ParentNode:
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        text = line[3:]
        node = text_to_children(text)
        children_nodes.append(ParentNode("li",node))
    return ParentNode('ol', children_nodes)


def block_to_ulist(block) -> ParentNode:
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        text = line[2:]
        node = text_to_children(text)
        children_nodes.append(ParentNode("li",node))
    return ParentNode('ul', children_nodes)