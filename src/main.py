from page_generator import generate_pages_recursive, copy_directory_recursive
import os 
import shutil
import sys
import config

if len(sys.argv) > 1:
  config.basepath = sys.argv[1]

def main():
  if os.path.exists(f"{config.basepath}docs"):
    shutil.rmtree(f"{config.basepath}docs")
  copy_directory_recursive(f"{config.basepath}static", f"{config.basepath}docs/static")
  generate_pages_recursive(f"{config.basepath}content", f"{config.basepath}template.html", f"{config.basepath}docs")

if __name__ == "__main__":
  main()
