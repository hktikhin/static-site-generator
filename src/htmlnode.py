from enum import Enum
from textnode import TextType

class HTMLNodeType(Enum):
  pass


class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag 
    self.value = value 
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError
  
  def props_to_html(self):
    if not self.props:
      return ""
    
    return "".join([f' {k}="{v}"' for k, v in self.props.items()])

  def __eq__(self, other):
    if ((self.tag is None) != (other.tag is None) or
      (self.value is None) != (other.value is None) or 
      (self.children is None) != (other.children is None) or
      (self.props is None) != (other.props is None)):
      return False
    return (
            (self.tag == other.tag if self.tag is not None else True) and
            (self.value == other.value if self.value is not None else True) and
            (self.children == other.children if self.children is not None else True) and 
            (self.props == other.props if self.props is not None else True)
          )
  
  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("All leaf nodes must have a value.")

    if not self.tag: 
      return self.value 

    if self.tag == "img":
      return f'<{self.tag}{self.props_to_html()}/>'

    return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if not self.tag: 
      raise ValueError("All parent nodes must have a tag.")
    
    if not self.children: 
      raise ValueError("All parent nodes must have the children.")

    if self.tag == "img":
      raise ValueError("The parent nodes cannot have an img tag.")
      
    return f'<{self.tag}{self.props_to_html()}>{"".join([child.to_html() for child in self.children])}</{self.tag}>'

def text_node_to_html_node(text_node):
    match text_node.text_type:
      case TextType.TEXT:
          return LeafNode(tag=None, value=text_node.text)
      case TextType.BOLD:
          return LeafNode(tag="b", value=text_node.text)
      case TextType.ITALIC:
          return LeafNode(tag="i", value=text_node.text)
      case TextType.CODE:
          return LeafNode(tag="code", value=text_node.text)
      case TextType.LINK:
          return LeafNode(tag="a", value=text_node.text)
      case TextType.IMAGE:
          return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
      case _:
          raise ValueError("The text node have a unsupported type.")

  
