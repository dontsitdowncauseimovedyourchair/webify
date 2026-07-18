from enum import Enum
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_to_textnodes, text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"

def markdown_to_blocks(markdown) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = [block.strip() for block in blocks if block.strip()]
    return filtered_blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith("#"):
        tag_count = 0
        index = 0
        for i in range(len(block)): #check number of #
            if block[i] != "#":
                tag_count = i
                index = i
                break
        if 0 < tag_count <= 6 and index < len(block) and block[index] == " ":
            return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE

    is_ul = True
    is_ol = True

    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            is_ol = False
        if not lines[i].startswith("- "):
            is_ul = False

    if is_ul:
        return BlockType.UNORDERED_LIST
    elif is_ol:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_raw_lines(block: str, block_type: BlockType) -> list[str]:
    out = None
    match block_type:
        case BlockType.PARAGRAPH:
            out = block.split("\n")
        case BlockType.HEADING:
            lines = block.split("\n")
            strt_indx = 0
            for i in range(len(lines[0])):
                if lines[0][i] == " ":
                    strt_indx = i + 1
                    break
            out = [lines[0][strt_indx:]] + lines[1:]
        case BlockType.QUOTE:
            lines = block.split("\n")
            out = list(map(lambda line: line[2:] if len(line) >= 2 and " " == line[1] else line[1:],lines))
        case BlockType.CODE:
            lines = block.split("\n")
            lines[-1] = lines[-1][:-3]
            if not lines[-1]:
                del lines[-1]
            out = lines[1:]
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            out = list(map(lambda line: line[2:], lines))
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            out = list(map(lambda line: line.split(" ", maxsplit=1)[1], lines))
    return out


def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    match block_type:
        case BlockType.PARAGRAPH:
            raw_lines = markdown_to_raw_lines(block, BlockType.PARAGRAPH)
            child_text = "\n".join(raw_lines)
            child_text_nodes = text_to_textnodes(child_text)
            child_html_nodes = [text_node_to_html_node(node) for node in child_text_nodes]
            return ParentNode("p", child_html_nodes)

        case BlockType.HEADING:
            raw_lines = markdown_to_raw_lines(block, BlockType.HEADING)
            child_text = "\n".join(raw_lines)
            child_text_nodes = text_to_textnodes(child_text)
            child_html_nodes = [text_node_to_html_node(node) for node in child_text_nodes]
            h_count = len(block.split(" ", maxsplit=1)[0])
            return ParentNode(f"h{h_count}", child_html_nodes)

        case BlockType.QUOTE:
            raw_lines = markdown_to_raw_lines(block, BlockType.QUOTE)
            child_text = "\n".join(raw_lines)
            child_text_nodes = text_to_textnodes(child_text)
            child_html_nodes = [text_node_to_html_node(node) for node in child_text_nodes]
            return ParentNode("blockquote", child_html_nodes)

        case BlockType.CODE:
            raw_lines = markdown_to_raw_lines(block, BlockType.CODE)
            child_text = "\n".join(raw_lines)
            child_text_nodes = [TextNode(child_text, TextType.TEXT)]
            child_html_nodes = [text_node_to_html_node(node) for node in child_text_nodes]
            return ParentNode("pre", [ParentNode("code", child_html_nodes)])

        case BlockType.UNORDERED_LIST:
            raw_lines = markdown_to_raw_lines(block, BlockType.UNORDERED_LIST)
            child_text_nodes_list = [text_to_textnodes(line) for line in raw_lines]
            li_nodes = []
            for nodes_list in child_text_nodes_list:
                child_html_nodes = [text_node_to_html_node(node) for node in nodes_list]
                li_nodes.append(ParentNode("li", child_html_nodes))
            return ParentNode("ul", li_nodes)

        case BlockType.ORDERED_LIST:
            raw_lines = markdown_to_raw_lines(block, BlockType.ORDERED_LIST)
            child_text_nodes_list = [text_to_textnodes(line) for line in raw_lines]
            li_nodes = []
            for nodes_list in child_text_nodes_list:
                child_html_nodes = [text_node_to_html_node(node) for node in nodes_list]
                li_nodes.append(ParentNode("li", child_html_nodes))
            return ParentNode("ol", li_nodes)

# def markdown_to_html_nodes(markdown)HTMLNode:
#     blocks = markdown_to_blocks(markdown)
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         html_node = block_to_html_node(block, block_type)