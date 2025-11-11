
import unittest 

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_init(self):
      # Test default initialization
      obj = HTMLNode()
      assert obj.tag is None
      assert obj.value is None
      assert obj.children is None
      assert obj.props is None

      # Test initialization with values
      props = {"class": "my-class", "id": "my-id"}
      children = ["child1", "child2"]
      obj = HTMLNode(tag="div", value="content", children=children, props=props)
      assert obj.tag == "div"
      assert obj.value == "content"
      assert obj.children == children
      assert obj.props == props


  def test_props_to_html(self):
      # When props is None or empty, should return empty string
      obj = HTMLNode()
      assert obj.props_to_html() == ""

      obj = HTMLNode(props={})
      assert obj.props_to_html() == ""

      # When props has items, should return formatted string
      props = {"class": "my-class", "id": "my-id"}
      obj = HTMLNode(props=props)
      result = obj.props_to_html()
      # The order of items in dict is preserved in Python 3.7+, so we can check exact string
      assert result == ' class="my-class" id="my-id"'

      # Also test with different props
      props = {"data-test": "value", "style": "color:red;"}
      obj = HTMLNode(props=props)
      result = obj.props_to_html()
      assert result == ' data-test="value" style="color:red;"'

  def test_repr(self):
      # Test __repr__ with all attributes set
      props = {"class": "my-class"}
      children = ["child1", "child2"]
      node = HTMLNode(tag="div", value="content", children=children, props=props)
      expected = f"HTMLNode(div, content, {children}, {props})"
      assert repr(node) == expected

      # Test __repr__ with default None attributes
      node = HTMLNode()
      expected = "HTMLNode(None, None, None, None)"
      assert repr(node) == expected

if __name__ == "__main__":
  unittest.main()

