
import unittest
from page_generator import extract_title

class TestGenerator(unittest.TestCase):
    def test_basic_h1(self):
      self.assertEqual(extract_title("# Hello"), "Hello")
    
    def test_h1_with_leading_trailing_spaces(self):
      self.assertEqual(extract_title("   #   Hello World   "), "Hello World")

    def test_h1_among_multiple_lines(self):
        markdown = """
Some intro text
# Title Here
More text
        """
        self.assertEqual(extract_title(markdown), "Title Here")

    def test_no_h1_raises_exception(self):
        markdown = """
## Subtitle
No h1 header here
        """
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))

    def test_h1_with_only_hash_and_spaces(self):
        self.assertEqual(extract_title("#    "), "")
