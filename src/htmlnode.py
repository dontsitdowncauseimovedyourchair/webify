class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list=None, props: dict=None):
        if props is None:
            props = {}
        if children is None:
            children = []
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        out = []
        for key, value in self.props.items():
            out.append(f"{key}=\"{value}\"")
        return " ".join(out)

    def __repr__(self):
        format_props = self.props_to_html()
        if not self.tag and not self.children and not self.props:
            return f"{self.value}"

        if self.children:
            return f"""
            <{self.tag if self.tag else ""}{" " + format_props if format_props else ""}>{self.value if self.value else ""}
              {"  \n".join(list(map(lambda x: x.__repr__(), self.children)))}
            </{self.tag if self.tag else ""}>
            """
        else:
            return f"<{self.tag if self.tag else ""}{" " + format_props if format_props else ""}>{self.value if self.value else ""}</{self.tag if self.tag else ""}>"