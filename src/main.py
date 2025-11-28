from functions import rewrite_dest_dir
from gencontent import generate_pages_recursive

def main():

    rewrite_dest_dir()

    generate_pages_recursive()

if __name__ == "__main__":
    main()
