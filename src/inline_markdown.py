from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []         
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(node.text.split(delimiter)) % 2 == 0:
            raise Exception("Unbalanced delimiter")
        else:
            split_node = node.text.split(delimiter)
            for i in range(len(split_node)):
                if split_node[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_node[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_node[i], text_type))
                    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue

        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            left_part = sections[0]
            right_part = sections[1]
            
            if left_part:
                new_nodes.append(TextNode(left_part, TextType.TEXT))    
            
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = right_part
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue


        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            left_part = sections[0]
            right_part = sections[1]
            
            if left_part:
                new_nodes.append(TextNode(left_part, TextType.TEXT))    
            
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = right_part
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
            

    return new_nodes
    

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
