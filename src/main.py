from functions import rewrite_dest_dir
from gencontent import generate_pages_recursive
import sys

def main():

    if len(sys.argv) > 1:

        basepath = sys.argv[1]

    else:

        basepath = "/"

    rewrite_dest_dir()

    generate_pages_recursive(basepath=basepath)

if __name__ == "__main__":
    main()
