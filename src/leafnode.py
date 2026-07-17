from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value

        formatted_props = super().props_to_html()
        return f"<{self.tag}{" " + formatted_props if formatted_props else ""}>{self.value}</{self.tag}>"

    def __repr__(self):
        super.__repr__()

