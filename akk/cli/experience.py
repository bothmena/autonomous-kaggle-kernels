import os
import json

from git.exc import InvalidGitRepositoryError

from akk.lib.exception import NoRepoException, UncommitedChangesException, ExperienceExistsException
from akk.lib.services import MongodbORM
from akk.lib.utils import CodeSourceImporter
from akk.lib.utils.helpers import get_experiences, get_project_last_commit, is_exp_valid
from akk.lib.utils import py2nb
from kaggle.api import KaggleApi


orm = MongodbORM()
kaggle = KaggleApi()


def _fill_experience(experience: dict):
    """
    if the optional keys: ['lr_decay', 'lr_cycle', 'opt_args', 'loss_args'] are not defined in the experience
    we should set them at their default values, respectfully: [None, None, {}, {}]
    :param experience: the experience that will be saved in the DB
    :return:
    """
    keys = ['lr_decay', 'lr_cycle', 'opt_args', 'loss_args']
    defaults = [None, None, {}, {}]

    for i in range(4):
        if keys[i] not in experience.keys():
            experience[keys[i]] = defaults[i]

    return experience


def _project_not_found():
    print('This directory is not a registered AKK project, please make sure you are issuing the cli from the right directory.')
    print('If you did not initialize the project all you have to do is to run:')
    print('$ akk project init [-h: for more information]')


def _assemble_code(project, output_dir):
    # todo: add new attribute to project and new cli argument to project init: entrypoint: main .py file, default: main.py
    project['entrypoint'] = 'main.py'
    importer = CodeSourceImporter(project['entrypoint'], project['path'], output_dir)
    importer.find_file_deps()
    importer.write_output()


def _write_exp_data(experience, path, last_commit):
    if not os.path.isdir(os.path.join(path, '.akk', last_commit, 'experiences')):
        os.mkdir(os.path.join(path, '.akk', last_commit, 'experiences'), 0o755)
    if not os.path.isdir(os.path.join(path, '.akk', last_commit, 'experiences', str(experience['_id']))):
        os.mkdir(os.path.join(path, '.akk', last_commit, 'experiences', str(experience['_id'])), 0o755)

    temp_filename = os.path.join(path, '.akk', last_commit, 'experiences', str(experience['_id']), 'script.py')

    with open(temp_filename, 'w') as temp:
        dic_next = False
        prev_space = 0
        pprev_space = 0
        ppprev_space = 0
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


def _slugify(st: str) -> str:
    return ' '.join(st.rstrip().split()).lower().replace(' ', '-')


def _kernel_metadata(project: dict, experience: dict):
    name = project['name'] + ' ' + str(experience['_id'])
    metadata = {
        "id"                 : "bothmena/" + _slugify(name),
        "title"              : name,
        "code_file"          : "script.ipynb",
        "language"           : "python",
        "kernel_type"        : project['type'],
        "is_private"         : project['private'],
        "enable_gpu"         : not project['cpu'],
        "enable_internet"    : project['internet'],
        "dataset_sources"    : project['datasets'],  # ["bothmena/my-awesome-dataset"]
        "competition_sources": project['competitions'],
        "kernel_sources"     : project['kernels'] + ["bothmena/" + _slugify(name)]
    }
    with open(os.path.join(project['path'], '.akk', experience['git_commit'], 'experiences', str(experience['_id']), 'kernel-metadata.json'), 'w') as f:
        json.dump(metadata, f)


# def new_project_handler(group=None, category=None, sort_by=None, page=1, search=None, csv_display=False):
def new_exp(filename: str):
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        _project_not_found()
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
                experience['status'] = 'Not started'  # profiling / running / stopped / completed / failed / queued (when using search space and set limit of parallel experiences)
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
        _project_not_found()
        return

    # get experience with id and project id.
    experience = orm.get_experience(exp_id, str(project['_id']))
    if experience is None:
        print('This project has no experience with id:', exp_id)
        return

    try:
        # check project last commit, else warning
        last_commit = get_project_last_commit(path)
        if last_commit is None:
            raise UncommitedChangesException()

        # check if the directory "project_path/.akk/_last_commit_id_" exists, if not create it.
        if not os.path.isdir(os.path.join(path, '.akk', last_commit)):
            os.mkdir(os.path.join(path, '.akk', last_commit), 0o755)
        # check if assembled file exists in: project_path/.akk/_last_commit_id_/output.py, if not assemble code.
        if not os.path.isfile(os.path.join(path, '.akk', last_commit, 'output.py')):
            _assemble_code(project, os.path.join(path, '.akk', last_commit))
    except InvalidGitRepositoryError:
        raise NoRepoException()

    # create profiling commit for the experience
    commit = {'experience': experience['_id'], 'cycles': {}}
    for name, cycle in experience['cycles'].items():
        commit['cycles'][name] = {'steps': 20, 'max_runtime': None}

    orm.new_commit(commit)

    # replace experience cycles with profiling commit cycles dict (where all cycles.steps = 50)
    experience_cp = experience.copy()
    experience_cp['cycles'] = commit['cycles']

    # todo: uncomment next line
    # _write_exp_data(experience_cp, path, last_commit)

    # create a kernel meta-data
    # todo: uncomment next line
    # _kernel_metadata(project, experience)

    # akk p init -n 'AKK - Udacity Facial Keypoints Detection Project' --internet
    # convert script to notebook
    folder = os.path.join(path, '.akk', last_commit, 'experiences', str(experience['_id']))
    # todo: uncomment next line
    # py2nb.convert(folder)

    # todo: use kaggle api to push the code.
    kaggle.kernels_push_cli(folder)

    # todo: split into commits and run sequentially.


def stop_exp(*args, **kwargs):
    print('-' * 50)
    print('experience stop cli / Not yet implemented')
    print('-' * 50)


def list_exp(*args, **kwargs):
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        _project_not_found()
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


def status_exp(*args, **kwargs):
    print('-' * 50)
    print('experience status cli / Not yet implemented')
    print('-' * 50)
