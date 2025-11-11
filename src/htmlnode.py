from enum import Enum

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



  
