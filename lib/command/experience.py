import os
from lib.services.db import MongodbORM
from lib.exception.database import ExperienceExistsException


orm = MongodbORM()


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


# def new_project_handler(group=None, category=None, sort_by=None, page=1, search=None, csv_display=False):
def init_exp(filename: str):
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        print('This directory is not a registered AKK project, please make sure you are issuing the command from the right directory.')
        print('If you did not initialize the project all you have to do is to run:')
        print('$ akk project init [-h: for more information]')
    else:
        experiences = _get_experiences(filename)
        successes = 0
        failures = 0
        for experience in experiences:
            experience = _fill_experience(experience)
            experience['project'] = str(project['_id'])
            experience['search_space'] = None
            experience['status'] = 'Not started'  # queued / running / stopped / completed
            try:
                orm.new_experience(experience)
                successes += 1
            except ExperienceExistsException:
                failures += 1

        print('Experiences saved successfully:', successes)
        print('Experiences that already exist:', failures)


def status_exp(*args, **kwargs):
    print('-' * 50)
    print('experience status command / Not yet implemented')
    print('-' * 50)


def start_exp(*args, **kwargs):
    print('-' * 50)
    print('experience start command / Not yet implemented')
    print('-' * 50)


def stop_exp(*args, **kwargs):
    print('-' * 50)
    print('experience stop command / Not yet implemented')
    print('-' * 50)


def list_exp(*args, **kwargs):
    path = os.getcwd()
    project = orm.get_project(path)
    if project is None:
        print('This directory is not a registered AKK project, please make sure you are issuing the command from the right directory.')
        print('If you did not initialize the project all you have to do is to run:')
        print('$ akk project init [-h: for more information]')
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

###########################################################
#  Code to use to assemble project code in a single file  #
###########################################################

# from lib.command.source_code import CodeSourceImporter
#
#
# class Push:
#     def __init__(self, project_dir, main_fn: str = 'main'):
#         self.project_dir = project_dir
#         self.main_fn = main_fn
#
#     def push_code(self):
#         importer = CodeSourceImporter(self.main_fn, self.project_dir)
#         importer.find_file_deps()
#         importer.write_output()
#
#
# pusher = Push('/opt/project/examples')
# pusher.push_code()
