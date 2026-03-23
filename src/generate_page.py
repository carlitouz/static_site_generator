from block_markdown import markdown_to_html_node
import os

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no h1 header found")

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as from_file:
        markdown = from_file.read()

    with open(template_path) as template_file:
        template = template_file.read()
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content)
    page = page.replace(f'href="/', f'href="{basepath}')
    page = page.replace(f'src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(page)



def generate_page_recursive(basepath, from_path, template_path, dest_path):
    for current_path in os.listdir(from_path):
        source = os.path.join(from_path, current_path)
        dest = os.path.join(dest_path, current_path)
        if os.path.isdir(source):
            generate_page_recursive(basepath, source, template_path, dest)
        elif source.endswith(".md"):
            generate_page(basepath, source, template_path, dest.replace(".md", ".html"))
