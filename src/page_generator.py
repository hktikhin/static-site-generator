import os 
import shutil
import sys
import config

from htmlnode import markdown_to_html_node
  
def copy_directory_recursive(source_dir, dest_dir):
  # Step 1: If destination directory exists, delete all its contents
  if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)  # Remove destination directory and all contents

  # Step 2: Create the destination directory fresh
  os.makedirs(dest_dir)

  # Step 3: List all entries in the source directory
  entries = os.listdir(source_dir)

  # Step 4: For each entry in the source directory
  for entry in entries:
    source_path = os.path.join(source_dir, entry)
    dest_path = os.path.join(dest_dir, entry)

    # Step 5: If entry is a file
    if os.path.isfile(source_path):
      shutil.copy(source_path, dest_path)  # Copy file to destination
      print("Copied file: " + dest_path)    # Log the copied file path

    # Step 6: If entry is a directory
    else:
      # Recursively copy the subdirectory
      copy_directory_recursive(source_path, dest_path)

def extract_title(markdown):
  lines = markdown.split('\n')
  for line in lines:
    for space_cnt in range(0, 4):
      hash_tag = space_cnt * " " + "# "
      if line.startswith(hash_tag):
        title = line.lstrip(hash_tag).strip()
        return title
  raise Exception("No h1 header found in the markdown text")

def generate_page(from_path, template_path, dest_path):
  print("Generating page from " + from_path + " to " + dest_path + " using " + template_path)
  with open(from_path, "r") as f:
    markdown_content = f.read()
  with open(template_path, "r") as f:
    template_content = f.read()
  
  html_node = markdown_to_html_node(markdown_content)
  html_content = html_node.to_html()
  title = extract_title(markdown_content)

  dest_dir = os.path.dirname(dest_path)
  basepath = config.basepath.rstrip(os.sep)
  root_folder = "/" + os.path.basename(basepath) if basepath else basepath

  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
  final_html = template_content.replace("{{ Title }}", title) \
                  .replace("{{ Content }}", html_content) \
                  .replace('href="/', 'href="' + root_folder + "/") \
                  .replace('src="/', 'src="' + root_folder + "/")
  
  with open(dest_path, "w") as f:
    f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  entries = os.listdir(dir_path_content)

  for entry in entries:
    source_path = os.path.join(dir_path_content, entry)
    dest_path = os.path.join(dest_dir_path, entry)
    if os.path.isfile(source_path):
      generate_page(source_path, template_path, dest_path)  
    else:
      generate_pages_recursive(source_path, template_path, dest_path)

