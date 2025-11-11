
import unittest 

from htmlnode import HTMLNode, LeafNode

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

  def test_leaf_to_html_p(self):
      node = LeafNode("p", "Hello, world!")
      assert node.to_html() == "<p>Hello, world!</p>"

  def test_leaf_to_html_span_with_props(self):
      node = LeafNode("span", "Text", props={"class": "highlight"})
      assert node.to_html() == '<span class="highlight">Text</span>'

  def test_leaf_to_html_code_tag(self):
      node = LeafNode("code", "print('Hello')")
      assert node.to_html() == "<code>print('Hello')</code>"

  def test_leaf_to_html_without_tag(self):
      node = LeafNode(None, "Just text")
      assert node.to_html() == "Just text"

  def test_leaf_to_html_empty_value_raises(self):
      node = LeafNode("p", None)
      try:
          node.to_html()
      except ValueError:
          pass  # Test passes if ValueError is raised
      else:
          assert False, "ValueError was not raised when value is empty"
      
  def test_leaf_to_html_img_tag_self_closing(self):
      node = LeafNode("img", "", props={"src": "image.png", "alt": "An image"})
      assert node.to_html() == '<img src="image.png" alt="An image"/>'

  def test_leaf_to_html_link_tag(self):
      node = LeafNode("a", "Click here", props={"href": "https://example.com"})
      assert node.to_html() == '<a href="https://example.com">Click here</a>'

if __name__ == "__main__":
  unittest.main()

