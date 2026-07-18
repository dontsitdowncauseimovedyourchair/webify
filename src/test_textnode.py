import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, \
    extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a cool node", TextType.BOLD, url="https://boot.dev")
        self.assertEqual(node.__repr__(), "TextNode(This is a cool node, **Bold text**, https://boot.dev)")

    def test_no_url(self):
        node = TextNode("HI I AM TESTING, BRO IS TESTING", TextType.CODE)
        self.assertIsNone(node.url)

    def test_eq_with_matching_urls(self):
        node = TextNode("link", TextType.LINK, url="https://boot.dev")
        node2 = TextNode("link", TextType.LINK, url="https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("first", TextType.TEXT)
        node2 = TextNode("second", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("link", TextType.LINK, url="https://boot.dev")
        node2 = TextNode("link", TextType.LINK, url="https://google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_vs_none(self):
        node = TextNode("link", TextType.LINK, url="https://boot.dev")
        node2 = TextNode("link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_both_urls_none(self):
        node = TextNode("plain", TextType.TEXT)
        node2 = TextNode("plain", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_default_url_is_none(self):
        node = TextNode("text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_constructor_stores_attributes(self):
        node = TextNode("hi", TextType.BOLD, url="https://boot.dev")
        self.assertEqual(node.text, "hi")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.url, "https://boot.dev")

    def test_repr_with_none_url(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(plain text, text, None)")

    def test_repr_uses_text_type_value(self):
        node = TextNode("code snippet", TextType.CODE)
        self.assertEqual(repr(node), "TextNode(code snippet, `Code text`, None)")

    def test_text_type_enum_values(self):
        self.assertEqual(TextType.TEXT.value, "text")
        self.assertEqual(TextType.BOLD.value, "**Bold text**")
        self.assertEqual(TextType.ITALIC.value, "_Italic text_")
        self.assertEqual(TextType.CODE.value, "`Code text`")
        self.assertEqual(TextType.LINK.value, "[anchor text](url)")
        self.assertEqual(TextType.IMAGE.value, "![alt text](url)")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")
        self.assertEqual(html_node.props, {})

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")
        self.assertEqual(html_node.props, {})

    def test_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")
        self.assertEqual(html_node.props, {})

    def test_link(self):
        node = TextNode("anchor text", TextType.LINK, url="https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor text")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, url="https://boot.dev/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://boot.dev/img.png", "alt": "alt text"},
        )

    def test_text_to_html_produces_leafnode(self):
        node = TextNode("plain", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)

    def test_invalid_text_type_raises(self):
        node = TextNode("oops", TextType.TEXT)
        node.text_type = "not a real type"
        with self.assertRaises(AttributeError):
            text_node_to_html_node(node)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_code_in_middle(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_bold_in_middle(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_italic_in_middle(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_delimiter_pairs(self):
        node = TextNode("a `b` c `d` e", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.TEXT),
        ])

    def test_non_text_node_passes_through_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("say `hi`", TextType.TEXT),
            TextNode("stay bold", TextType.BOLD),
            TextNode("and `bye`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("say ", TextType.TEXT),
            TextNode("hi", TextType.CODE),
            TextNode("stay bold", TextType.BOLD),
            TextNode("and ", TextType.TEXT),
            TextNode("bye", TextType.CODE),
        ])

    def test_plain_text_with_no_delimiter_unchanged(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("just plain text", TextType.TEXT)])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("this is `broken", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestExtractMDImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_single_image(self):
        matches = extract_markdown_images("![alt text](https://boot.dev/img.png)")
        self.assertListEqual([("alt text", "https://boot.dev/img.png")], matches)

    def test_multiple_images(self):
        text = "![one](https://a.com/1.png) and ![two](https://b.com/2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("one", "https://a.com/1.png"), ("two", "https://b.com/2.png")],
            matches,
        )

    def test_no_images_returns_empty(self):
        self.assertListEqual([], extract_markdown_images("no images here"))

    def test_image_extraction_ignores_links(self):
        # A plain link (no leading "!") must NOT be picked up as an image.
        matches = extract_markdown_images("a [link](https://boot.dev) here")
        self.assertListEqual([], matches)

    def test_image_among_links(self):
        text = "![img](https://a.com/i.png) and [link](https://b.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("img", "https://a.com/i.png")], matches)

    def test_image_empty_alt_and_url(self):
        # Both capture groups allow zero characters.
        matches = extract_markdown_images("![](  )")
        self.assertListEqual([("", "  ")], matches)

    def test_image_url_with_parens_not_matched(self):
        # A "(" inside the url terminates the url group, so it fails to match.
        matches = extract_markdown_images("![x](https://en.wikipedia.org/(y))")
        self.assertListEqual([], matches)

    def test_adjacent_images(self):
        matches = extract_markdown_images("![a](1)![b](2)")
        self.assertListEqual([("a", "1"), ("b", "2")], matches)


class TestExtractMDLinks(unittest.TestCase):
    def test_single_link(self):
        matches = extract_markdown_links("This is a [link](https://boot.dev) here")
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_multiple_links(self):
        text = "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com"),
            ],
            matches,
        )

    def test_no_links_returns_empty(self):
        self.assertListEqual([], extract_markdown_links("no links here"))

    def test_link_extraction_ignores_images(self):
        # An image (leading "!") must NOT be picked up as a link.
        matches = extract_markdown_links("an ![image](https://a.com/i.png) here")
        self.assertListEqual([], matches)

    def test_link_among_images(self):
        text = "![img](https://a.com/i.png) and [link](https://b.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://b.com")], matches)

    def test_link_empty_anchor_and_url(self):
        matches = extract_markdown_links("[]()")
        self.assertListEqual([("", "")], matches)

    def test_link_url_with_parens_not_matched(self):
        matches = extract_markdown_links("[wiki](https://en.wikipedia.org/(y))")
        self.assertListEqual([], matches)

    def test_adjacent_links(self):
        matches = extract_markdown_links("[a](1)[b](2)")
        self.assertListEqual([("a", "1"), ("b", "2")], matches)

    def test_bang_then_space_before_bracket_is_a_link(self):
        # The "!" is not immediately before "[", so the lookbehind allows a match.
        matches = extract_markdown_links("! [x](y)")
        self.assertListEqual([("x", "y")], matches)

class TestSplitImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_single_image_in_middle(self):
        node = TextNode("text ![img](https://a.com/i.png) end", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
                TextNode(" end", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_image_at_start(self):
        node = TextNode("![img](https://a.com/i.png) tail", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
                TextNode(" tail", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_image_at_end_no_trailing_text(self):
        node = TextNode("lead ![img](https://a.com/i.png)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("lead ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
            ],
            split_nodes_image([node]),
        )

    def test_only_image_no_surrounding_text(self):
        node = TextNode("![img](https://a.com/i.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("img", TextType.IMAGE, "https://a.com/i.png")],
            split_nodes_image([node]),
        )

    def test_no_images_returns_plain_text_node(self):
        node = TextNode("just plain text", TextType.TEXT)
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            split_nodes_image([node]),
        )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("a ![x](1) b", TextType.TEXT),
            TextNode("no image here", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("x", TextType.IMAGE, "1"),
                TextNode(" b", TextType.TEXT),
                TextNode("no image here", TextType.TEXT),
            ],
            split_nodes_image(nodes),
        )


class TestSplitLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is a [link](https://boot.dev) and [second](https://youtube.com)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://youtube.com"),
            ],
            split_nodes_link([node]),
        )

    def test_single_link_in_middle(self):
        node = TextNode("text [l](https://a.com) end", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("l", TextType.LINK, "https://a.com"),
                TextNode(" end", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_link_at_start(self):
        node = TextNode("[l](https://a.com) tail", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("l", TextType.LINK, "https://a.com"),
                TextNode(" tail", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_only_link_no_surrounding_text(self):
        node = TextNode("[l](https://a.com)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("l", TextType.LINK, "https://a.com")],
            split_nodes_link([node]),
        )

    def test_no_links_returns_plain_text_node(self):
        node = TextNode("just plain text", TextType.TEXT)
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            split_nodes_link([node]),
        )

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_text_node_all(self):
        text="This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [
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
        ])

    def test_plain_text_only(self):
        self.assertEqual(
            text_to_textnodes("just plain text"),
            [TextNode("just plain text", TextType.TEXT)],
        )

    def test_empty_string(self):
        # Empty input yields no nodes: the single "" segment is filtered out.
        self.assertEqual(text_to_textnodes(""), [])

    def test_bold_only(self):
        self.assertEqual(
            text_to_textnodes("This is **bold** text"),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_only(self):
        self.assertEqual(
            text_to_textnodes("This is _italic_ text"),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_code_only(self):
        self.assertEqual(
            text_to_textnodes("This is `code` text"),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_image_only(self):
        self.assertEqual(
            text_to_textnodes("![img](https://a.com/i.png)"),
            [TextNode("img", TextType.IMAGE, "https://a.com/i.png")],
        )

    def test_link_only(self):
        self.assertEqual(
            text_to_textnodes("[link](https://boot.dev)"),
            [TextNode("link", TextType.LINK, "https://boot.dev")],
        )

    def test_bold_at_start_no_leading_empty_node(self):
        # A marker at position 0 must NOT produce an empty leading TEXT node.
        self.assertEqual(
            text_to_textnodes("**bold** at start"),
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" at start", TextType.TEXT),
            ],
        )

    def test_bold_at_end_no_trailing_empty_node(self):
        self.assertEqual(
            text_to_textnodes("ends with **bold**"),
            [
                TextNode("ends with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_multiple_of_same_type(self):
        self.assertEqual(
            text_to_textnodes("**a** and **b**"),
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_image_and_link_together(self):
        self.assertEqual(
            text_to_textnodes(
                "![img](https://a.com/i.png) then [link](https://boot.dev)"
            ),
            [
                TextNode("img", TextType.IMAGE, "https://a.com/i.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_all_delimiter_types_together(self):
        self.assertEqual(
            text_to_textnodes("a **b** c _d_ e `f`"),
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" c ", TextType.TEXT),
                TextNode("d", TextType.ITALIC),
                TextNode(" e ", TextType.TEXT),
                TextNode("f", TextType.CODE),
            ],
        )

if __name__ == "__main__":
    unittest.main()