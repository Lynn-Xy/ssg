import os
from functions import extract_markdown_title, markdown_to_html_node


def generate_pages_recursive(src_path="content/", template_path="src/template.html", dest_path="public/"):

    if os.path.exists(src_path) and os.path.exists(dest_path):

        print(f"Generating pages from {src_path} to {dest_path}.")

        for name in os.listdir(src_path):

            name_path = os.path.join(src_path, name)

            if os.path.isfile(name_path):

                with open(name_path, "r") as src_object:

                    src_content = src_object.read()

                    src_file_name_full = os.path.basename(name_path)

                    src_file_name_parts = src_file_name_full.split(".", 1)

                    src_file_name = src_file_name_parts[0]

                    with open(template_path, "r") as template_object:

                        template_content = template_object.read()

                        parent_html_node = markdown_to_html_node(src_content)

                        src_html = parent_html_node.to_html()

                        src_title = extract_markdown_title(src_content)

                        page_html = template_content.replace("{{ Title }}", src_title)

                        page_html = page_html.replace("{{ Content }}", src_html)

                        dest_html_path = os.path.join(dest_path, f"{src_file_name}.html")

                        with open(dest_html_path, "w") as dest_html_object:

                            dest_html_object.write(page_html)

                            print(f"src_html written to {dest_html_path}")

            elif os.path.isdir(name_path):

                sub_src_path = os.path.join(src_path, name)

                sub_dest_path = os.path.join(dest_path, name)

                os.makedirs(sub_dest_path, exist_ok=True)

                generate_pages_recursive(src_path=sub_src_path, template_path=template_path, dest_path=sub_dest_path)

            else:

                print(f"{name_path}")
                raise Exception("invalid item in directory.")

    else:

        raise Exception("directories not copied correctly.")