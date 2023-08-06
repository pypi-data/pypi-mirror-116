#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import types

import jinja2
import yaml


def get_data(directory, remove=False):
    data = {
        "sublate": {}
    }

    module = None
    for filename in ['sublate.json', 'sublate.yaml', 'sublate.py']:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()
        else:
            continue

        if filename.endswith("json"):
            data.update(json.loads(content))
        elif filename.endswith("yaml"):
            data.update(yaml.load(content, Loader=yaml.FullLoader))
        elif filename.endswith("py"):
            module = types.ModuleType('module')

            cwd = os.getcwd()
            os.chdir(directory)
            exec(content, module.__dict__)
            os.chdir(cwd)

            for k, v in module.__dict__.items():
                if k[:2] != "__" and k.isupper():
                    data[k.lower()] = v

        if remove:
            os.remove(path)
    return data, module


def build_dst_directory(path, data, loaders):
    local_data, module = get_data(path, remove=True)
    data.update(local_data)

    loader = jinja2.FileSystemLoader(searchpath=path)
    loaders.insert(0, loader)

    env = jinja2.Environment(loader=jinja2.ChoiceLoader(loaders))

    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)

        # FIXME: support paths not just filenames
        if "exclude" in data and filename in data["exclude"]:
            continue

        if os.path.isdir(full_path):
            build_dst_directory(full_path, data.copy(), loaders)
        else:
            # print(full_path)
            try:
                template = env.get_template(filename)
            except UnicodeDecodeError:
                # print(f"skip: {full_path}")
                continue

            output = template.render(**data).strip()
            with open(full_path, 'w+') as f:
                f.write(output)

    if hasattr(module, 'post'):
        cwd = os.getcwd()
        os.chdir(path)
        module.post()
        os.chdir(cwd)


def build(src_path, dst_path):
    data, module = get_data(src_path, remove=False)

    # TODO: iterate over <path>/*
    if "src" in data.get("sublate"):
        if data["sublate"]["src"][0] == "/":
            src_path = data["sublate"]["src"]
        else:
            src_path = os.path.join(src_path, data["sublate"]["src"])

    if "dst" in data["sublate"]:
        dst_path = data["sublate"]["dst"]

    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)

    shutil.copytree(src_path, dst_path)

    loaders = []
    build_dst_directory(dst_path, data, loaders)


def main():
    parser = argparse.ArgumentParser(prog='sublate')
    parser.add_argument('src', metavar='SRC', type=str, help='src path')
    parser.add_argument('dst', metavar='DST', type=str, nargs='?', default='build', help='dst path')

    args = parser.parse_args()

    build(args.src, args.dst)


if __name__ == "__main__":
    main()
