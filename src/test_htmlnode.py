import unittest
from htmlnode import HTMLNode, LeafNode


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

