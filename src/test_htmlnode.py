
import unittest
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node
from textnode import TextNode, TextType

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

  def test_to_html_with_children(self):
      child_node = LeafNode("span", "child")
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
      grandchild_node = LeafNode("b", "grandchild")
      child_node = ParentNode("span", [grandchild_node])
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(
          parent_node.to_html(),
          "<div><span><b>grandchild</b></span></div>",
      )

  def test_parentnode_no_tag_raises(self):
      node = ParentNode(tag=None, children=[])
      try:
          node.to_html()
      except ValueError as e:
          assert str(e) == "All parent nodes must have a tag."
      else:
          assert False, "ValueError not raised for missing tag"

  def test_parentnode_no_children_raises(self):
      node = ParentNode(tag="div", children=None)
      try:
          node.to_html()
      except ValueError as e:
          assert str(e) == "All parent nodes must have the children."
      else:
          assert False, "ValueError not raised for missing children"

  def test_parentnode_img_tag_raises(self):
      node = ParentNode(tag="img", children=[LeafNode("p", "text")])
      try:
          node.to_html()
      except ValueError as e:
          assert str(e) == "The parent nodes cannot have an img tag."
      else:
          assert False, "ValueError not raised for img tag"

  def test_parentnode_empty_children_list_raises(self):
      node = ParentNode(tag="div", children=[])
      try:
          node.to_html()
      except ValueError as e:
          assert str(e) == "All parent nodes must have the children."
      else:
          assert False, "ValueError not raised for empty children list"

  def test_parentnode_single_child_to_html(self):
      child = LeafNode("p", "Hello")
      node = ParentNode(tag="div", children=[child])
      expected_html = "<div><p>Hello</p></div>"
      assert node.to_html() == expected_html

  def test_parentnode_multiple_children_to_html(self):
      children = [LeafNode("p", "Hello"), LeafNode("span", "World")]
      node = ParentNode(tag="section", children=children)
      expected_html = "<section><p>Hello</p><span>World</span></section>"
      assert node.to_html() == expected_html

  def test_parentnode_nested_parentnodes(self):
      inner_child = LeafNode("em", "italic text")
      inner_parent = ParentNode(tag="span", children=[inner_child])
      outer_parent = ParentNode(tag="div", children=[inner_parent])
      expected_html = "<div><span><em>italic text</em></span></div>"
      assert outer_parent.to_html() == expected_html

  def test_parentnode_with_props(self):
      child = LeafNode("p", "Hello")
      props = {"class": "container", "id": "main"}
      node = ParentNode(tag="div", children=[child], props=props)
      expected_html = '<div class="container" id="main"><p>Hello</p></div>'
      assert node.to_html() == expected_html

  def test_text(self):
      node = TextNode("This is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "This is a text node")

  def test_text_node_to_html_node_text(self):
      node = TextNode("This is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      assert html_node.tag is None
      assert html_node.value == "This is a text node"
      assert html_node.props is None

  def test_text_node_to_html_node_bold(self):
      node = TextNode("Bold text", TextType.BOLD)
      html_node = text_node_to_html_node(node)
      assert html_node.tag == "b"
      assert html_node.value == "Bold text"
      assert html_node.props is None

  def test_text_node_to_html_node_italic(self):
      node = TextNode("Italic text", TextType.ITALIC)
      html_node = text_node_to_html_node(node)
      assert html_node.tag == "i"
      assert html_node.value == "Italic text"
      assert html_node.props is None

  def test_text_node_to_html_node_code(self):
      node = TextNode("print('Hello')", TextType.CODE)
      html_node = text_node_to_html_node(node)
      assert html_node.tag == "code"
      assert html_node.value == "print('Hello')"
      assert html_node.props is None

  def test_text_node_to_html_node_link(self):
      node = TextNode("Click here", TextType.LINK)
      html_node = text_node_to_html_node(node)
      assert html_node.tag == "a"
      assert html_node.value == "Click here"
      assert html_node.props is None

  def test_text_node_to_html_node_image(self):
      node = TextNode("An image", TextType.IMAGE)
      node.url = "http://example.com/image.png"
      html_node = text_node_to_html_node(node)
      assert html_node.tag == "img"
      assert html_node.value == ""
      assert html_node.props == {"src": "http://example.com/image.png", "alt": "An image"}

  def test_text_node_to_html_node_unsupported_type(self):
      class FakeTextType(Enum):
          UNSUPPORTED = 99
      node = TextNode("Unsupported", FakeTextType.UNSUPPORTED)
      try:
          text_node_to_html_node(node)
      except ValueError as e:
          assert str(e) == "The text node have a unsupported type."
      else:
          assert False, "ValueError not raised for unsupported text type"

  def test_paragraphs(self):
      md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
      node = markdown_to_html_node(md)
      html = node.to_html()
      self.assertEqual(
          html,
          "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
      )

  def test_codeblock(self):
      md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

      node = markdown_to_html_node(md)
      html = node.to_html()
      self.assertEqual(
          html,
          "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
      )

  def test_heading(self):
      md = "# Heading level 1\n\n## Heading level 2\n\n### Heading level 3"
      node = markdown_to_html_node(md)
      html = node.to_html()
      print(repr(html))
      expected_html = "".join([f"<h{i}>Heading level {i}</h{i}>" for i in range(1, 4)])
      self.assertEqual(html, f"<div>{expected_html}</div>")

  def test_quote_block(self):
      md = "> This is a quote line 1\n> This is a quote line 2"
      node = markdown_to_html_node(md)
      html = node.to_html()
      expected_html = "<div><q>This is a quote line 1\nThis is a quote line 2</q></div>"
      self.assertEqual(html, expected_html)

  def test_unordered_list(self):
      md = "- item 1\n- item 2\n- item 3"
      node = markdown_to_html_node(md)
      html = node.to_html()
      expected_html = "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>"
      self.assertEqual(html, expected_html)

  def test_ordered_list(self):
      md = "1. first item\n2. second item\n3. third item"
      node = markdown_to_html_node(md)
      html = node.to_html()
      expected_html = "<div><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>"
      self.assertEqual(html, expected_html)

if __name__ == "__main__":
  unittest.main()

