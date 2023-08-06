#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import types

import jinja2
import yaml


def main():
    parser = argparse.ArgumentParser(prog='sublate')
    parser.add_argument('src', metavar='SRC', type=str, help='src path')
    parser.add_argument('dst', metavar='DST', type=str, nargs='?', default='build', help='dst path')
    # TODO: support --data option

    args = parser.parse_args()
    build(args.src, args.dst)


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

    # TODO: ask
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)

    shutil.copytree(src_path, dst_path)
    render(src_path, dst_path, data)


def render(src_path, dst_path, data):
    local_data, module = get_data(dst_path, remove=True)
    data.update(local_data)

    if "data" in local_data:
        if data["data"].startswith("/"):
            normalized = data["data"]
        else:
            normalized = os.path.join(src_path, data["data"])

        external_data, m = get_data(normalized, remove=False)
        data.update(external_data)

    # TODO: support custom templates path
    loader = jinja2.FileSystemLoader(searchpath=dst_path)
    env = jinja2.Environment(loader=jinja2.ChoiceLoader([loader]))

    for filename in os.listdir(dst_path):
        # TODO: support generic paths
        if "exclude" in data and filename in data["exclude"]:
            continue

        new_dst_path = os.path.join(dst_path, filename)
        if os.path.isdir(new_dst_path):
            new_src_path = os.path.join(src_path, filename)
            render(new_src_path, new_dst_path, data.copy())
        else:
            try:
                template = env.get_template(filename)
            except UnicodeDecodeError:
                continue

            output = template.render(**data).strip()
            with open(new_dst_path, 'w+') as f:
                f.write(output)

    if hasattr(module, 'post'):
        cwd = os.getcwd()
        os.chdir(dst_path)
        module.post(dst_path)
        os.chdir(cwd)


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


if __name__ == "__main__":
    main()
