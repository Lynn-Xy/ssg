import shutil
import os
from functions import rewrite_dest_dir, generate_pages

def main():

    rewrite_dest_dir()

    generate_pages()


if __name__ == "__main__":
    main()
