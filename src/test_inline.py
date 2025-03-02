import unittest

from textnode import TextNode,TEXT_TYPE
from inlilne_markdown import (split_nodes_delimiter, extract_markdown_images,
                              extract_markdown_links , split_nodes_image , split_nodes_link,
                              text_to_textnodes)

class TestTextDelimiterSplit(unittest.TestCase):
    def test_function_middle(self):
        node = TextNode("This is text with a `code block` word", TEXT_TYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE.CODE)
        new_nodes_result = [
            TextNode("This is text with a ", TEXT_TYPE.TEXT),
            TextNode("code block", TEXT_TYPE.CODE),
            TextNode(" word", TEXT_TYPE.TEXT),
            ]
        self.assertEqual(new_nodes, new_nodes_result)
    def test_function_end(self):
        node = TextNode("This is text with a `code block word`", TEXT_TYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE.CODE)
        new_nodes_result = [
            TextNode("This is text with a ", TEXT_TYPE.TEXT),
            TextNode("code block word", TEXT_TYPE.CODE)
            ]
        self.assertEqual(new_nodes, new_nodes_result)
    def test_function_front(self):
        node = TextNode("`This is text with a `code block word", TEXT_TYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE.CODE)
        new_nodes_result = [
            TextNode("This is text with a ", TEXT_TYPE.CODE),
            TextNode("code block word", TEXT_TYPE.TEXT)
            ]
        self.assertEqual(new_nodes, new_nodes_result)
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TEXT_TYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXT_TYPE.TEXT),
                TextNode("bolded", TEXT_TYPE.BOLD),
                TextNode(" word", TEXT_TYPE.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TEXT_TYPE.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXT_TYPE.TEXT),
                TextNode("bolded", TEXT_TYPE.BOLD),
                TextNode(" word and ", TEXT_TYPE.TEXT),
                TextNode("another", TEXT_TYPE.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TEXT_TYPE.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXT_TYPE.TEXT),
                TextNode("bolded word", TEXT_TYPE.BOLD),
                TextNode(" and ", TEXT_TYPE.TEXT),
                TextNode("another", TEXT_TYPE.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TEXT_TYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TEXT_TYPE.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TEXT_TYPE.TEXT),
                TextNode("italic", TEXT_TYPE.ITALIC),
                TextNode(" word", TEXT_TYPE.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TEXT_TYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TEXT_TYPE.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TEXT_TYPE.BOLD),
                TextNode(" and ", TEXT_TYPE.TEXT),
                TextNode("italic", TEXT_TYPE.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TEXT_TYPE.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXT_TYPE.TEXT),
                TextNode("code block", TEXT_TYPE.CODE),
                TextNode(" word", TEXT_TYPE.TEXT),
            ],
            new_nodes,
        )

class TestImgExtractor(unittest.TestCase):
    def test_one(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), output)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )
class TestSplitImgAndLink(unittest.TestCase):
    def test_1(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                        TEXT_TYPE.TEXT,)
        new_node = split_nodes_link([node])
        test_node =  [
            TextNode("This is text with a link ", TEXT_TYPE.TEXT),
            TextNode("to boot dev", TEXT_TYPE.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TEXT_TYPE.TEXT),
            TextNode("to youtube", TEXT_TYPE.LINKS, "https://www.youtube.com/@bootdotdev"),]
        
        self.assertEqual(new_node, test_node)
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TEXT_TYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TEXT_TYPE.TEXT),
                TextNode("image", TEXT_TYPE.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGES.PNG)",
            TEXT_TYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TEXT_TYPE.IMAGES, "https://www.example.COM/IMAGES.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TEXT_TYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TEXT_TYPE.TEXT),
                TextNode("image", TEXT_TYPE.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TEXT_TYPE.TEXT),
                TextNode(
                    "second image", TEXT_TYPE.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TEXT_TYPE.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXT_TYPE.TEXT),
                TextNode("link", TEXT_TYPE.LINKS, "https://boot.dev"),
                TextNode(" and ", TEXT_TYPE.TEXT),
                TextNode("another link", TEXT_TYPE.LINKS, "https://blog.boot.dev"),
                TextNode(" with text that follows", TEXT_TYPE.TEXT),
            ],
            new_nodes,
        )

class TestTextToNodes(unittest.TestCase):
    def test_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = [
            TextNode("This is ", TEXT_TYPE.TEXT),
            TextNode("text", TEXT_TYPE.BOLD),
            TextNode(" with an ", TEXT_TYPE.TEXT),
            TextNode("italic", TEXT_TYPE.ITALIC),
            TextNode(" word and a ", TEXT_TYPE.TEXT),
            TextNode("code block", TEXT_TYPE.CODE),
            TextNode(" and an ", TEXT_TYPE.TEXT),
            TextNode("obi wan image", TEXT_TYPE.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TEXT_TYPE.TEXT),
            TextNode("link", TEXT_TYPE.LINKS, "https://boot.dev"),]
        self.assertEqual(output, text_to_textnodes(text))
