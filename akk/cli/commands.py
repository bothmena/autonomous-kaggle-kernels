#!/opt/conda/bin/python
import argparse
from akk.cli import experience, project, search_space


def main():
    parser = argparse.ArgumentParser(description='Autonomous Kaggle Kernels CLI', prog='akk', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-v', '--version', action='version', version='Autonomous Kaggle Kernels CLI - %(prog)s - v0.1')

    subparsers = parser.add_subparsers(title='commands', dest='cli')
    subparsers.required = True
    subparsers.choices = Help.akk_choices

    parse_project(subparsers)
    parse_experience(subparsers)
    parse_search_space(subparsers)

    args = parser.parse_args()
    command_args = {}
    command_args.update(vars(args))
    del command_args['func']
    del command_args['cli']
    error = False
    try:
        out = args.func(**command_args)
    except ValueError as e:
        print(e)
        out = None
        error = True
    except KeyboardInterrupt:
        print('User cancelled operation')
        out = None
    if out is not None:
        print(out, end='')

    # This is so that scripts that pick up on error codes can tell when there was a failure
    if error:
        exit(1)


def parse_project(subparsers):
    parser_project = subparsers.add_parser('project', formatter_class=argparse.RawTextHelpFormatter, help=Help.project, aliases=['p'])
    subparsers_project = parser_project.add_subparsers(title='commands', dest='cli')
    subparsers_project.required = True
    subparsers_project.choices = Help.project_choices

    # project init
    parser_project_init = subparsers_project.add_parser('init', formatter_class=argparse.RawTextHelpFormatter, help=Help.project_init)
    parser_project_init_opt = parser_project_init._action_groups.pop()

    for kwargs in Help.project_init_args:
        args = kwargs['args']
        del kwargs['args']
        parser_project_init_opt.add_argument(*args, **kwargs)

    parser_project_init._action_groups.append(parser_project_init_opt)
    parser_project_init.set_defaults(func=project.init_project)

    # project status
    parser_project_status = subparsers_project.add_parser('status', formatter_class=argparse.RawTextHelpFormatter, help=Help.project_status)
    parser_project_status_opt = parser_project_status._action_groups.pop()

    for kwargs in Help.project_status_args:
        args = kwargs['args']
        del kwargs['args']
        parser_project_status_opt.add_argument(*args, **kwargs)

    parser_project_status._action_groups.append(parser_project_status_opt)
    parser_project_status.set_defaults(func=project.status_project)

    # project update
    parser_project_update = subparsers_project.add_parser('update', formatter_class=argparse.RawTextHelpFormatter, help=Help.project_update)
    parser_project_update_opt = parser_project_update._action_groups.pop()

    for kwargs in Help.project_update_args:
        args = kwargs['args']
        del kwargs['args']
        parser_project_update_opt.add_argument(*args, **kwargs)

    parser_project_update._action_groups.append(parser_project_update_opt)
    parser_project_update.set_defaults(func=project.update_project)

    # project list
    parser_project_list = subparsers_project.add_parser('list', formatter_class=argparse.RawTextHelpFormatter, help=Help.project_list)
    parser_project_list_opt = parser_project_list._action_groups.pop()

    for kwargs in Help.project_list_args:
        args = kwargs['args']
        del kwargs['args']
        parser_project_list_opt.add_argument(*args, **kwargs)

    parser_project_list._action_groups.append(parser_project_list_opt)
    parser_project_list.set_defaults(func=project.list_project)


def parse_experience(subparsers):
    parser_exp = subparsers.add_parser('experience', formatter_class=argparse.RawTextHelpFormatter, help=Help.exp, aliases=['e'])
    subparsers_exp = parser_exp.add_subparsers(title='commands', dest='cli')
    subparsers_exp.required = True
    subparsers_exp.choices = Help.exp_choices

    # experience new
    parser_exp_new = subparsers_exp.add_parser('new', formatter_class=argparse.RawTextHelpFormatter, help=Help.exp_new)
    parser_exp_new_opt = parser_exp_new._action_groups.pop()

    for kwargs in Help.exp_new_args:
        args = kwargs['args']
        del kwargs['args']
        parser_exp_new_opt.add_argument(*args, **kwargs)

    parser_exp_new._action_groups.append(parser_exp_new_opt)
    parser_exp_new.set_defaults(func=experience.new_exp)

    # experience status
    parser_exp_status = subparsers_exp.add_parser('status', formatter_class=argparse.RawTextHelpFormatter, help=Help.exp_status)
    parser_exp_status_opt = parser_exp_status._action_groups.pop()

    for kwargs in Help.exp_status_args:
        args = kwargs['args']
        del kwargs['args']
        parser_exp_status_opt.add_argument(*args, **kwargs)

    parser_exp_status._action_groups.append(parser_exp_status_opt)
    parser_exp_status.set_defaults(func=experience.status_exp)

    # experience start
    parser_exp_start = subparsers_exp.add_parser('start', formatter_class=argparse.RawTextHelpFormatter, help=Help.exp_start)
    parser_exp_start_opt = parser_exp_start._action_groups.pop()

    for kwargs in Help.exp_start_args:
        args = kwargs['args']
        del kwargs['args']
        parser_exp_start_opt.add_argument(*args, **kwargs)

    parser_exp_start._action_groups.append(parser_exp_start_opt)
    parser_exp_start.set_defaults(func=experience.start_exp)

    # experience stop
    parser_exp_stop = subparsers_exp.add_parser('stop', formatter_class=argparse.RawTextHelpFormatter, help=Help.exp_stop)
    parser_exp_stop_opt = parser_exp_stop._action_groups.pop()

    for kwargs in Help.exp_stop_args:
        args = kwargs['args']
        del kwargs['args']
        parser_exp_stop_opt.add_argument(*args, **kwargs)

    parser_exp_stop._action_groups.append(parser_exp_stop_opt)
    parser_exp_stop.set_defaults(func=experience.stop_exp)

    # experience list
    parser_exp_list = subparsers_exp.add_parser('list', formatter_class=argparse.RawTextHelpFormatter, help=Help.exp_list)
    parser_exp_list_opt = parser_exp_list._action_groups.pop()

    for kwargs in Help.exp_list_args:
        args = kwargs['args']
        del kwargs['args']
        parser_exp_list_opt.add_argument(*args, **kwargs)

    parser_exp_list._action_groups.append(parser_exp_list_opt)
    parser_exp_list.set_defaults(func=experience.list_exp)


def parse_search_space(subparsers):
    parser_ss = subparsers.add_parser('search-space', formatter_class=argparse.RawTextHelpFormatter, help=Help.ss, aliases=['ss'])
    subparsers_ss = parser_ss.add_subparsers(title='commands', dest='cli')
    subparsers_ss.required = True
    subparsers_ss.choices = Help.ss_choices

    # search-space expand
    parser_ss_expand = subparsers_ss.add_parser('expand', formatter_class=argparse.RawTextHelpFormatter, help=Help.ss_expand)
    parser_ss_expand_opt = parser_ss_expand._action_groups.pop()

    for kwargs in Help.ss_expand_args:
        args = kwargs['args']
        del kwargs['args']
        parser_ss_expand_opt.add_argument(*args, **kwargs)

    parser_ss_expand._action_groups.append(parser_ss_expand_opt)
    parser_ss_expand.set_defaults(func=search_space.expand_ss)

    # search-space run
    parser_ss_run = subparsers_ss.add_parser('run', formatter_class=argparse.RawTextHelpFormatter, help=Help.ss_run)
    parser_ss_run_opt = parser_ss_run._action_groups.pop()

    for kwargs in Help.ss_run_args:
        args = kwargs['args']
        del kwargs['args']
        parser_ss_run_opt.add_argument(*args, **kwargs)

    parser_ss_run._action_groups.append(parser_ss_run_opt)
    parser_ss_run.set_defaults(func=search_space.run_ss)

    # search-space list
    parser_ss_list = subparsers_ss.add_parser('list', formatter_class=argparse.RawTextHelpFormatter, help=Help.ss_list)
    parser_ss_list_opt = parser_ss_list._action_groups.pop()

    for kwargs in Help.ss_list_args:
        args = kwargs['args']
        del kwargs['args']
        parser_ss_list_opt.add_argument(*args, **kwargs)

    parser_ss_list._action_groups.append(parser_ss_list_opt)
    parser_ss_list.set_defaults(func=search_space.list_ss)


class Help:
    akk_choices = ['project', 'p', 'experience', 'e', 'search-space', 'ss']
    project_choices = ['init', 'status', 'update', 'list']
    exp_choices = ['new', 'status', 'start', 'stop', 'list']
    ss_choices = ['expand', 'list', 'run']

    project = 'Manage your projects'
    project_init = 'Initiate a new project'
    project_status = 'Check the status of the project'
    project_update = 'Update project info and settings'
    project_list = 'List all the projects'

    exp = 'Manage your project experiences'
    exp_new = 'Create a new experience'
    exp_start = 'Assemble code if not already assembled then start running an experience on kaggle kernels'
    exp_stop = 'Stop an experience, this will stop the experience from running further commits.'
    exp_list = 'List a project experiences, you can also list an experience\'s commits and their status'
    exp_status = 'Check the status of experiences'

    ss = 'Manage hyper parameters and net architecture search spaces'
    ss_run = 'Launch multiple experiences from a search space'
    ss_expand = 'Expand a search space into experiences'
    ss_list = 'List project\'s search spaces, and search space\'s experiences'

    project_init_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique and less than 50 and longer than 5 characters, default: first 50 characters of the name of the directory',
        },
        {
            'args': ['-a', '--alias'],
            'dest': 'alias',
            'required': False,
            'default': None,
            'help': 'Alias of the new project, it should be less than 25 characters, default: first 25 characters of project name',
        },
        {
            'args': ['-p', '--path'],
            'dest': 'path',
            'required': False,
            'help': 'Absolute path of the directory containing the project, default working directory',
            'default': '.',
        },
        {
            'args': ['-r', '--repository'],
            'dest': 'repository',
            'required': False,
            'help': 'Url of the repository where the project is stored',
        },
        {
            'args': ['-k', '--framework'],
            'dest': 'framework',
            'default': 'pytorch',
            'choices': ['pytorch', 'tensorflow', 'keras'],
            'help': 'Deep Learning framework in use, choose from pytorch/tensorflow/keras, default pytorch',
        },
        {
            'args': ['--cpu'],
            'dest': 'cpu',
            'required': False,
            'help': 'Use cpu for training instead of GPU, default: False',
            'action': 'store_true',
        },
        {
            'args': ['--internet'],
            'dest': 'internet',
            'required': False,
            'help': 'Enable the internet access for the kernel, default: False',
            'action': 'store_true',
        },
    ]
    project_status_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique, default: name of the directory',
        },
    ]
    project_update_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique, default: name of the directory',
        },
    ]
    project_list_args = []

    exp_new_args = [
        {
            'args': ['-f', '--filename'],
            'dest': 'filename',
            'required': True,
            'help': 'Path to the file where the experience dictionary is defined.',
        },
    ]
    exp_status_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique, default: name of the directory',
        },
    ]
    exp_start_args = [
        {
            'args': ['exp_id'],
            'help': 'Id of the experience to be started',
        },
    ]
    exp_stop_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique, default: name of the directory',
        },
    ]
    exp_list_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique, default: name of the directory',
        },
    ]

    ss_expand_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique, default: name of the directory',
        },
    ]
    ss_list_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique, default: name of the directory',
        },
    ]
    ss_run_args = [
        {
            'args': ['-n', '--name'],
            'dest': 'name',
            'required': False,
            'help': 'Name of the new project, it should be unique, default: name of the directory',
        },
    ]


if __name__ == '__main__':
    main()
