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

def copy_from_static_to_public():
    current_dir = Path(__file__).resolve().parent
    public_dir = current_dir.parent / "public"
    static_dir = current_dir.parent / "static"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)

    files_dirs = list_files_and_dirs(static_dir)
    for fs_item_path in files_dirs:
        relative_dirname = os.path.relpath(fs_item_path, static_dir)
        if os.path.isdir(fs_item_path):
            os.mkdir(os.path.join(public_dir, relative_dirname))
        else:
            shutil.copy(fs_item_path, os.path.join(public_dir, relative_dirname))
