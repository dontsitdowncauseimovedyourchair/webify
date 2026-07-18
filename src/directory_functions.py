import os
import shutil
from pathlib import Path

def list_files_and_dirs(dir_path):
    if not dir_path:
        return []
    paths = []
    files_dirs = os.listdir(dir_path)
    for fs_item in files_dirs:
        fs_item_path = os.path.join(dir_path, fs_item)
        if os.path.isdir(fs_item_path):
            paths.append(fs_item_path)
            paths.extend(list_files_and_dirs(fs_item_path))
        else:
            paths.append(fs_item_path)
    return paths

def copy_dir(src_path: Path, dest_path: Path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)

    files_dirs = list_files_and_dirs(src_path)
    for fs_item_path in files_dirs:
        relative_dirname = os.path.relpath(fs_item_path, src_path)
        if os.path.isdir(fs_item_path):
            os.mkdir(os.path.join(dest_path, relative_dirname))
        else:
            shutil.copy(fs_item_path, os.path.join(dest_path, relative_dirname))
