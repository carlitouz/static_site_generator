from enum import Enum
from htmlnode import *
from inline_markdown import *
from textnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    new_blocks = []
    for block in block_strings:
        if not block.strip():
            continue
        new_blocks.append(block.strip())
    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    def isHeader(text):
        count = 0
        for ch in text:
            if ch == "#":
                count += 1
            else:
                break
        return 1 <= count <= 6 and len(text) > count and text[count] == " "

    if isHeader(block) and len(lines) == 1:
        return BlockType.HEADING
    if lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def block_type_to_html_node(block_type, text):
    match block_type:
        case BlockType.HEADING:
            h_size = len(text) - len(text.lstrip("#"))
            children = text_to_children(text[h_size + 1:])
            return ParentNode(f"h{h_size}", children)
        case BlockType.QUOTE:
            lines = text.split("\n")
            cleaned = [line.lstrip(">").lstrip() for line in lines]
            prepared_text = " ".join(cleaned)
            children = text_to_children(prepared_text)
            return ParentNode("blockquote", children)

        case BlockType.UNORDERED_LIST:
            lines = text.split("\n")
            cleaned = [line[2:] for line in lines]
            children = [ParentNode("li", text_to_children(line)) for line in cleaned]
            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            lines = text.split("\n")
            cleaned = [line.split(". ")[1] for line in lines]
            children = [ParentNode("li", text_to_children(line)) for line in cleaned]
            return ParentNode("ol", children)

        case BlockType.PARAGRAPH:
            lines = text.split("\n")
            prepared_text = " ".join(lines)
            children = text_to_children(prepared_text)
            return ParentNode("p", children)

        case BlockType.CODE:
            prepared_text = text.split("```")
            code_textnode = TextNode(prepared_text[1].lstrip("\n"), TextType.CODE)
            code_htmlnode = text_node_to_html_node(code_textnode)
            return ParentNode("pre", [code_htmlnode])

        case _:
            return Exception

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_type_to_html_node(block_type, block)
        child_nodes.append(html_node)

    return ParentNode("div", child_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children