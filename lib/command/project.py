import os
from git import Repo
from lib.services.db import MongodbORM

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
        'name': name,
        'path': path,
        'repository': repository,
        'framework': framework,
        'cpu': cpu,
        'internet': internet,
    }

    orm.new_project(project)
    # todo create the config file if necessary.


def status_project(*args, **kwargs):
    print('-' * 50)
    print('project status command / Not yet implemented')
    print('-' * 50)


def update_project(*args, **kwargs):
    print('-' * 50)
    print('project update command / Not yet implemented')
    print('-' * 50)
