from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def count_starting_hashes(markdown: str) -> int:
  stripped = markdown.lstrip('#')
  return len(markdown) - len(stripped)

def block_to_block_type(markdown):
  if markdown.startswith("```\n") and markdown.endswith("\n```"):
    return BlockType.CODE

  hash_count = count_starting_hashes(markdown)
  if hash_count >= 1 and hash_count <= 6:
    return BlockType.HEADING

  lines = markdown.split("\n")
  if all([line.startswith(">") for line in lines]):
    return BlockType.QUOTE

  if all([line.startswith("- ") for line in lines]):
    return BlockType.UNORDERED_LIST

  expected_number = 1
  for line in lines:
    if not line.startswith(f"{expected_number}. "):
      return BlockType.PARAGRAPH
    expected_number += 1
  return BlockType.ORDERED_LIST
