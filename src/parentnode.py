from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        if not props:
            props = {}
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        formatted_props = super().props_to_html()
        return f"<{self.tag}{" " + formatted_props if formatted_props else ""}>{"".join(child.to_html() for child in self.children)}</{self.tag}>"