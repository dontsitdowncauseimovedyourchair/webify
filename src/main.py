from textnode import TextNode, TextType


def main():
    node = TextNode("Super interesting text", TextType.text, "https://flop.com")
    print(node)

if __name__ == "__main__":
    main()