import os
import re

import toml

from ..transpiler.utils import is_snake_case
from .mys_dir import MYS_DIR


class Author:

    def __init__(self, name, email):
        self.name = name
        self.email = email


class PackageConfig:

    def __init__(self, path):
        self.authors = []
        self.config = self.load_package_configuration(path)

    def load_package_configuration(self, path):
        with open(os.path.join(path, 'package.toml')) as fin:
            config = toml.loads(fin.read())

        package = config.get('package')

        if package is None:
            raise Exception("'[package]' not found in package.toml.")

        for name in ['name', 'version', 'authors']:
            if name not in package:
                raise Exception(f"'[package].{name}' not found in package.toml.")

        if not is_snake_case(package['name']):
            raise Exception(
                f"package name must be snake case, got '{package['name']}'")

        for author in package['authors']:
            mo = re.match(r'^([^<]+)<([^>]+)>$', author)

            if not mo:
                raise Exception(f"Bad author '{author}'.")

            self.authors.append(Author(mo.group(1).strip(), mo.group(2).strip()))

        if 'description' not in package:
            package['description'] = ''

        dependencies = {
            'fiber': {'path': os.path.join(MYS_DIR, 'lib/packages/fiber')}
        }

        if 'dependencies' in config:
            dependencies.update(config['dependencies'])

        config['dependencies'] = dependencies

        if 'c-dependencies' not in config:
            config['c-dependencies'] = {}

        return config

    def __getitem__(self, key):
        return self.config[key]
