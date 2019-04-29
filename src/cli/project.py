import os
from git import Repo
from git.exc import InvalidGitRepositoryError
from src.lib.services.db import MongodbORM
from src.lib import ProjectExistsException
from src.lib import NoRepoException


orm = MongodbORM()


# def new_project_handler(group=None, category=None, sort_by=None, page=1, search=None, csv_display=False):
def init_project(name: str, path: str, repository: str, framework: str, cpu: bool, internet: bool):
    if path == '.':
        path = os.getcwd()
    if name is None:
        name = os.path.basename(path)
    if repository is None:
        try:
            repo = Repo(path)
            remotes = list(repo.remotes)
            if len(remotes) > 0:
                urls = list(remotes[0].urls)
                if len(urls) > 0:
                    repository = urls[0]
        except InvalidGitRepositoryError:
            raise NoRepoException()

    project = {
        'name'      : name,
        'path'      : path,
        'repository': repository,
        'framework' : framework,
        'cpu'       : cpu,
        'internet'  : internet,
    }

    try:
        orm.new_project(project)
    except ProjectExistsException:
        print(
            'Could not create a new project, a project already exists with the same name and/or path. Please make sure you use a unique name for your project to be able to '
            'identify them on kaggle')
    # todo create the config file if necessary.
    os.mkdir(os.path.join(path, '.akk'), 0o755)


def status_project(*args, **kwargs):
    print('-' * 50)
    print('project status cli / Not yet implemented')
    print('-' * 50)


def update_project(*args, **kwargs):
    print('-' * 50)
    print('project update cli / Not yet implemented')
    print('-' * 50)


def list_project(*args, **kwargs):
    def yor(cond: bool):
        return 'Yes' if cond else 'No'

    print('')
    print(' ' + '-' * 94)
    print(' | {:3s} | {:30s} | {:12s} | {:10s} | {:10s} | {:10s} |'.format('#', 'Project name', 'Framework', 'Repository', 'GPU/CPU', 'Internet'))
    print(' ' + '-' * 94)
    i = 0
    for project in orm.projects.find():
        i += 1
        print(' | {:3d} | {:30s} | {:12s} | {:10s} | {:10s} | {:10s} |'.format(i, project['name'], project['framework'], yor(project['repository'] is not None),
                                                                               'CPU' if project['cpu'] else 'GPU', yor(project['internet'])))
        print(' ' + '-' * 94)
    print('')
