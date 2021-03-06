from __future__ import print_function
import os
import shutil
from argparse import ArgumentParser
from logger import get_module_logger
from dependency_graph import DependencyGraph
from git_control import GitControl
from package_json import PackageJson

WORK = '.work'
OUTPUT_FILE = 'dependency_graph.html'

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

    parser.add_argument('-s', '--skip_setting',
                        action='store_true',
                        required=False,
                        default=False
                        )

    return parser.parse_args()


def main():
    args = get_options()
    if args.clean:
        shutil.rmtree(WORK)
        return 0

    os.makedirs(WORK, exist_ok=True)

    dict = {}
    for repo in args.repository_names:
        path = f'{WORK}/{repo}'
        if not args.skip_setting:
            git = GitControl(directory=path, repository=repo)
            git.clone()
            git.pull()

        json = PackageJson(file_path=f'{path}/package.json')
        dict[repo] = json.dependencies_all()

    graph = DependencyGraph()
    graph.data_setting(dict=dict, filter_words=args.filter_words)
    graph.graph_setting(scale_num=2)
    graph.show(file_path=OUTPUT_FILE)
    logger.info(OUTPUT_FILE)
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
