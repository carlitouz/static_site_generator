import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

test_dict = {}
test_dict2 = {
    "href": "urllink.com",
    }

test_dict3 = {
    "href": "urllink.com",
    "target": "_blank",
    }

image_dict = {
    "src": "http://linkurl.com"
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
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", test_dict2)
        self.assertEqual(node.to_html(), '<a href="urllink.com">Click me!</a>')
    
    def test_leaf_to_html_propsMultiKeys(self):
        node = LeafNode("a", "Click me!", test_dict3)
        self.assertEqual(node.to_html(), '<a href="urllink.com" target="_blank">Click me!</a>')

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "link text here")
        self.assertEqual(node.to_html(), '<a>link text here</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_nested_parents_and_multiple_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node_2 = LeafNode("a", "grandchild2", test_dict3)
        child_node = ParentNode("span", [grandchild_node, grandchild_node_2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span><b>grandchild</b><a href="urllink.com" target="_blank">grandchild2</a></span></div>')


if __name__ == "__main__":
    unittest.main()