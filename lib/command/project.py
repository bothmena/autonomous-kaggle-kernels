import os
from git import Repo
from lib.services.db import MongodbORM
from lib.exception.database import ProjectExistsException


orm = MongodbORM()


# def new_project_handler(group=None, category=None, sort_by=None, page=1, search=None, csv_display=False):
def init_project(name: str, path: str, repository: str, framework: str, cpu: bool, internet: bool):
    if path == '.':
        path = os.getcwd()
    if name is None:
        name = os.path.basename(path)
    if repository is None:
        repo = Repo(path)
        repository = list(repo.remotes[0].urls)[0]

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


def status_project(*args, **kwargs):
    print('-' * 50)
    print('project status command / Not yet implemented')
    print('-' * 50)


def update_project(*args, **kwargs):
    print('-' * 50)
    print('project update command / Not yet implemented')
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
        print(' | {:3d} | {:30s} | {:12s} | {:10s} | {:10s} | {:10s} |'.format(i, project['name'], project['framework'], yor(len(project['repository']) > 0),
                                                                               'CPU' if project['cpu'] else 'GPU', yor(project['internet'])))
        print(' ' + '-' * 94)
    print('')
