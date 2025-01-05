class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        all_props = []
        for prop in self.props:
            hprop = prop +'="' + self.props[prop] + '"'
            all_props.append(hprop)
        return " ".join(all_props)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):        
        if self.value == None:
            raise ValueError("Must have a value parameter")
        if self.tag == None:
            return str(self.value)
        if self.props:
            props = self.props_to_html()
            return f"<{self.tag} {props}>{self.value}</{self.tag}>"        
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, [], children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Must have tag.")
        if not self.children:
            raise ValueError("Must have children")
        children = ""
        for child in self.children:
            children += child.to_html()
        return f"<{self.tag}>{children}</{self.tag}>"