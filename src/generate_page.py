import os
import shutil
from markdown_blocks import *
from htmlnode import *

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        read_markdown = f.read()
    with open(template_path) as f:
        read_template = f.read()
    html_node = markdown_to_html_node(read_markdown)
    html = html_node.to_html()
    title = extract_title(read_markdown)
    read_template = read_template.replace("{{ Title }}",title)
    new_template = read_template.replace("{{ Content }}",html)
    new_dirs = os.path.dirname(dest_path)
    if not os.path.exists(new_dirs):
        os.makedirs(new_dirs)
    with open(dest_path,"w") as new_f:
        new_f.write(new_template)
        new_f.close()
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_list = os.listdir(dir_path_content)
    for content in content_list:
        content_path = os.path.join(dir_path_content,content)
        dest_content_path = os.path.join(dest_dir_path,content)
        if os.path.isfile(content_path):
            print("content path:   ", content_path)
            template_file = open(template_path, "r")
            template = template_file.read()
            template_file.close()
            markdown_file = open(content_path,"r")
            markdown = markdown_file.read()
            markdown_file.close()
            html_node = markdown_to_html_node(markdown)
            html = html_node.to_html()
            title = extract_title(markdown)
            template = template.replace("{{ Title }}",title)
            new_template = template.replace("{{ Content }}",html)
            name = os.path.splitext(content)
            filename = f"{name[0]}.html"
            print("FILENAME!!!!  ",filename)
            dest_content_name_path = os.path.join(dest_dir_path,filename)
            with open(dest_content_name_path,"w") as new_f:
                new_f.write(new_template)
                new_f.close()
        else:
            public_dirs = os.path.join(dest_dir_path,content)
            print("DIRS!!!")
            print(content)
            if not os.path.exists(public_dirs):
                os.makedirs(public_dirs,exist_ok=True)
            generate_pages_recursive(content_path,template_path,public_dirs)
            

"""        filename = os.path.splitext(content)
        filename = str.join(filename[0],".html")
        dest_content_name = os.path.join(dest_content_path,filename)
"""


generate_pages_recursive("content","template.html","public")