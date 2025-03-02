import unittest

from htmlnode import HTLMNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props(self):
        prop = {
            "href": "https://www.google.com",
            "target": "_blank",}
        node = HTLMNode('p','siemano', None, prop)
        text = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(text, node.props_to_html())
    
class TestLeafNode(unittest.TestCase):
    def test_string(self):
        str1 = "<p>This is a paragraph of text.</p>"
        str2 = '<a href="https://www.google.com">Click me!</a>'
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode(None, "Big bones are scam")
        self.assertEqual(str1, node1.to_html())
        self.assertEqual(str2, node2.to_html())
        self.assertEqual("Big bones are scam", node3.to_html())

    def test_none_for_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(None, None)

class TestParentNode(unittest.TestCase):
    def test_parent(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
        text = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), text)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_none_for_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "Bold text")])
    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
if __name__ == "__main__":
    unittest.main()