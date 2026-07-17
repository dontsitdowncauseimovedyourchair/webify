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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        self.assertEqual(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_node_raw(self):
        node =  LeafNode(None, "Tagless leaf :(")
        self.assertEqual(node.to_html(), "Tagless leaf :(")


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