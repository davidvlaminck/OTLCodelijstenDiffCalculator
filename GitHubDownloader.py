import os
import shutil
import stat
import subprocess


def git(*args):
    return subprocess.check_call(['git'] + list(args))


class GitHubDownloader:
    @classmethod
    def download_all_branches(cls, branches: dict, temp_dir=''):
        github_repo = "https://github.com/Informatievlaanderen/OSLOthema-wegenenverkeer.git"

        for directory, branch in branches.items():
            cls.download_branch(github_url=github_repo, directory=temp_dir + directory, branch=branch)

    @classmethod
    def download_branch(cls, github_url: str, directory: str, branch: str):
        if os.path.isdir(directory):
            # fix for being unable to delete files in .git dir
            def del_rw(action, name, exc):
                os.chmod(name, stat.S_IWRITE)
                os.remove(name)

            shutil.rmtree(directory, onerror=del_rw)

        git("clone", github_url, directory, '-b', branch)
