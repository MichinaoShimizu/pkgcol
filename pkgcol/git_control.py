from __future__ import print_function
from logger import get_module_logger
import subprocess

logger = get_module_logger(__name__)


class GitControl:
    def __init__(self, directory, repository):
        self.directory = directory
        self.repository = repository

    def clone(self):
        cmd = f'git clone git@github.com:{self.repository} {self.directory}'
        return subprocess.run(cmd, check=False, shell=True)

    def pull(self):
        cmd = f'cd {self.directory} && git pull'
        return subprocess.run(cmd, check=True, shell=True)
