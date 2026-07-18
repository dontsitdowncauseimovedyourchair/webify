from markdown_functions import markdown_to_blocks, block_to_block_type, BlockType
import unittest


class TestMarkdownToBlock(unittest.TestCase):
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

    def test_empty_string_returns_empty_list(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace_returns_empty_list(self):
        self.assertEqual(markdown_to_blocks("   \n\n   "), [])

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("single block"), ["single block"])

    def test_single_block_with_internal_newline_preserved(self):
        self.assertEqual(
            markdown_to_blocks("line1\nline2"),
            ["line1\nline2"],
        )

    def test_multiple_blank_lines_between_blocks_filtered(self):
        # Extra blank lines create empty blocks that must be filtered out.
        self.assertEqual(markdown_to_blocks("a\n\n\n\nb"), ["a", "b"])

    def test_odd_blank_lines_between_blocks(self):
        # Three newlines: split leaves a leading "\n" that strip() removes.
        self.assertEqual(markdown_to_blocks("a\n\n\nb"), ["a", "b"])

    def test_leading_and_trailing_whitespace_stripped(self):
        self.assertEqual(
            markdown_to_blocks("   leading and trailing   "),
            ["leading and trailing"],
        )

    def test_leading_and_trailing_blank_blocks_filtered(self):
        self.assertEqual(
            markdown_to_blocks("\n\nfirst\n\nsecond\n\n"),
            ["first", "second"],
        )

    def test_each_block_is_stripped(self):
        self.assertEqual(
            markdown_to_blocks("  first  \n\n  second  "),
            ["first", "second"],
        )


class TestBlockToBlockType(unittest.TestCase):
    # ---- Headings: 1-6 "#" followed by a space ----
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_all_levels_h1_to_h6(self):
        for level in range(1, 7):
            block = ("#" * level) + " Heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        # 7 "#" is not a valid heading level in markdown.
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_heading_requires_space_after_hash(self):
        # No space after the "#" -> not a heading.
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # ---- Code: fenced with triple backticks ----
    def test_code_block_multiline(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # ---- Quote: every line starts with ">" ----
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> a quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        block = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_partial_is_paragraph(self):
        # Not every line is a quote -> paragraph.
        block = "> line one\nnot a quote line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # ---- Unordered list: every line starts with "- " ----
    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_requires_space_after_dash(self):
        # "-item" without a space is not a list item.
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_unordered_list_partial_is_paragraph(self):
        block = "- one\ntwo"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # ---- Ordered list: lines numbered "1. ", "2. ", ... starting at 1 ----
    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_must_start_at_one(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment_by_one(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_requires_dot_space(self):
        # "1) one" is not the markdown ordered-list form.
        self.assertEqual(block_to_block_type("1) one"), BlockType.PARAGRAPH)

    def test_ordered_list_partial_is_paragraph(self):
        block = "1. one\nnot numbered"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # ---- Paragraph: anything that matches no other type ----
    def test_plain_paragraph(self):
        self.assertEqual(block_to_block_type("just some text"), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        block = "first line\nsecond line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()