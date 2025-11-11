
import unittest 
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType 
from splitter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
  def test_split_nodes_delimiter_basic_split(self):
      node = TextNode("This is text with a `code block` word", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
      assert len(new_nodes) == 3
      assert new_nodes[0].text == "This is text with a "
      assert new_nodes[0].text_type == TextType.TEXT
      assert new_nodes[1].text == "code block"
      assert new_nodes[1].text_type == TextType.CODE
      assert new_nodes[2].text == " word"
      assert new_nodes[2].text_type == TextType.TEXT

  def test_split_nodes_delimiter_no_delimiter(self):
      node = TextNode("This text has no code block", TextType.TEXT)
      new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
      # Should return the original node unchanged
      assert len(new_nodes) == 1
      assert new_nodes[0].text == "This text has no code block"
      assert new_nodes[0].text_type == TextType.TEXT

  def test_split_nodes_delimiter_unmatched_delimiter_raises(self):
      node = TextNode("This is text with an `unmatched code block", TextType.TEXT)
      try:
          split_nodes_delimiter([node], "`", TextType.CODE)
      except ValueError as e:
          assert str(e) == "A matching closing delimiter is not found"
      else:
          assert False, "ValueError not raised for unmatched delimiter"

  def test_extract_markdown_images(self):
      matches = extract_markdown_images(
          "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
      )
      self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
      
  def test_extract_markdown_images_basic(self):
      text = "Here is an image ![alt text](http://example.com/image.png)"
      result = extract_markdown_images(text)
      assert result == [("alt text", "http://example.com/image.png")]

  def test_extract_markdown_images_no_alt_text(self):
      text = "Image without alt text ![](http://example.com/image.png)"
      result = extract_markdown_images(text)
      assert result == [("", "http://example.com/image.png")]

  def test_extract_markdown_images_multiple_images(self):
      text = "First ![img1](http://example.com/1.png) and second ![img2](http://example.com/2.png)"
      result = extract_markdown_images(text)
      assert result == [("img1", "http://example.com/1.png"), ("img2", "http://example.com/2.png")]

  def test_extract_markdown_images_no_images(self):
      text = "This text has no images."
      result = extract_markdown_images(text)
      assert result == []

  def test_extract_markdown_links_basic(self):
      text = "Here is a [link](http://example.com)"
      result = extract_markdown_links(text)
      assert result == [("link", "http://example.com")]

  def test_extract_markdown_links_multiple_links(self):
      text = "Links: [Google](https://google.com), [Bing](https://bing.com)"
      result = extract_markdown_links(text)
      assert result == [("Google", "https://google.com"), ("Bing", "https://bing.com")]

  def test_extract_markdown_links_no_links(self):
      text = "No links here!"
      result = extract_markdown_links(text)
      assert result == []

  def test_extract_markdown_links_empty_text(self):
      text = "Empty []() link"
      result = extract_markdown_links(text)
      assert result == [("", "")]

  def test_extract_markdown_images_nested_brackets_problem(self):
      text = "This is an image with nested brackets ![alt [nested] text](http://example.com/image.png)"
      matches = extract_markdown_images(text)
      # Since Markdown does not support nested brackets in alt text,
      # the regex should not match this invalid syntax, so matches should be empty.
      assert matches == [], "Expected no matches because nested brackets are not supported in Markdown."

  def test_extract_markdown_links_excludes_image_links(self):
      text = "This is an image ![alt text](http://example.com/image.png) and a link [example](http://example.com)"
      matches = extract_markdown_links(text)
      # The link extractor should NOT return the image link
      # It should only return the regular link
      assert ("alt text", "http://example.com/image.png") not in matches, "Image link was incorrectly matched as a regular link"
      assert ("example", "http://example.com") in matches, "Regular link was not matched"

if __name__ == "__main__":
  unittest.main()

