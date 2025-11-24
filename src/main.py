import shutil
import os

def main():

    src_dir = "static/"

    dest_dir = "public/"

    if os.path.exists(dest_dir):

        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

    copy_src_to_dest(src_dir, dest_dir)

def copy_src_to_dest(src_dir, dest_dir):
    
    for name in os.listdir(src_dir):

        src_path = os.path.join(src_dir, name)

        if os.path.isfile(src_path):

            copied_path = shutil.copy(src_path, dest_dir)

            print(copied_path)

        elif os.path.isdir(src_path):

            os.mkdir(os.path.join(dest_dir, name))

            src_sub_dir = os.path.join(src_dir, name)

            dest_sub_dir = os.path.join(dest_dir, name)

            copy_src_to_dest(src_sub_dir, dest_sub_dir)

        else:

            raise OSError("Invalid item in directory path.")


if __name__ == "__main__":
    main()
