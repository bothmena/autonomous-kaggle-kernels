from git import Repo
from akk.lib.exception import UncommitedChangesException
import logging


def get_project_last_commit(path: str):
    repo = Repo(path)
    if repo.is_dirty():
        raise UncommitedChangesException()
    last_commit = None
    for commit in repo.iter_commits():
        last_commit = commit.name_rev[:10]
        break

    return last_commit


def get_experiences(filename: str):
    experiences = []
    try:
        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            local_vars = {}
            exec(code, {}, local_vars)
            for var_name, var_val in local_vars.items():
                # todo: add a verbose arg to commands and replace print() with logging.info()
                print('---> checking experience `{}` validity'.format(var_name))
                if isinstance(var_val, dict) and is_exp_valid(var_val):
                    experiences.append(var_val)

        return experiences
    except FileNotFoundError:
        print('File: "{}" not found. Please make sure that filename parameter is correct'.format(filename))
        return None


def is_exp_valid(exp: dict):
    for key, tp in {'batch_size': int, 'cycles': dict, 'networks': dict}.items():
        # check that all required keys exist in exp dict
        if key not in exp.keys():
            logging.error('\texperience is missing a required key: {}'.format(key))
            return False
        # check all required keys have the correct type
        elif not isinstance(exp[key], tp):
            logging.error('\texperience does not have the right type for key: {}'.format(key))
            return False

    for net_name, hps in exp['networks'].items():
        if not isinstance(hps, dict):
            logging.error('\tnetwork {} is not a dictionary'.format(net_name))
            return False
        for key, tp in {'lr': float, 'optimizer': str, 'loss': str}.items():
            if key in hps.keys():
                if not isinstance(hps[key], tp):
                    logging.error('\tnetwork {} does not have the right type for key: {}, defined in network dict'.format(net_name, key))
                    return False
            elif key in exp.keys():
                if not isinstance(exp[key], tp):
                    logging.error('\tnetwork {} does not have the right type for key: {}, defined in experience dict'.format(net_name, key))
                    return False
            else:
                logging.error('\tnetwork {} is missing a required key: {}'.format(net_name, key))
                return False

    for cycle_name, items in exp['cycles'].items():
        if not isinstance(items, dict):
            logging.error('\tcycle {} is not a dictionary'.format(cycle_name))
            return False
        for key, tp in {'steps': int, 'index': int}.items():
            # if key is in the cycle dict, make sure the type is correct
            if key in items.keys():
                if not isinstance(items[key], tp):
                    logging.error('\tcycle {} does not have the right type for key: {}, defined in cycle dict'.format(cycle_name, key))
                    return False
            # if key is not in the cycle dict but defined in the exp dict, make sure the type is correct
            elif key in exp.keys():
                if not isinstance(exp[key], tp):
                    logging.error('\tcycle {} does not have the right type for key: {}, defined in experience dict'.format(cycle_name, key))
                    return False
            else:
                logging.error('\tcycle {} is missing a required key: {}'.format(cycle_name, key))
                return False

    return True


def project_not_found():
    print('This directory is not a registered AKK project, please make sure you are issuing the cli from the right directory.')
    print('If you did not initialize the project all you have to do is to run:')
    print('$ akk project init [-h: for more information]')
