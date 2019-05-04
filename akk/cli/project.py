import os

from git import Repo
from git.exc import InvalidGitRepositoryError

from akk.lib.exception import ProjectExistsException, NoRepoException
from akk.lib.services import MongodbORM


orm = MongodbORM()


def init_project(name: str, alias: str, path: str, entrypoint: str, repository: str, framework: str, cpu: bool, internet: bool, datasets: list, kernels: list,
                 competitions: list, public: bool, k_type: str):
    if path == '.':
        path = os.getcwd()
    if name is None:
        name = os.path.basename(path)[:50]
    elif len(name) < 5:
        raise ValueError('Project name should at least 5 characters long.')
    elif len(name) > 50:
        raise ValueError('Project name should be 50 characters long or less.')
    if alias is None:
        alias = name[:25]
    elif len(alias) > 25:
        raise ValueError('Project alias should be 50 characters long or less.')
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
        'name'        : name,
        'alias'       : alias,
        'path'        : path,
        'entrypoint'  : entrypoint,
        'repository'  : repository,
        'framework'   : framework,
        'cpu'         : cpu,
        'internet'    : internet,
        'datasets'    : datasets,
        'kernels'     : kernels,
        'competitions': competitions,
        'private'     : not public,
        'type'        : k_type,
    }

    try:
        orm.new_project(project)
    except ProjectExistsException:
        print(
            'Could not create a new project, a project already exists with the same name and/or path. Please make sure you use a unique name for your project to be able to '
            'identify them on kaggle')

    if not os.path.isdir(os.path.join(path, '.akk')):
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
