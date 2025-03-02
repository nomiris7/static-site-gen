import os
import shutil
import re

from block_markdown import markdown_to_html_node

def copy_content(source = None, dest = None):
    if source == None:
        source = os.path.join(os.getcwd(), 'static')
    if dest == None:
        dest = os.path.join(os.getcwd(), 'public')
        shutil.rmtree(dest)
        os.mkdir(os.path.join(dest))
    
    static_files = os.listdir(source)

    for file in static_files:
        if os.path.isdir(os.path.join(source, file)):
            os.mkdir(os.path.join(dest, file))
            copy_content(os.path.join(source, file), os.path.join(dest, file))
        else:
            shutil.copy(os.path.join(source, file), os.path.join(dest, file))


def extract_title(text):
    title = re.search(r"^#{1}\ {1}(.*)", text)
    return title.group(1)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
        title = extract_title(markdown)
        with open(template_path) as file_2:
            template = file_2.read()
            html_content = markdown_to_html_node(markdown)
            html_string = html_content.to_html()
            final_string = template.replace(r"{{ Title }}", title)
            final_string = final_string.replace(r"{{ Content }}", html_string)
            #if not os.path.exists(dest_path):
            #    os.mkdir(dest_path)
            with open(dest_path, "w") as file_3:
                file_3.write(final_string)

def generate_page_recursive(source, template_path, dest):
    if source == None:
        source = os.path.join(os.getcwd(), 'content')
    if dest == None:
        dest = os.path.join(os.getcwd(), 'public')
    
    content_files = os.listdir(source)

    for file in content_files:
        if os.path.isdir(os.path.join(source, file)):
            os.mkdir(os.path.join(dest, file))
            generate_page_recursive(os.path.join(source, file), template_path ,os.path.join(dest, file))
        else:
            page = file.rstrip('.md')
            page = page + ".html"
            generate_page(os.path.join(source, file), template_path ,os.path.join(dest, page))