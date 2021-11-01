# -*- coding: utf-8 -*-
import json
import logging
import multiprocessing
import os
import subprocess
import time
from distutils.core import setup
from tempfile import TemporaryDirectory

from Cython.Build import cythonize

logging.basicConfig(
    format='',
    level=logging.INFO
)

"""
encryptcode.txt 几种规则定义

# 忽略此文件
./setup.py

# 正则忽略文件 
./*/__init__.py

# 忽略此文件夹
./pot_images/

# ～～开头开头表示删除文件
～～./src/ratel/pot/http
"""

encryptcode_rule_file = 'encryptcode.txt'


def build_find():
    all_rules = []
    if not os.path.exists(encryptcode_rule_file):
        logging.info("not found encryptcode.txt file, exit")
        exit(0)
    with open('encryptcode.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            # 跳过注释行
            if line.startswith("#"):
                continue
            # 删除文件夹/文件
            if line.startswith('~~'):
                os.system("rm -rf {}".format(os.path.abspath(line.strip()[2:])))
                continue

            line = line.split("#")[0].strip()
            # ./src/ratel/api/apps => ./src/ratel/api/apps/*
            if not line.endswith('py') and '*' not in line:
                if not line.endswith('/'):
                    line = line + '/'
                line = line + '*'
            all_rules.append('-not -path "{}"'.format(line))
    if not all_rules:
        return "find . -name '*py' -type f"
    find_cmd = '''find . -name '*py' -type f {}'''.format(' '.join(all_rules))
    return find_cmd


def process_py_to_so(file_paths: [] = None, dir_path: str = None):
    """
    .py to .so file
    :return:
    """
    dir_map = {}
    if dir_path and os.path.isdir(dir_path):
        tmp_paths = []
        for _ in os.listdir(dir_path):
            if _.endswith('.py') and _ != '__init__.py':
                tmp_paths.append(os.path.join(dir_path, _))
        dir_map[dir_path] = tmp_paths
    else:
        for _ in file_paths:
            dirname = os.path.dirname(_)
            if dirname in dir_map:
                dir_map[dirname].append(_)
            else:
                dir_map[dirname] = [_]
    if not dir_map:
        logging.error("dir_map is none，finished")
        exit()

    logging.info("dir_map: {}".format(json.dumps(dir_map, indent=4)))

    for dir_name in dir_map:
        _file_paths = dir_map.get(dir_name)
        with TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            setup(ext_modules=cythonize(_file_paths, nthreads=multiprocessing.cpu_count()), script_args=["build_ext", "--inplace"])

            find_cmd = 'find {} -name "*.so" -type f'.format(temp_dir)
            out, error = subprocess.Popen(find_cmd, stdout=subprocess.PIPE, shell=True).communicate()
            so_files = out.decode('utf-8').strip()
            for _ in so_files.split("\n"):
                mv_cmd = 'mv {} {}'.format(_, dir_name)
                _, error = subprocess.Popen(mv_cmd, stdout=subprocess.PIPE, shell=True).communicate()
                if error:
                    logging.error("mv_cmd: {} error".format(mv_cmd))
                    exit(0)

            rm_cmd = 'rm -f {} {}'.format(' '.join([_ for _ in _file_paths]), ' '.join([_.replace('.py', '.c') for _ in _file_paths]))
            # _, error = subprocess.Popen(rm_cmd, stdout=subprocess.PIPE, shell=True).communicate()
            # if error:
            #     logging.error("rm_cmd: {} error".format(rm_cmd))
            #     exit(0)


def get_all_py_files():
    find_cmd = build_find()
    output, error = subprocess.Popen(find_cmd, stdout=subprocess.PIPE, shell=True).communicate()
    file_names = [os.path.abspath(_) for _ in output.decode("utf-8").split('\n') if os.path.isfile(_)]
    return file_names


def main():
    logging.info('start encrypt code ...')
    start = time.time()

    file_names = get_all_py_files()
    process_py_to_so(file_paths=file_names)

    # 最后删除临时文件 build 目录
    # os.system('rm -rf build/*')

    end = time.time()
    logging.info('运行时长：{}s'.format(str(int(end - start))))


if __name__ == '__main__':
    main()
