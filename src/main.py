from page_generator import generate_pages_recursive, copy_directory_recursive
import os 
import shutil
import sys

if len(sys.argv) > 1:
  basepath = sys.argv[1]
else:
  basepath = "/"

def main():
  if os.path.exists(f"{basepath}docs"):
    shutil.rmtree(f"{basepath}docs")
  copy_directory_recursive("static", f"{basepath}docs/static")
  generate_pages_recursive("content", "template.html", f"{basepath}docs")

if __name__ == "__main__":
  main()
