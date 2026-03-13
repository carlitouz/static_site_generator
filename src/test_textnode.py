import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.LINK, url=None)
        node2 = TextNode("This is a text node", TextType.LINK, url=None)
        self.assertEqual(node, node2)

    def test_url_diff(self):
        node = TextNode("This is a text node", TextType.LINK, url=None)
        node2 = TextNode("This is a text node", TextType.LINK, url="www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text_noteq(self):
        node = TextNode("My first line", TextType.BOLD)
        node2 = TextNode("My second line", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("This is a link node with prop", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node with prop")
        self.assertEqual(html_node.props, {'href': "www.google.com"})
        self.assertEqual(html_node.to_html(), '<a href="www.google.com">This is a link node with prop</a>')

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "image/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': "image/image.png", 'alt': "alt text"})

    def test_invalid_type(self):
        node = TextNode("some text", "not_a_valid_type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
    
    def test_link_url_none(self):
        node = TextNode("Click me!", TextType.LINK, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="None">Click me!</a>')

if __name__ == "__main__":
    unittest.main()