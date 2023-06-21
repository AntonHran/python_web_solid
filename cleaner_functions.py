import asyncio
import aiofiles
import aiofiles.os
import aioshutil

import os
import re
import unicodedata
from cleaner_consts import table
from typing import Tuple, Callable

root = ''


async def process_directory(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if await aiofiles.os.path.isfile(file_path):
            await process_file(directory, file)
        elif await aiofiles.os.path.isdir(file_path) and file.lower() not in extensions.keys():
            await process_directory(file_path)


async def process_file(file_path, file):
    name, extension = file.rsplit('.', 1)
    func_ = handle_func(extension)
    await func_[0](file_path, f'{root}\\{func_[1]}', name, extension)  # !!!!! old path
    await check_folder(file_path)
    await asyncio.sleep(0.01)


async def move_to(old_path: str, new_path: str, file_name: str, ext: str) -> None:
    new_name: str = rename(file_name)
    await aiofiles.os.rename(f'{old_path}\\{file_name}.{ext}', f'{old_path}\\{new_name}.{ext}')
    i: int = 0
    while True:
        if f'{new_name}.{ext}' not in os.listdir(new_path):
            await aiofiles.os.replace(f'{old_path}\\{new_name}.{ext}', f'{new_path}\\{new_name}.{ext}')
            break
        else:
            i += 1
            file_name = new_name
            new_name = f'{file_name}_{i}'
            await aiofiles.os.rename(f'{old_path}\\{file_name}.{ext}', f'{old_path}\\{new_name}.{ext}')


async def move_to_archive(old_path: str, new_path: str, file_name: str, ext: str) -> None:
    new_name: str = rename(file_name)
    try:
        await aiofiles.os.makedirs('\\'.join((new_path, new_name.title())))
        await aioshutil.unpack_archive(f'{old_path}\\{file_name}.{ext}', '\\'.join((new_path, new_name.title())))
        await aiofiles.os.remove(f'{old_path}\\{file_name}.{ext}')
    except FileExistsError:
        await aiofiles.os.remove(f'{old_path}\\{file_name}.{ext}')


async def move_to_other(old_path: str, new_path: str, file_name: str, ext: str) -> None:
    new_name: str = rename(file_name)
    await aiofiles.os.rename(f'{old_path}\\{file_name}.{ext}', f'{old_path}\\{new_name}.{ext}')
    await aiofiles.os.replace(f'{old_path}\\{file_name}.{ext}', f'{new_path}\\{new_name}.{ext}')


def rename(file_name: str) -> str:
    pattern = r'[a-zA-Z0-9\.\-\(\)]'
    for char in file_name:
        if not re.match(pattern, char):
            if ord(unicodedata.normalize('NFC', char.lower())) in table.keys():
                file_name = file_name.replace(char, char.translate(table))
            else:
                file_name = file_name.replace(char, '_')
    return file_name


async def check_folder(old_path: str) -> None:
    if not os.listdir(old_path):
        await aiofiles.os.rmdir(old_path)


extensions = dict(images=[('jpeg', 'png', 'jpg', 'svg'), move_to],
                  video=[('avi', 'mp4', 'mov', 'mkv'), move_to],
                  documents=[('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'), move_to],
                  audio=[('mp3', 'ogg', 'wav', 'amr', 'm4a'), move_to],
                  web=[('html', 'xml', 'csv', 'json'), move_to],
                  archive=[('zip', 'gz', 'tar'), move_to_archive])


def handle_func(file_extension: str) -> Tuple[Callable, str]:
    for category, extension in extensions.items():
        if file_extension in extension[0]:
            return extension[1], category.title()
    return move_to_other, 'Other'


async def after_check(path: str) -> None:
    for folder in os.listdir(path):
        if get_folder_size(f'{path}\\{folder}') == 0:
            await aioshutil.rmtree(f'{path}\\{folder}')


def get_folder_size(folder_path: str) -> int:
    total_size: int = 0
    for roots, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(roots, file)
            total_size += os.path.getsize(file_path)
    return total_size


async def make_directions(path: str) -> None:
    if await aiofiles.os.path.exists(path):
        for key in extensions:
            await aiofiles.os.makedirs('\\'.join((path, key.title())), exist_ok=True)
        await aiofiles.os.makedirs('\\'.join((path, 'Other')), exist_ok=True)
    else:
        print('Something went wrong. Check a validity of the entered path.')


def instructions() -> None:
    print('''\tNow you are in the cleaning module. In this module I help you to sort all files in the chosen directory 
    thus cleaning your folder.
    To do that, type the path to your folder according the pattern: <DISC:\\Folder\\Other folder...>
    To back to main menu, type: <back>''')


async def clean_folder_main():
    instructions()
    global root
    while True:
        root = input('\nType a path to a folder to clean: ')
        if root == 'back':
            break
        await make_directions(root)
        await process_directory(root)
        await after_check(root)


# asyncio.run(clean_folder_main())

'''for key, val in extensions.items():
        if extension in val:
            await move_to(old_path=current_path, new_path=f'{root}\\{key.title()}', file_name='.'.join(name),
                          ext=extension)
            await check_folder(current_path)
            break
            
D:\\GOIT\\trash
'''
