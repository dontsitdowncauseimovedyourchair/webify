import os
import sys
from pathlib import Path

from directory_functions import copy_dir
from markdown_functions import markdown_to_html_node

def extract_title(html: str):
    title = ""
    start_index = html.find("<h1>") + 4
    end_index = html.find("</h1>")
    return html[start_index:end_index]

def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.exists(from_path) or os.path.isdir(from_path):
        raise ValueError(f"{from_path} does not exists or is not a file")
    if not os.path.exists(template_path) or os.path.isdir(template_path):
        raise ValueError(f"{template_path} does not exists or is not a file")

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    html_template = ""
    with open(from_path, "r") as md:
        markdown = md.read()
    with open(template_path, "r") as html_file:
        html_template = html_file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(html)
    full_html_page = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_path):
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html_page)


def generate_pages_recursively(dir_path_content, template_path, dest_root_path, basepath):
    files_dirs = os.listdir(dir_path_content)
    for fs_item in files_dirs:
        fs_item_path = os.path.join(dir_path_content, fs_item)
        if os.path.isdir(fs_item_path):
            generate_pages_recursively(fs_item_path, template_path, os.path.join(dest_root_path, fs_item), basepath)
        else:
            if fs_item_path.endswith(".md"):
                generate_page(fs_item_path, template_path, os.path.join(dest_root_path, fs_item.replace(".md", ".html")), basepath)

def main():
    current_dir = Path(__file__).resolve().parent
    public_dir = current_dir.parent / "public"
    docs_dir = current_dir.parent / "docs"
    static_dir = current_dir.parent / "static"

    copy_dir(static_dir, docs_dir)

    content_dir = current_dir.parent / "content"
    template_file = current_dir.parent / "template.html"

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    generate_pages_recursively(content_dir, template_file, docs_dir, basepath)

if __name__ == "__main__":
    main()