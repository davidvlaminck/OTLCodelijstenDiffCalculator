import os
import shutil
import subprocess


def git(*args):
    return subprocess.check_call(['git'] + list(args))


class GitHubDownloader:
    @classmethod
    def download_all_branches(cls, branches: dict, temp_dir=''):
        github_repo = "https://github.com/Informatievlaanderen/OSLOthema-wegenenverkeer.git"

        for directory, branch in branches.items():
            cls.download_branch(github_url=github_repo, directory=temp_dir + '\\' + directory, branch=branch)

    @classmethod
    def download_branch(cls, github_url: str, directory: str, branch: str):
        if os.path.isdir(directory):
            shutil.rmtree(directory)

        git("clone", github_url, directory, '-b', branch)
