class HTLMNode():
    def __init__(self, tag = None, value = None, children = None, props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html_string = ""
        for prop in self.props:
            html_string = html_string + " " +f"{prop}=\"{self.props[prop]}\""
        return html_string
    def __repr__(self):
        return f"""tag is: {self. tag} \n
                value is: {self.value} \n
                childrens are: {self.children} \n
                props are: {self.props}
                """
class LeafNode(HTLMNode):
    def __init__(self, tag=None, value=None, props=None):
        if value == None:
            raise ValueError("Value is required")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag == None:
            return self.value
        return "<" + self.tag + self.props_to_html() + ">" + self.value + f"</{self.tag}>"
    
    def __repr__(self):
        return f"""tag is: {self. tag} \n
                value is: {self.value} \n
                props are: {self.props}
                """
class ParentNode(HTLMNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag == None:
            raise ValueError("Tag is not optional!")
        if children == None:
            raise ValueError("Parent node have to have children!")
        super().__init__(tag, None, children, props)
    def to_html(self):
        string = "<" + self.tag + self.props_to_html() + ">"
        for child in self.children:
            string =  string + child.to_html()
        return string + f"</{self.tag}>"
   
    def __repr__(self):
        return f"""tag is: {self. tag} \n
                childrens are: {self.children} \n
                props are: {self.props}
                """
