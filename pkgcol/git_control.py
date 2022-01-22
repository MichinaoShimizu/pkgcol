from __future__ import print_function
from logger import get_module_logger
import subprocess

logger = get_module_logger(__name__)


class GitControl:
    def __init__(self, directory, repository_name):
        self.directory = directory
        self.repository_name = repository_name

    def clone(self):
        cmd = 'git clone git@github.com:{} {}'.format(
            self.repository_name,
            self.directory
        )
        return subprocess.run(cmd, check=False, shell=True)

    def pull(self):
        cmd = 'cd {} && git config pull.rebase false && git pull'.format(
            self.directory
        )
        return subprocess.run(cmd, check=True, shell=True)
