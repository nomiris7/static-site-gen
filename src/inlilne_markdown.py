import re
from textnode import TextNode, TEXT_TYPE

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        texts = node.text.split(delimiter)
        text_type_old = node.text_type
        for i in range(len(texts)):
            if len(texts[i]) > 0:
                if i % 2 == 0 or i == 0:
                    new_nodes.append(TextNode(texts[i], text_type_old))
                else:
                    new_nodes.append(TextNode(texts[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_images(text)
        text_type_old = node.text_type
        if len(matches) <= 0:
            new_nodes.append(node)
            continue
        for match in matches:
            text = text.split(f"![{match[0]}]({match[1]})", 1)
            if len(text[0]) > 0:
                new_nodes.append(TextNode(text[0], text_type_old))
            new_nodes.append(TextNode(match[0], TEXT_TYPE.IMAGES, match[1]))
            text = "".join(text[1:])
        if len(text) > 0:
            new_nodes.append(TextNode(text, text_type_old))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_links(text)
        text_type_old = node.text_type
        if len(matches) <= 0:
            new_nodes.append(node)
            continue
        for match in matches:
            text = text.split(f"[{match[0]}]({match[1]})", 1)
            if len(text[0]) > 0:
                new_nodes.append(TextNode(text[0], text_type_old))
            new_nodes.append(TextNode(match[0], TEXT_TYPE.LINKS, match[1]))
            text = "".join(text[1:])
        if len(text) > 0:
            new_nodes.append(TextNode(text, text_type_old))
    return new_nodes

def text_to_textnodes(text):
    new_node = TextNode(text,TEXT_TYPE.TEXT)
    nodes = split_nodes_delimiter([new_node], "**", TEXT_TYPE.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TEXT_TYPE.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TEXT_TYPE.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes