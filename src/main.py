from page_generator import generate_pages_recursive, copy_directory_recursive
import os 
import shutil

def main():
  if os.path.exists(f"./docs"):
    shutil.rmtree(f"./docs")
  copy_directory_recursive("static", f"./docs/static")
  generate_pages_recursive("content", "template.html", f"./docs")

if __name__ == "__main__":
  main()
