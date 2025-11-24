import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    parts = node.text.split(delimiter)
    if len(parts) % 2 == 0:
      raise ValueError("A matching closing delimiter is not found")

    for idx in range(len(parts)):
      if idx % 2 == 0:
        new_nodes.append(TextNode(parts[idx], TextType.TEXT))
      else:
        new_nodes.append(TextNode(parts[idx], text_type))

  return new_nodes

def extract_markdown_images(text):
  pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

def extract_markdown_links(text):
  pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    img_matches = extract_markdown_images(node.text)
    if not img_matches:
      new_nodes.append(node)
      continue

    current_text = node.text
    for alt_text, url in img_matches:
      parts = current_text.split(f"![{alt_text}]({url})")
      if len(parts)> 0 and parts[0]:
        new_nodes.append(TextNode(parts[0], TextType.TEXT))
      new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
      current_text = parts[1] if len(parts) > 1 else None

    if current_text:
      new_nodes.append(TextNode(current_text, TextType.TEXT))

  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    link_matches = extract_markdown_links(node.text)
    if not link_matches:
      new_nodes.append(node)
      continue

    current_text = node.text
    for text, url in link_matches:
      parts = re.split(fr"(?<!!)\[{text}\]\({url}\)", current_text)
      if len(parts)> 0 and parts[0]:
        new_nodes.append(TextNode(parts[0], TextType.TEXT))
      new_nodes.append(TextNode(text, TextType.LINK, url))
      current_text = parts[1] if len(parts) > 1 else None

    if current_text:
      new_nodes.append(TextNode(current_text, TextType.TEXT))

  return new_nodes

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.TEXT)]
  bold_splited = split_nodes_delimiter(nodes, '**', TextType.BOLD)
  ltalic_splited = split_nodes_delimiter(bold_splited, '_', TextType.ITALIC)
  code_splited = split_nodes_delimiter(ltalic_splited, '`', TextType.CODE)
  image_splited = split_nodes_image(code_splited)
  link_splited = split_nodes_link(image_splited)

  return link_splited

def markdown_to_blocks(markdown):
  blocks = markdown.split("\n\n")
  cleaned_blocks = []
  for block in blocks:
    stripped_block = block.strip()
    if stripped_block:
      cleaned_blocks.append(stripped_block)
  return cleaned_blocks



