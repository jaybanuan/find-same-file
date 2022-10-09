#!/usr/bin/env python3
 
import os
import sys
import pathlib
import hashlib


def get_message_digest(file_path:pathlib.Path, algorithm:str='md5', partial:bool=True, max_size:int=1024*1024) -> str:
    hash = hashlib.new(algorithm)

    remain_size = max_size
    read_size = 1024*1024
    with open(file_path, "rb") as input_stream:
        while (not partial) or (remain_size > 0):
            data = input_stream.read(read_size)
            if data == '':
                break
        
            hash.update(data)
            remain_size -= read_size
        
        return hash.digest()


def find_same_file(src_file_path:pathlib.Path, search_root:pathlib.Path):
    src_digest = get_message_digest(src_file_path)

    for root, _, files in os.walk(search_root):
        for file in files:
            dst_file_path = pathlib.Path(root, file)

            try:
                dst_digest = get_message_digest(dst_file_path)
            except Exception as e:
                yield e, dst_file_path
            else:
                if src_digest == dst_digest:
                    yield None, dst_file_path


if __name__ == "__main__":
    src_file_path = pathlib.Path(sys.argv[1])
    search_root = pathlib.Path('.')

    for exception, file_path in find_same_file(src_file_path, search_root):
        if exception:
            print(f'error: file={str(file_path)}  cause: {str(exception)}')
        else:
            print(str(file_path))
