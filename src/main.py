from page_generator import generate_pages_recursive, copy_directory_recursive
import os 
import shutil

def main():
  if os.path.exists("public"):
    shutil.rmtree("public")
  copy_directory_recursive("static", "public/static")
  generate_pages_recursive("content", "template.html", "public")
if __name__ == "__main__":
  main()
