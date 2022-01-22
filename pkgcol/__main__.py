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
    description = ''
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

    parser.add_argument('-c', '--clean_after_deps',
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
    repo_names = args.repository_names
    os.makedirs(WORK, exist_ok=True)

    dict = {}
    for repo_name in repo_names:
        logger.info(f'target:{repo_name}')
        directory_path = f'{WORK}/{repo_name}'
        if not args.skip_repository_setting:
            git = GitControl(directory=directory_path, repo_name=repo_name)
            git.clone()
            git.pull()

        package_json_path = f'{directory_path}/package.json'
        package_json = PackageJson(file_path=package_json_path)
        org_name = repo_name.split('/')[0]
        repo_package_name = package_json.name()
        if repo_package_name.find(org_name) < 0:
            repo_package_name = f'@{org_name}/{package_json.name()}'

        dict[repo_package_name] = package_json.dependencies_all()
        if args.clean_after_deps:
            shutil.rmtree(WORK)

    filter_words = args.filter_words

    graph = DependencyGraph(dict=dict)
    graph.data_setting(filter_words=filter_words)
    graph.graph_setting(scale_num=3)
    graph.output(file_path='dependency_graph.html')
    return 0


if __name__ == '__main__':
    # try:
    exit_code = main()
    exit(exit_code)
    # except KeyboardInterrupt:
    #     exit(1)
    # except Exception as e:
    #     logger.error(e)
    #     exit(1)
