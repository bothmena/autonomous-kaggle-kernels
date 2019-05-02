from git import Repo
from akk.lib.exception import UncommitedChangesException


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
            for _, var_val in local_vars.items():
                if isinstance(var_val, dict) and is_exp_valid(var_val):
                    experiences.append(var_val)

        return experiences
    except FileNotFoundError:
        print('File: "{}" not found. Please make sure that filename parameter is correct'.format(filename))
        return None


def is_exp_valid(exp: dict):
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
