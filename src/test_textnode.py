import unittest
from textnode import TextNode, TextType, text_node_to_html_node
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

if __name__ == "__main__":
    unittest.main()