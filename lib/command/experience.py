import os
import shutil
from git import Repo
from git.exc import InvalidGitRepositoryError
from lib.services.db import MongodbORM
from lib.command.source_code import CodeSourceImporter
from lib.exception.git import NoRepoException, UncommitedChangesException
from lib.exception.database import ExperienceExistsException


orm = MongodbORM()


def _is_exp_valid(exp: dict):
    for key, tp in {'batch_size': int, 'cycles': dict, 'networks': dict}.items():
        if key not in exp.keys():
            return False
        elif not isinstance(exp[key], tp):
            return False

    for _, hps in exp['networks'].items():
        if not isinstance(hps, dict):
            return False
        for key, tp in {'lr': float, 'optimizer': str, 'loss': str}.items():
            if key in hps.keys():
                if not isinstance(hps[key], tp):
                    return False
            elif key in exp.keys():
                if not isinstance(exp[key], tp):
                    return False
            else:
                return False

    for _, items in exp['cycles'].items():
        if not isinstance(items, dict):
            return False
        for key, tp in {'steps': int}.items():
            if key in items.keys():
                if not isinstance(items[key], tp):
                    return False
            elif key in exp.keys():
                if not isinstance(exp[key], tp):
                    return False
            else:
                return False

    return True


def _get_experiences(filename: str):
    experiences = []
    try:
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            local_vars = {}
            exec(code, {}, local_vars)
            i = 0
            for _, var_val in local_vars.items():
                if isinstance(var_val, dict):
                    i += 1
                    valid_exp = True
                    for key in ['batch_size', 'epochs', 'lr', 'optimizer', 'loss']:
                        if key not in var_val.keys():
                            print('ERROR! not saving experience #{}, missing a required field: {}'.format(i, key))
                            valid_exp = False
                            break
                    if valid_exp:
                        experiences.append(var_val)

        return experiences
    except FileNotFoundError:
        print('File: "{}" not found. Please make sure that filename parameter is correct'.format(filename))
        return None


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
    print('This directory is not a registered AKK project, please make sure you are issuing the command from the right directory.')
    print('If you did not initialize the project all you have to do is to run:')
    print('$ akk project init [-h: for more information]')


def _get_project_last_commit(path: str):
    repo = Repo(path)
    if repo.is_dirty():
        raise UncommitedChangesException()
    last_commit = None
    for commit in repo.iter_commits():
        last_commit = commit.name_rev[:10]
        break

    return last_commit


def _assemble_code(project, output_dir):
    # todo: add new attribute to project and new command argument to project init: entrypoint: main .py file, default: main.py
    project['entrypoint'] = 'main.py'
    importer = CodeSourceImporter(project['entrypoint'], project['path'], output_dir)
    importer.find_file_deps()
    importer.write_output()


def _write_exp_data(experience, path, last_commit):
    with open(os.path.join(path, '.akk', last_commit, 'temp.py'), 'w') as temp:
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
                elif line.strip() == '':
                    ppprev_space = pprev_space
                    pprev_space = prev_space
                    prev_space = 1
                else:
                    ppprev_space = pprev_space
                    pprev_space = prev_space
                    prev_space = 0

                if prev_space * pprev_space * ppprev_space == 0:
                    temp.write(line)

    os.remove(os.path.join(path, '.akk', last_commit, 'output.py'))
    shutil.move(os.path.join(path, '.akk', last_commit, 'temp.py'),
                os.path.join(path, '.akk', last_commit, 'output.py'))
    os.chmod(os.path.join(path, '.akk', last_commit, 'output.py'), 0o755)


# def new_project_handler(group=None, category=None, sort_by=None, page=1, search=None, csv_display=False):
def new_exp(filename: str):
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        _project_not_found()
    else:
        experiences = _get_experiences(filename)
        successes = 0
        failures = 0
        for experience in experiences:
            if _is_exp_valid(experience):
                try:
                    last_commit = _get_project_last_commit(path)
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
        last_commit = _get_project_last_commit(path)
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

    _write_exp_data(experience, path, last_commit)

    # todo: write the FKP project using the akk library.

    # todo: run profiling commit to measure the duration of each cycle.

    # todo: split into commits and run sequentially.


def stop_exp(*args, **kwargs):
    print('-' * 50)
    print('experience stop command / Not yet implemented')
    print('-' * 50)


def list_exp(*args, **kwargs):
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        _project_not_found()
    else:
        def lr_state(lr, lr_decay, lr_cycle):
            if lr_decay is not None:
                if lr_cycle is not None:
                    return 'D+R: {:.2f} / {:d}'.format(lr_decay, lr_cycle)
                else:
                    return 'Decay: {:.2f}'.format(lr_decay)
            else:
                return 'Const: {:.5f}'.format(lr)

        print('')
        print(' ' + '-' * 125)
        print(' | {:3s}  | {:24s} | {:10s} | {:10s} | {:14s} | {:10s} | {:16s} | {:12s} |'.format('#', 'Id', 'Batch Size', 'Epochs', 'Learning Rate', 'Optimizer', 'Loss Fct'
                                                                                                  , 'Status'))
        print(' ' + '-' * 125)
        i = 0
        for exp in orm.experiences.find({'project': str(project['_id'])}):
            i += 1
            print(' | {:3d}  | {:24s} | {:10d} | {:10d} | {:14s} | {:10s} | {:16s} | {:12s} |'.format(i, str(exp['_id']), exp['batch_size'], exp['epochs'],
                                                                                                      lr_state(exp['lr'], exp['lr_decay'], exp['lr_cycle']),
                                                                                                      exp['optimizer'], exp['loss'], exp['status']))
            print(' ' + '-' * 125)
        print('')


def status_exp(*args, **kwargs):
    print('-' * 50)
    print('experience status command / Not yet implemented')
    print('-' * 50)
