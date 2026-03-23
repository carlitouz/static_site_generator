import os
import shutil

def copy_static(src, dst):
    if os.path.exists(dst):
        print(f"Removing directory: {dst}")
        shutil.rmtree(dst)
    copy_static_no_delete(src, dst)

def copy_static_no_delete(src, dst):
    print(f"Creating directory: {dst}")
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            print(f"{item} is a file, copying from {src_path} to {dst_path}")
            shutil.copy(src_path, dst_path)
        if os.path.isdir(src_path):
            print(f"{item} is a directory")
            copy_static_no_delete(src_path, dst_path)