
import unittest
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from splitter import (
                      split_nodes_delimiter,
                      extract_markdown_images,
                      extract_markdown_links,
                      split_nodes_image,
                      split_nodes_link,
                      text_to_textnodes,
                      markdown_to_blocks
                    )

from block import BlockType, block_to_block_type


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

  def test_split_nodes_image_multiple_images(self):
      node = TextNode(
          "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
          TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
          [
              TextNode("This is text with an ", TextType.TEXT),
              TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
              TextNode(" and another ", TextType.TEXT),
              TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
          ],
          new_nodes,
      )

  def test_split_nodes_image_no_images(self):
      node = TextNode(
          "This text has no images.",
          TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
          [TextNode("This text has no images.", TextType.TEXT)],
          new_nodes,
      )

  def test_split_nodes_image_non_text_node(self):
      node = TextNode(
          "![image](https://i.imgur.com/zjjcJKZ.png)",
          TextType.IMAGE,
          "https://i.imgur.com/zjjcJKZ.png",
      )
      new_nodes = split_nodes_image([node])
      # Non-text nodes should be returned as-is
      self.assertListEqual(
          [node],
          new_nodes,
      )

  def test_split_nodes_link_multiple_links(self):
    node = TextNode(
        "Here is a [link1](https://example.com/1) and another [link2](https://example.com/2)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
        ],
        new_nodes,
    )


  def test_split_nodes_link_no_links(self):
      node = TextNode(
          "This text has no links.",
          TextType.TEXT,
      )
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
          [TextNode("This text has no links.", TextType.TEXT)],
          new_nodes,
      )


  def test_split_nodes_link_non_text_node(self):
      node = TextNode(
          "link text",
          TextType.LINK,
          "https://example.com",
      )
      new_nodes = split_nodes_link([node])
      # Non-text nodes should be returned as-is
      self.assertListEqual(
          [node],
          new_nodes,
      )

  def test_text_to_textnodes_basic_formatting(self):
      text = "This is **bold** text"
      nodes = text_to_textnodes(text)
      expected = [
          TextNode("This is ", TextType.TEXT),
          TextNode("bold", TextType.BOLD),
          TextNode(" text", TextType.TEXT),
      ]
      self.assertListEqual(expected, nodes)

  def test_text_to_textnodes_all_formats(self):
      text = (
          "This is **text** with an _italic_ word and a `code block` "
          "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
          "and a [link](https://boot.dev)"
      )
      nodes = text_to_textnodes(text)
      expected = [
          TextNode("This is ", TextType.TEXT),
          TextNode("text", TextType.BOLD),
          TextNode(" with an ", TextType.TEXT),
          TextNode("italic", TextType.ITALIC),
          TextNode(" word and a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" and an ", TextType.TEXT),
          TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
          TextNode(" and a ", TextType.TEXT),
          TextNode("link", TextType.LINK, "https://boot.dev"),
      ]
      self.assertListEqual(expected, nodes)

  def test_text_to_textnodes_no_formatting(self):
      text = "Just plain text without any formatting."
      nodes = text_to_textnodes(text)
      expected = [TextNode(text, TextType.TEXT)]
      self.assertListEqual(expected, nodes)

  def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

  def test_markdown_to_blocks_basic(self):
    md = """This is a paragraph.

This is another paragraph."""
    expected = [
        "This is a paragraph.",
        "This is another paragraph."
    ]
    result = markdown_to_blocks(md)
    self.assertEqual(result, expected)

  def test_markdown_to_blocks_with_empty_lines(self):
    md = """Paragraph one.


Paragraph two with extra empty lines.


Paragraph three."""
    expected = [
        "Paragraph one.",
        "Paragraph two with extra empty lines.",
        "Paragraph three."
    ]
    result = markdown_to_blocks(md)
    self.assertEqual(result, expected)

  def test_markdown_to_blocks_with_leading_trailing_spaces(self):
    md = """  Paragraph with leading spaces.

Paragraph with trailing spaces.

  Paragraph with both.  """
    expected = [
        "Paragraph with leading spaces.",
        "Paragraph with trailing spaces.",
        "Paragraph with both."
    ]
    result = markdown_to_blocks(md)
    self.assertEqual(result, expected)

  def test_block_to_block_type_code(self):
      markdown = "```\nprint('Hello, world!')\n```"
      result = block_to_block_type(markdown)
      assert result == BlockType.CODE

  def test_block_to_block_type_heading(self):
      for i in range(1, 7):
          markdown = "#" * i + " Heading level " + str(i)
          result = block_to_block_type(markdown)
          assert result == BlockType.HEADING

  def test_block_to_block_type_quote(self):
      markdown = "> This is a quote line 1\n> This is a quote line 2"
      result = block_to_block_type(markdown)
      assert result == BlockType.QUOTE

  def test_block_to_block_type_unordered_list(self):
      markdown = "- item 1\n- item 2\n- item 3"
      result = block_to_block_type(markdown)
      assert result == BlockType.UNORDERED_LIST

  def test_block_to_block_type_ordered_list(self):
      markdown = "1. first item\n2. second item\n3. third item"
      result = block_to_block_type(markdown)
      assert result == BlockType.ORDERED_LIST

  def test_block_to_block_type_paragraph(self):
      markdown = "This is a normal paragraph without any special markdown."
      result = block_to_block_type(markdown)
      assert result == BlockType.PARAGRAPH

  def test_block_to_block_type_ordered_list_with_wrong_numbering(self):
      markdown = "1. first item\n3. second item\n4. third item"
      result = block_to_block_type(markdown)
      assert result == BlockType.PARAGRAPH

if __name__ == "__main__":
  unittest.main()

