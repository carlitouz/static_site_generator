import unittest

from textnode import TextType, TextNode
from inline_markdown import *

class TestSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_non_text(self):
        node = TextNode("bold text", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("bold text", TextType.BOLD)]
        self.assertEqual(result, expected)


    def test_split_nodes_delimiter_unbalanced(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This has **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_empty_nodes(self):
        node = TextNode("**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_without_alt_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links_without_anchor_text(self):
        matches = extract_markdown_links(
            "This is text with an [](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_without_url_text(self):
        matches = extract_markdown_images(
            "This is text with an ![alt text]()"
        )
        self.assertListEqual([("alt text", "")], matches)
    
    def test_extract_markdown_links_without_url_text(self):
        matches = extract_markdown_links(
            "This is text with an [anchor text]()"
        )
        self.assertListEqual([("anchor text", "")], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "Here is ![img](https://img.com/a.png) and [site](https://site.com)"
        )
        self.assertListEqual([("site", "https://site.com")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](https://a.com) text ![two](https://b.com)"
        )
        self.assertListEqual(
            [("one", "https://a.com"), ("two", "https://b.com")],
            matches,
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[one](https://a.com) text [two](https://b.com)"
        )
        self.assertListEqual(
            [("one", "https://a.com"), ("two", "https://b.com")],
            matches,
        )

    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image(self):
        node = TextNode("This is text with an image ![alt text here](https://image.com/image.png) and ![Image link to YouTube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("alt text here", TextType.IMAGE, "https://image.com/image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Image link to YouTube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(result, expected)

    def test_split_links_multiple(self):
        node = TextNode("start [one](https://a.com) middle [two](https://b.com) end", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("start ", TextType.TEXT),
            TextNode("one", TextType.LINK, "https://a.com"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.LINK, "https://b.com"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_split_image_at_start(self):
        node = TextNode("![alt](https://img.com) tail", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("alt", TextType.IMAGE, "https://img.com"),
            TextNode(" tail", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_split_link_at_end(self):
        node = TextNode(
            "head [one](https://a.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("head ", TextType.TEXT),
            TextNode("one", TextType.LINK, "https://a.com")
        ]
        self.assertEqual(result, expected)
    
    def test_split_links_non_text(self):
        node = TextNode("boot.dev", TextType.LINK, "https://boot.dev")
        result = split_nodes_link([node])
        expected = [
            TextNode("boot.dev", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_happy_path(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_plain_text_only(self):
        text = "This is only plain text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is only plain text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_single_type_bold(self):
        text = "Only **bold** type"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Only ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" type", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_text_to_textnodes_single_type_italic(self):
        text = "Only _italic_ type"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Only ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" type", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_single_type_code(self):
        text = "Only `code` type"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Only ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" type", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_text_to_textnodes_adjacent_types(self):
        text = "Testing **bold** _italic_"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Testing ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        expected = []
        self.assertEqual(result, expected)
    
    def test_text_to_textnodes_no_closing_delimiter(self):
        text = "Text without a **closing delimiter"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    