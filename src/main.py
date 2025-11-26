import shutil
import os
from functions import rewrite_dest_dir

def main():

    rewrite_dest_dir()

    generate_page(src_path="static/content/index.md", template_path="src/template.html", dest_path="public/content/")


if __name__ == "__main__":
    main()
