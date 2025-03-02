from textnode import TextNode, TEXT_TYPE
from utils import copy_content, generate_page, generate_page_recursive
import os

def main():
    copy_content()
    template_path = os.path.join(os.getcwd(), 'template.html')
    generate_page_recursive('content', template_path, 'public')

if __name__ == "__main__":
    main()
