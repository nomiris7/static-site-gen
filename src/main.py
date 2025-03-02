import sys
from textnode import TextNode, TEXT_TYPE
from utils import copy_content, generate_page, generate_page_recursive
import os

def main():
    basepath = sys.argv[1]
    if basepath == None:
        basepath = '/'
    copy_content()
    template_path = os.path.join(os.getcwd(), 'template.html')
    generate_page_recursive('content', template_path, 'docs', basepath)

if __name__ == "__main__":
    main()
