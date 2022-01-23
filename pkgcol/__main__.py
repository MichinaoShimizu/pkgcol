from __future__ import print_function
import os
import shutil
from argparse import ArgumentParser
from logger import get_module_logger
from dependency_graph import DependencyGraph
from git_control import GitControl
from package_json import PackageJson

WORK = '.work'

logger = get_module_logger(__name__)


def get_options():
    description = 'Visualize repository and package dependencies'
    parser = ArgumentParser(description=description)
    parser.add_argument('-r', '--repository_names',
                        action='store',
                        nargs='*',
                        required=True,
                        default=None
                        )

    parser.add_argument('-f', '--filter_words',
                        action='store',
                        nargs='*',
                        required=False,
                        default=[]
                        )

    parser.add_argument('-c', '--clean',
                        action='store_true',
                        required=False,
                        default=False
                        )

    parser.add_argument('-s', '--skip_repository_setting',
                        action='store_true',
                        required=False,
                        default=False
                        )

    return parser.parse_args()


def main():
    args = get_options()
    repos = args.repository_names
    os.makedirs(WORK, exist_ok=True)

    dict = {}
    for repo in repos:
        directory_path = f'{WORK}/{repo}'
        if not args.skip_repository_setting:
            git = GitControl(directory=directory_path, repository=repo)
            git.clone()
            git.pull()

        json = PackageJson(file_path=f'{directory_path}/package.json')
        dict[repo] = json.dependencies_all()

        if args.clean:
            shutil.rmtree(WORK)

    graph = DependencyGraph(dict=dict)
    graph.data_setting(filter_words=args.filter_words)
    graph.graph_setting(scale_num=2)
    graph.show(file_path='dependency_graph.html')
    return 0


if __name__ == '__main__':
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        exit(1)
    except Exception as e:
        logger.error(e)
        exit(1)
