import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()