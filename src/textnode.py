from enum import Enum

from leafnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url:str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode):
        return self.text == other.text and  self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise AttributeError(f"Text node text type {text_node.text_type} comes from another universe, we don't do that here.")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception(f"No matching {delimiter} in LeafNode: {node.text}")

            split_node = node.text.split(delimiter)

            for i in range(len(split_node)):
                if split_node[i] == "":
                    continue
                if i % 2 == 1:
                    out.append(TextNode(split_node[i], text_type))
                else:
                    out.append(TextNode(split_node[i], TextType.TEXT))
        else:
            out.append(node)

    return out


def extract_markdown_images(text):
    expression = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(expression, text)
    return matches

def extract_markdown_links(text):
    expression = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" #ignores images using (?<!!). Two capture groups
    matches = re.findall(expression, text)
    return matches



def __split_nodes_splitter(old_nodes: list[TextNode], splitter_type: TextType)-> list[TextNode]:
    out = []
    for node in old_nodes:
        splitters: list[tuple[str,str]] = []
        splitter_pattern = ""
        if splitter_type == TextType.IMAGE:
            splitters = extract_markdown_images(node.text)
            splitter_pattern = "![{}]({})"
        elif splitter_type == TextType.LINK:
            splitters = extract_markdown_links(node.text)
            splitter_pattern = "[{}]({})"

        if splitters:
            node_text = node.text
            for splitter in splitters:
                cut_list = node_text.split(splitter_pattern.format(splitter[0], splitter[1]), maxsplit=1)
                if cut_list[0]:
                    out.append(TextNode(cut_list[0], TextType.TEXT))
                out.append(TextNode(splitter[0], splitter_type, splitter[1]))
                node_text = cut_list[1]

            if node_text:
                out.append(TextNode(node_text, TextType.TEXT))
        else:
            out.append(node)

    return out


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return __split_nodes_splitter(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return __split_nodes_splitter(old_nodes, TextType.LINK)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    image_split_nodes = split_nodes_image(nodes)
    link_split_nodes = split_nodes_link(image_split_nodes)
    code_split_nodes = split_nodes_delimiter(link_split_nodes, "`", TextType.CODE)
    italic_split_nodes = split_nodes_delimiter(code_split_nodes, "_", TextType.ITALIC)
    bold_split_nodes = split_nodes_delimiter(italic_split_nodes, "**", TextType.BOLD)
    return bold_split_nodes