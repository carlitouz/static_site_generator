import unittest
from htmlnode import HTMLNode

test_dict = {}
test_dict2 = {
    "href": "urllink.com",
    }

test_dict3 = {
    "href": "urllink.com",
    "target": "_blank",
    }

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "value text", None, test_dict2)
        node2 = HTMLNode("a", "value text", None, test_dict2)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_noteq(self):
        node = HTMLNode("h1", "value text", None, test_dict)
        node2 = HTMLNode("b", "value_text", None, test_dict2)
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

    def test_propsEmpty(self):
        node = HTMLNode(None, None, None, test_dict)
        self.assertEqual(node.props_to_html(), "")

    def test_propsEq(self):
        node = HTMLNode(None, None, None, test_dict2)
        self.assertEqual(node.props_to_html(), ' href="urllink.com"')

    def test_propsMultiKeys(self):
        node = HTMLNode(None, None, None, test_dict3)
        self.assertEqual(node.props_to_html(), ' href="urllink.com" target="_blank"')

    def test_propsNone(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()