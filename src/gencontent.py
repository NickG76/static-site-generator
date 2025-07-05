import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f" * Generating: {from_path} -> {dest_path} using {template_path}")

    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    title = extract_title(markdown_content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as to_file:
        to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown")


def generate_pages_recursive(content_dir, template_path, public_dir):
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file == "index.md":
                from_path = os.path.join(root, file)
                # relative path like blog/glorfindel
                rel_path = os.path.relpath(root, content_dir)
                dest_dir = os.path.join(public_dir, rel_path)
                dest_path = os.path.join(dest_dir, "index.html")
                generate_page(from_path, template_path, dest_path)

