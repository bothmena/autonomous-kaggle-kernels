import json
import os

from git.exc import InvalidGitRepositoryError
from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle.api_client import ApiClient
from slugify import slugify
from bson import ObjectId

from akk.lib.exception import NoRepoException, UncommitedChangesException, ExperienceExistsException, \
    ExperienceNotFoundException, ProjectNotAssembledException
from akk.lib.services import MongodbORM
from akk.lib.utils import py2nb
from akk.lib.utils.helpers import get_experiences, get_project_last_commit, is_exp_valid, project_not_found


orm = MongodbORM()

kaggle = KaggleApi(ApiClient())
kaggle.authenticate()


def _write_exp_data(experience, path, last_commit):
    temp_filename = os.path.join(path, '.akk', last_commit, 'experiences', str(experience['_id']), 'script.py')

    with open(temp_filename, 'w') as temp:
        dic_next = False
        with open(os.path.join(path, '.akk', last_commit, 'output.py'), 'r') as f:
            for line in f.readlines():
                if line == '# __EXP__\n':
                    dic_next = True
                elif dic_next:
                    exp = experience.copy()
                    del exp['project']
                    del exp['date']
                    del exp['status']
                    del exp['search_space']
                    del exp['_id']
                    line = line.rstrip()[2:].replace('____', str(exp)) + '\n\n'
                    dic_next = False
                    temp.write(line)
                else:
                    temp.write(line)

    os.chmod(temp_filename, 0o777)


def _kernel_metadata(project: dict, experience: dict):
    name = project['alias'] + ' ' + str(experience['_id'])
    meta_data = {
        'id'                 : 'bothmena/' + slugify(name),
        'title'              : name,
        'code_file'          : 'script.ipynb',
        'language'           : 'python',
        'kernel_type'        : project['type'],
        'is_private'         : 'true' if project['private'] else 'false',
        'enable_gpu'         : 'false' if project['cpu'] else 'true',
        'enable_internet'    : 'true' if project['internet'] else 'false',
        'dataset_sources'    : project['datasets'],
        'competition_sources': project['competitions'],
        'kernel_sources'     : ["bothmena/" + slugify(name)] + project['kernels']
    }
    meta_file = os.path.join(os.path.join(project['path'], '.akk', experience['git_commit'], 'experiences', str(experience['_id']), KaggleApi.KERNEL_METADATA_FILE))
    with open(meta_file, 'w') as f:
        json.dump(meta_data, f, indent=2)


# def new_project_handler(group=None, category=None, sort_by=None, page=1, search=None, csv_display=False):
def new_exp(filename: str):
    # todo: remove experiences from previous project git_commit that were not yet started.
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        project_not_found()
    else:
        experiences = get_experiences(filename)
        successes = 0
        failures = 0
        for experience in experiences:
            if is_exp_valid(experience):
                try:
                    last_commit = get_project_last_commit(path)
                    if last_commit is None:
                        raise UncommitedChangesException()
                except InvalidGitRepositoryError:
                    raise NoRepoException()

                experience['project'] = str(project['_id'])
                experience['git_commit'] = last_commit
                experience['search_space'] = None
                experience['status'] = 'unstarted'  # profiling / running / stopped / completed / failed / queued (when using search space and set limit of parallel experiences)
                try:
                    orm.new_experience(experience)
                    successes += 1
                except ExperienceExistsException:
                    failures += 1

        print('Experiences saved successfully:', successes)
        print('Experiences that already exist:', failures)


def start_exp(exp_id, *args, **kwargs):
    # get project
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        project_not_found()
        return

    # get experience with id and project id.
    experience = orm.get_experience(exp_id, str(project['_id']))
    if experience is None:
        print('This project has no experience with id:', exp_id)
        return

    # if an experience marked as stopped, mark it as running and let the watchdog commit the code automatically.
    if experience['status'] == 'stopped':
        orm.experiences.update_one({'_id': experience['_id']}, {'$set': {'status': 'running'}})
        print('Experience restarted.')
        return

    # you can only start an experience that is unstarted, queued or failed
    # a queued exp. is an experience expanded from a search space and marked as queued if not started immediately
    # an experience can fail due to two reasons: a bug in the project code -> fix the bug, commit, create new experience and start it.
    # or because a problem in estimating the time of execution of the cycles -> fix the akk library -> restart the experience.
    if experience['status'] not in ['unstarted', 'queued', 'failed']:
        print('This experience has already started!')
        return

    # check if assembled file exists in: project_path/.akk/_last_commit_id_/output.py
    if not os.path.isfile(os.path.join(path, '.akk', experience['git_commit'], 'output.py')):
        raise ProjectNotAssembledException()

    if not os.path.isdir(os.path.join(path, '.akk', experience['git_commit'], 'experiences', str(experience['_id']))):
        os.makedirs(os.path.join(path, '.akk', experience['git_commit'], 'experiences', str(experience['_id'])), 0o755)

    # create profiling commit for the experience
    commit = {'experience': experience['_id'], 'cycles': {}}
    for name, cycle in experience['cycles'].items():
        commit['cycles'][name] = {'steps': 20, 'max_runtime': None}

    commit_id = orm.new_commit(commit)

    # replace experience cycles with profiling commit cycles dict (where all cycles.steps = 50)
    experience_cp = experience.copy()
    experience_cp['cycles'] = commit['cycles']

    _write_exp_data(experience_cp, path, experience['git_commit'])

    # create a kernel meta-data
    _kernel_metadata(project, experience)

    # convert script to notebook
    folder = os.path.join(path, '.akk', experience['git_commit'], 'experiences', str(experience['_id']))
    py2nb.convert(folder)

    kaggle.kernels_push_cli(folder)
    orm.commits.update_one({'_id': commit_id}, {'$set': {'status': 'running'}})
    orm.experiences.update_one({'_id': experience['_id']}, {'$set': {'status': 'profiling'}})


def stop_exp(*args, **kwargs):
    print('-' * 50)
    print('experience stop cli / Not yet implemented')
    print('-' * 50)


def list_exp(*args, **kwargs):
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        project_not_found()
    else:
        print('')
        print(' ' + '-' * 98)
        print(' | {:3s} | {:24s} | {:10s} | {:14s} | {:14s} | {:14s} |'.format('#', 'Id', 'Git Commit', 'Batch Size', 'Cycles', 'Networks'))
        print(' ' + '-' * 98)
        i = 0
        for exp in orm.experiences.find({'project': str(project['_id'])}):
            i += 1
            steps = sum([c['steps'] for _, c in exp['cycles'].items()])

            print(' | {:3d} | {:24s} | {:10s} | {:14d} | {:14s} | {:14d} |'.format(
                i, str(exp['_id']), exp['git_commit'], exp['batch_size'], '{} / {} steps'.format(len(exp['cycles']), steps),
                len(exp['networks']))
            )
            print(' ' + '-' * 98)

        print('')


def status_exp(experience: str):
    exp = orm.get_experience(experience)
    if exp is None:
        raise ExperienceNotFoundException()

    commit = orm.commits.find_one({'index': 0, 'experience': exp['_id']})

    print('')
    print(' Status: ', exp['status'])
    print('\n ' + '-' * 42)
    print(' | {:2s} | {:15s} | {:15s} |'.format('#', 'Focused', 'Status'))
    print(' ' + '-' * 42)
    i = 0
    while commit is not None:
        i += 1
        print(' | {:2d} | {:15s} | {:15s} |'.format(i, 'Yes' if commit['focus'] else 'No', commit['status'].upper()))
        print(' ' + '-' * 42)
        if commit['next'] is None:
            commit = None
        else:
            commit = orm.get_commit(str(commit['next']))
