import unittest
from textnode import TextType, TextNode
from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_heading_levels(self):
        for i in range(1,7):
            block = f"{'#' * i} heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_invalid_heading(self):
        block = "####### not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_requires_space(self):
        block = "#heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nsome code here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote_multiline(self):
        block = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_mixed_lines(self):
        block = "> line one\nnot a quote\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three\n- item four"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_wrong_start(self):
        block = "2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_skips_number(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph(self):
        block = "just some normal text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading_with_bold(self):
        md = """
# Header **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Header <b>bold</b></h1></div>"
        )

    def test_multiple_quotes(self):
        md = """
> First quote
> Second quote
> Third quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>First quote Second quote Third quote</blockquote></div>"
        )
    
    def test_ordered_list_with_inline_differences(self):
        md = """
1. Plain item
2. **Bold item**
3. _Italic item_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Plain item</li><li><b>Bold item</b></li><li><i>Italic item</i></li></ol></div>"
            )

    def test_paragraph_with_link(self):
        md = """
My paragraph with a link [to my website](http://www.mywebsite.com)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>My paragraph with a link <a href="http://www.mywebsite.com">to my website</a></p></div>'
        )

    def test_paragraph_with_image(self):
        md = """
My paragraph with an image ![image description](https://image.com/image.jpg)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>My paragraph with an image <img src="https://image.com/image.jpg" alt="image description"></p></div>'
        )
