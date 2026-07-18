from enum import Enum

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


