import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_contains_tags_and_children(self):
        node = HTMLNode(
            tag="p",
            value="Hola mundo",
            children=[
                HTMLNode("img", "crazy image", [HTMLNode(value="Papoi")], props={"src": "assets/img.jpg"})
            ],
            props={"href": "https://www.google.com"}
        )
        result = repr(node)

        self.assertIn("<p", result)
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn("Hola mundo", result)
        self.assertIn("<img", result)
        self.assertIn('src="assets/img.jpg"', result)
        self.assertIn("Papoi", result)
        self.assertIn("</p>", result)

    def test_repr_no_children(self):
        node = HTMLNode(tag="p", value="Hola mundo 2", props={"target": "_blank"})
        result = repr(node)

        self.assertIn('<p', result)
        self.assertIn('target="_blank"', result)
        self.assertIn('>Hola mundo 2</p>', result)

    def test_props_to_html_contains_all_props(self):
        node = HTMLNode(props={
            "src": "papoi.jpg",
            "href": "https://wikipedia.org"
        })
        result = node.props_to_html()

        self.assertIn('src="papoi.jpg"', result)
        self.assertIn('href="https://wikipedia.org"', result)

    def test_props_to_html_empty_props_returns_empty_string(self):
        node = HTMLNode(tag="p", value="no props")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none_props_returns_empty_string(self):
        node = HTMLNode(tag="p", value="no props", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop_exact(self):
        node = HTMLNode(props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), 'href="https://boot.dev"')

    def test_props_to_html_multiple_props_space_separated(self):
        node = HTMLNode(props={"a": "1", "b": "2", "c": "3"})
        self.assertEqual(node.props_to_html(), 'a="1" b="2" c="3"')

    def test_defaults_props_is_empty_dict(self):
        node = HTMLNode()
        self.assertEqual(node.props, {})

    def test_defaults_children_is_empty_list(self):
        node = HTMLNode()
        self.assertEqual(node.children, [])

    def test_defaults_tag_and_value_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)

    def test_constructor_stores_all_attributes(self):
        child = HTMLNode(value="child")
        node = HTMLNode(
            tag="a",
            value="link",
            children=[child],
            props={"href": "https://boot.dev"},
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "link")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {"href": "https://boot.dev"})

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode(tag="p", value="Hola")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_bare_value_only_node(self):
        node = HTMLNode(value="just text")
        self.assertEqual(repr(node), "just text")

    def test_repr_no_props_no_children(self):
        node = HTMLNode(tag="span", value="content")
        self.assertEqual(repr(node), "<span>content</span>")

    def test_repr_tag_without_value(self):
        node = HTMLNode(tag="br")
        self.assertEqual(repr(node), "<br></br>")

    def test_repr_children_are_included(self):
        child_one = HTMLNode(tag="li", value="one")
        child_two = HTMLNode(tag="li", value="two")
        node = HTMLNode(tag="ul", children=[child_one, child_two])
        result = repr(node)
        self.assertIn("<ul", result)
        self.assertIn("<li>one</li>", result)
        self.assertIn("<li>two</li>", result)
        self.assertIn("</ul>", result)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        self.assertEqual(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_node_raw(self):
        node =  LeafNode(None, "Tagless leaf :(")
        self.assertEqual(node.to_html(), "Tagless leaf :(")

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode(
            "img",
            "alt text",
            {"src": "img.png", "alt": "alt text"},
        )
        self.assertEqual(
            node.to_html(),
            '<img src="img.png" alt="alt text">alt text</img>',
        )

    def test_leaf_to_html_none_props_no_attributes(self):
        node = LeafNode("h1", "Title", None)
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

    def test_leaf_to_html_empty_props_no_attributes(self):
        node = LeafNode("h1", "Title", {})
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

    def test_leaf_to_html_raises_without_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_raises_with_empty_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_is_htmlnode_subclass(self):
        node = LeafNode("p", "text")
        self.assertIsInstance(node, HTMLNode)

    def test_leaf_has_no_children(self):
        node = LeafNode("p", "text")
        self.assertEqual(node.children, [])


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        parent_node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container"},
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_to_html_raises_without_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_raises_without_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_raises_with_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_is_htmlnode_subclass(self):
        parent_node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsInstance(parent_node, HTMLNode)

    def test_parent_value_is_none(self):
        parent_node = ParentNode("div", [LeafNode("span", "child")])
        self.assertIsNone(parent_node.value)

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("b", "one")]),
                        ParentNode("li", [LeafNode("b", "two")]),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>one</b></li><li><b>two</b></li></ul></div>",
        )

    def test_to_html_mixed_parent_and_leaf_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode(None, "raw "),
                ParentNode("span", [LeafNode("b", "bold")]),
                LeafNode("i", " tail"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div>raw <span><b>bold</b></span><i> tail</i></div>",
        )


if __name__ == "__main__":
    unittest.main()