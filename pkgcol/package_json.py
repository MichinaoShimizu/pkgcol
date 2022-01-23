from __future__ import print_function
import json
from logger import get_module_logger

logger = get_module_logger(__name__)


class PackageJson:
    def __init__(self, file_path):
        with open(file_path) as f:
            self.data = json.load(f)

    def __seek(self, name, default):
        return self.data[name] if name in self.data else default

    def name(self):
        return self.__seek('name', '')

    def dependencies(self):
        return self.__seek('dependencies', {})

    def dev_dependencies(self):
        return self.__seek('devDependencies', {})

    def dependencies_all(self):
        a = self.dependencies()
        b = self.dev_dependencies()
        return {**a, **b}
