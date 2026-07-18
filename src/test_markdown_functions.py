from markdown_functions import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_raw_lines, \
    block_to_html_node, markdown_to_html_node
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


class TestMarkdownToRawText(unittest.TestCase):
    # ---- Paragraph: no markers, text returned unchanged, one entry per line ----
    def test_paragraph_single_line(self):
        self.assertEqual(
            markdown_to_raw_lines("just some text", BlockType.PARAGRAPH),
            ["just some text"],
        )

    def test_paragraph_multiline(self):
        self.assertEqual(
            markdown_to_raw_lines("line one\nline two", BlockType.PARAGRAPH),
            ["line one", "line two"],
        )

    # ---- Heading: strip the leading "#"s and the following space ----
    def test_heading_h1(self):
        self.assertEqual(
            markdown_to_raw_lines("# Heading", BlockType.HEADING),
            ["Heading"],
        )

    def test_heading_h6(self):
        self.assertEqual(
            markdown_to_raw_lines("###### Deep heading", BlockType.HEADING),
            ["Deep heading"],
        )

    def test_heading_keeps_inner_hash(self):
        # Only the leading marker is stripped; a "#" inside the text stays.
        self.assertEqual(
            markdown_to_raw_lines("## C# notes", BlockType.HEADING),
            ["C# notes"],
        )

    # ---- Quote: strip the leading ">" (and the optional following space) ----
    def test_quote_single_line_with_space(self):
        self.assertEqual(
            markdown_to_raw_lines("> a quote", BlockType.QUOTE),
            ["a quote"],
        )

    def test_quote_single_line_no_space(self):
        self.assertEqual(
            markdown_to_raw_lines(">a quote", BlockType.QUOTE),
            ["a quote"],
        )

    def test_quote_multiline(self):
        self.assertEqual(
            markdown_to_raw_lines("> line one\n> line two", BlockType.QUOTE),
            ["line one", "line two"],
        )

    # ---- Code: strip the opening/closing triple-backtick fences ----
    def test_code_single_line(self):
        self.assertEqual(
            markdown_to_raw_lines("```\ncode\n```", BlockType.CODE),
            ["code"],
        )

    def test_code_multiline(self):
        self.assertEqual(
            markdown_to_raw_lines("```\nline 1\nline 2\n```", BlockType.CODE),
            ["line 1", "line 2"],
        )

    # ---- Unordered list: strip the leading "- " from every line ----
    def test_unordered_list_single_item(self):
        self.assertEqual(
            markdown_to_raw_lines("- item", BlockType.UNORDERED_LIST),
            ["item"],
        )

    def test_unordered_list_multiple_items(self):
        self.assertEqual(
            markdown_to_raw_lines("- one\n- two\n- three", BlockType.UNORDERED_LIST),
            ["one", "two", "three"],
        )

    # ---- Ordered list: strip the leading "N. " from every line ----
    def test_ordered_list_single_item(self):
        self.assertEqual(
            markdown_to_raw_lines("1. item", BlockType.ORDERED_LIST),
            ["item"],
        )

    def test_ordered_list_multiple_items(self):
        self.assertEqual(
            markdown_to_raw_lines("1. one\n2. two\n3. three", BlockType.ORDERED_LIST),
            ["one", "two", "three"],
        )

    def test_ordered_list_double_digit(self):
        # The "10. " marker is 4 chars, so a fixed 3-char strip is not enough.
        block = "\n".join(f"{i}. item{i}" for i in range(1, 11))
        expected = [f"item{i}" for i in range(1, 11)]
        self.assertEqual(
            markdown_to_raw_lines(block, BlockType.ORDERED_LIST),
            expected,
        )


class TestBlockToHtmlNode(unittest.TestCase):
    # ---- Paragraph -> <p>...</p> with inline markdown parsed ----
    def test_paragraph_plain(self):
        node = block_to_html_node("just some text", BlockType.PARAGRAPH)
        self.assertEqual(node.to_html(), "<p>just some text</p>")

    def test_paragraph_with_inline_formatting(self):
        node = block_to_html_node("hello **world** and _you_", BlockType.PARAGRAPH)
        self.assertEqual(
            node.to_html(),
            "<p>hello <b>world</b> and <i>you</i></p>",
        )

    # ---- Heading -> <h1>..<h6> depending on the number of "#" ----
    def test_heading_h1(self):
        node = block_to_html_node("# Title", BlockType.HEADING)
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

    def test_heading_all_levels(self):
        for level in range(1, 7):
            block = ("#" * level) + " Title"
            node = block_to_html_node(block, BlockType.HEADING)
            self.assertEqual(node.to_html(), f"<h{level}>Title</h{level}>")

    def test_heading_with_inline_formatting(self):
        node = block_to_html_node("## Sub _title_", BlockType.HEADING)
        self.assertEqual(node.to_html(), "<h2>Sub <i>title</i></h2>")

    # ---- Quote -> <blockquote>...</blockquote>, marker stripped on every line ----
    def test_quote_single_line_tag_is_blockquote(self):
        node = block_to_html_node("> be brave", BlockType.QUOTE)
        self.assertEqual(node.to_html(), "<blockquote>be brave</blockquote>")

    def test_quote_multiline_strips_every_marker(self):
        node = block_to_html_node("> line one\n> line two", BlockType.QUOTE)
        self.assertEqual(node.tag, "blockquote")
        html = node.to_html()
        # Every line's ">" marker must be gone, not just the first line's.
        self.assertNotIn("> line two", html)
        self.assertIn("line one", html)
        self.assertIn("line two", html)

    # ---- Code -> <pre><code>...</code></pre>, fences removed, NO inline parsing ----
    def test_code_wraps_in_pre_code_and_strips_fences(self):
        node = block_to_html_node("```\nprint(1)\n```", BlockType.CODE)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(node.children[0].tag, "code")
        html = node.to_html()
        self.assertNotIn("`", html)          # triple-backtick fences stripped
        self.assertIn("print(1)", html)

    def test_code_does_not_apply_inline_formatting(self):
        node = block_to_html_node("```\nx = **not bold**\n```", BlockType.CODE)
        html = node.to_html()
        self.assertIn("**not bold**", html)  # literal, not converted
        self.assertNotIn("<b>", html)
        self.assertNotIn("`", html)          # fences stripped

    # ---- Unordered list -> <ul><li>..</li>..</ul>, "- " stripped on every line ----
    def test_unordered_list(self):
        node = block_to_html_node("- one\n- two\n- three", BlockType.UNORDERED_LIST)
        self.assertEqual(
            node.to_html(),
            "<ul><li>one</li><li>two</li><li>three</li></ul>",
        )

    def test_unordered_list_with_inline_formatting(self):
        node = block_to_html_node("- **a**\n- b", BlockType.UNORDERED_LIST)
        self.assertEqual(node.to_html(), "<ul><li><b>a</b></li><li>b</li></ul>")

    # ---- Ordered list -> <ol><li>..</li>..</ol>, "N. " stripped on every line ----
    def test_ordered_list(self):
        node = block_to_html_node("1. one\n2. two\n3. three", BlockType.ORDERED_LIST)
        self.assertEqual(
            node.to_html(),
            "<ol><li>one</li><li>two</li><li>three</li></ol>",
        )

    def test_ordered_list_with_inline_formatting(self):
        node = block_to_html_node("1. **a**\n2. b", BlockType.ORDERED_LIST)
        self.assertEqual(node.to_html(), "<ol><li><b>a</b></li><li>b</li></ol>")

    # ================= MULTILINE / EDGE CASES =================

    # ---- Paragraph ----
    def test_paragraph_multiline(self):
        # A paragraph block can span several source lines.
        node = block_to_html_node("first line\nsecond line", BlockType.PARAGRAPH)
        self.assertEqual(node.tag, "p")
        html = node.to_html()
        self.assertIn("first line", html)
        self.assertIn("second line", html)

    def test_paragraph_multiline_with_inline_across_lines(self):
        node = block_to_html_node("a **bold** here\nand _italic_ there", BlockType.PARAGRAPH)
        html = node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)

    def test_paragraph_with_link(self):
        node = block_to_html_node("see [boot](https://boot.dev) now", BlockType.PARAGRAPH)
        self.assertEqual(
            node.to_html(),
            '<p>see <a href="https://boot.dev">boot</a> now</p>',
        )

    # ---- Quote ----
    def test_quote_multiline_with_inline_formatting(self):
        node = block_to_html_node("> be **bold**\n> stay _true_", BlockType.QUOTE)
        self.assertEqual(node.tag, "blockquote")
        html = node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>true</i>", html)
        self.assertNotIn("> ", html)  # no leaked markers on any line

    def test_quote_no_space_after_marker(self):
        node = block_to_html_node(">tight", BlockType.QUOTE)
        self.assertEqual(node.to_html(), "<blockquote>tight</blockquote>")

    def test_quote_three_lines(self):
        node = block_to_html_node("> a\n> b\n> c", BlockType.QUOTE)
        self.assertEqual(node.tag, "blockquote")
        html = node.to_html()
        for letter in ("a", "b", "c"):
            self.assertIn(letter, html)
        # No leaked ">" markers: inspect the text between the tags only.
        inner = html[len("<blockquote>"):-len("</blockquote>")]
        self.assertNotIn(">", inner)

    # ---- Code ----
    def test_code_multiline_preserves_newlines(self):
        node = block_to_html_node("```\nline 1\nline 2\n```", BlockType.CODE)
        self.assertEqual(node.tag, "pre")
        self.assertEqual(node.children[0].tag, "code")
        html = node.to_html()
        self.assertNotIn("`", html)
        self.assertIn("line 1\nline 2", html)  # line breaks preserved

    def test_code_multiline_no_inline_parsing(self):
        node = block_to_html_node("```\na = **x**\nb = _y_\n```", BlockType.CODE)
        html = node.to_html()
        self.assertIn("**x**", html)
        self.assertIn("_y_", html)
        self.assertNotIn("<b>", html)
        self.assertNotIn("<i>", html)
        self.assertNotIn("`", html)

    def test_code_with_language_tag_on_fence(self):
        # An opening fence with a language hint is still just a fence to strip.
        node = block_to_html_node("```python\nprint(1)\n```", BlockType.CODE)
        html = node.to_html()
        self.assertNotIn("`", html)
        self.assertNotIn("python", html)
        self.assertIn("print(1)", html)

    # ---- Unordered list ----
    def test_unordered_list_single_item(self):
        node = block_to_html_node("- only", BlockType.UNORDERED_LIST)
        self.assertEqual(node.to_html(), "<ul><li>only</li></ul>")

    def test_unordered_list_four_items(self):
        node = block_to_html_node("- a\n- b\n- c\n- d", BlockType.UNORDERED_LIST)
        self.assertEqual(
            node.to_html(),
            "<ul><li>a</li><li>b</li><li>c</li><li>d</li></ul>",
        )

    def test_unordered_list_inline_on_every_line(self):
        node = block_to_html_node("- **a**\n- _b_\n- `c`", BlockType.UNORDERED_LIST)
        self.assertEqual(
            node.to_html(),
            "<ul><li><b>a</b></li><li><i>b</i></li><li><code>c</code></li></ul>",
        )

    def test_unordered_list_item_with_link(self):
        node = block_to_html_node("- see [x](https://a.com)\n- plain", BlockType.UNORDERED_LIST)
        self.assertEqual(
            node.to_html(),
            '<ul><li>see <a href="https://a.com">x</a></li><li>plain</li></ul>',
        )

    # ---- Ordered list ----
    def test_ordered_list_single_item(self):
        node = block_to_html_node("1. only", BlockType.ORDERED_LIST)
        self.assertEqual(node.to_html(), "<ol><li>only</li></ol>")

    def test_ordered_list_double_digit(self):
        # Items 10+ have a 4-char "10. " marker that must be fully stripped.
        block = "\n".join(f"{i}. item{i}" for i in range(1, 13))
        expected = "<ol>" + "".join(f"<li>item{i}</li>" for i in range(1, 13)) + "</ol>"
        self.assertEqual(block_to_html_node(block, BlockType.ORDERED_LIST).to_html(), expected)

    def test_ordered_list_inline_on_every_line(self):
        node = block_to_html_node("1. **a**\n2. _b_\n3. `c`", BlockType.ORDERED_LIST)
        self.assertEqual(
            node.to_html(),
            "<ol><li><b>a</b></li><li><i>b</i></li><li><code>c</code></li></ol>",
        )

class TestMarkdownToHTMLNode(unittest.TestCase):
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
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_single_paragraph(self):
        node = markdown_to_html_node("just text")
        self.assertEqual(node.to_html(), "<div><p>just text</p></div>")

    def test_root_is_a_div(self):
        node = markdown_to_html_node("hello")
        self.assertEqual(node.tag, "div")

    def test_empty_markdown_yields_childless_div(self):
        # No blocks -> a div with no children (to_html() would raise, so
        # inspect the structure instead).
        node = markdown_to_html_node("")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [])

    def test_headings_all_levels(self):
        md = "# H1\n\n## H2\n\n### H3\n\n#### H4\n\n##### H5\n\n###### H6"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3><h4>H4</h4><h5>H5</h5><h6>H6</h6></div>",
        )

    def test_heading_with_inline_formatting(self):
        node = markdown_to_html_node("## A **bold** heading")
        self.assertEqual(
            node.to_html(),
            "<div><h2>A <b>bold</b> heading</h2></div>",
        )

    def test_quote_multiline(self):
        node = markdown_to_html_node("> a quote\n> second line")
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>a quote\nsecond line</blockquote></div>",
        )

    def test_unordered_list(self):
        node = markdown_to_html_node("- one\n- two\n- three")
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )

    def test_ordered_list(self):
        node = markdown_to_html_node("1. one\n2. two\n3. three")
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )

    def test_unordered_list_with_inline_formatting(self):
        node = markdown_to_html_node("- **a**\n- _b_\n- `c`")
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>a</b></li><li><i>b</i></li><li><code>c</code></li></ul></div>",
        )

    def test_multiple_blocks_kept_separate(self):
        md = "First paragraph\n\nSecond paragraph"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p></div>",
        )

    def test_blank_lines_between_blocks_do_not_create_empty_nodes(self):
        # Extra blank lines should be collapsed away, not turned into empty <p>.
        md = "one\n\n\n\ntwo"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>one</p><p>two</p></div>",
        )

    def test_full_document_mixed_blocks_in_order(self):
        md = """# Title

This is a paragraph with **bold** and _italic_ and a [link](https://boot.dev).

- first item
- second item

1. step one
2. step two

> a wise quote

```
code stays _literal_
```"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            '<p>This is a paragraph with <b>bold</b> and <i>italic</i> and a <a href="https://boot.dev">link</a>.</p>'
            "<ul><li>first item</li><li>second item</li></ul>"
            "<ol><li>step one</li><li>step two</li></ol>"
            "<blockquote>a wise quote</blockquote>"
            "<pre><code>code stays _literal_\n</code></pre>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()