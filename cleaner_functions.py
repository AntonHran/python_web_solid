import os
import shutil
import unicodedata
import re
from cleaner_consts import table, extensions


def sort_files(path: str, path_: str) -> None:
    for file in os.listdir(path):
        if os.path.isfile(path + '\\' + file):
            process_file(path, file, path_)
        elif os.path.isdir(path + '\\' + file) and file.lower() not in extensions.keys():
            sort_files(path + '\\' + file, path_)


def process_file(path: str, file_name: str, root: str) -> None:
    current_path: str = path + '\\'
    *name, extension = file_name.split('.')
    for key, val in extensions.items():
        if extension in val:
            move_to(old_path=current_path, new_path=root + '\\' + key.title(), file_name='.'.join(name), ext=extension)
            break
        elif extension not in val and key == 'other':
            shutil.move(current_path + file_name, root + '\\' + key.title() + '\\' + file_name)


def check(path: str) -> None:
    for folder in os.listdir(path):
        if get_folder_size(path + '\\' + folder) == 0:
            shutil.rmtree(path + '\\' + folder)


def get_folder_size(folder_path: str) -> int:
    total_size: int = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size


def rename(file_name: str) -> str:
    pattern = r'[\w\.\-\(\)]'
    for char in file_name:
        if not re.match(pattern, char):
            if ord(unicodedata.normalize('NFC', char)) in table.keys():
                new_char = char.translate(table)
                file_name = file_name.replace(char, new_char)
            else:
                file_name = file_name.replace(char, '_')
    return file_name


def move_to(old_path: str, new_path: str, file_name: str, ext: str) -> None:
    new_name: str = rename(file_name)
    if ext in extensions['archive']:
        try:
            os.makedirs('\\'.join((new_path, new_name.title())))
            shutil.unpack_archive(old_path + file_name + '.' + ext, '\\'.join((new_path, new_name.title())))
            os.remove(old_path + file_name + '.' + ext)
        except FileExistsError:
            os.remove(old_path + file_name + '.' + ext)
    else:
        os.rename(old_path + file_name + '.' + ext, old_path + new_name + '.' + ext)  # f'{old_path}{file_name}.{ext}'
        i: int = 0
        while True:
            if new_name + '.' + ext not in os.listdir(new_path):
                shutil.move(old_path + new_name + '.' + ext, new_path + '\\' + new_name + '.' + ext)
                break
            else:
                i += 1
                file_name = new_name
                new_name = file_name + f'_{i}'
                os.rename(old_path + file_name + '.' + ext, old_path + new_name + '.' + ext)
    if not os.listdir(old_path):
        os.rmdir(old_path)


def make_dir(path_to: str) -> None:
    if os.path.exists(path_to):
        for key in extensions:
            try:
                os.makedirs('\\'.join((path_to, key.title())))
            except FileExistsError:
                continue
    else:
        print('Something went wrong. Check a correctness of the entered path.')
