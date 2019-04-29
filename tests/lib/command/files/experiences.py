experience_dic = {
    'batch_size': 64,
    'delta': 0.002,
    'k_r': 50,
    'k_d': 1,
    'nb_features': 64,
    'resnet_blocks': 4,
    'networks'  : {
        'refiner'      : {
            'lr'       : 0.005,
            'lr_decay' : 0.6,
            'lr_cycle' : 50,
            'optimizer': 'adam',
            'opt_args' : {},
            'loss'     : 'custom',
            'loss_sc'     : 'loss function source code, FUTURE feature',
            'loss_hash'   : 'loss function hash, FUTURE feature',
            'loss_version': 'loss function version, hash source code (str), try to find the same hash in the history of experiences, if not found create a new version, '
                            'FUTURE feature',
            'loss_args': {},
        },
        'discriminator': {
            'lr'          : 0.005,
            'lr_decay'    : 0.6,
            'lr_cycle'    : 50,
            'optimizer'   : 'adam',
            'opt_args'    : {},
            'loss'        : 'custom',
            'loss_sc'     : 'FUTURE feature',
            'loss_hash'   : 'FUTURE feature',
            'loss_version': 'FUTURE feature',
            'loss_args'   : {},
        },
    },
    'cycles'    : {
        'ref_pre_train': {
            'steps'            : 1000,
            'unit_running_time': 40,
        },
        'disc_pre_train': {
            'steps'            : 200,
            'unit_running_time': 20,
        },
        'combined_train': {
            'steps'            : 10000,
            'unit_running_time': 90,
        },
    },
}

experience_dic_2 = {
    'batch_size': 64,
    'networks'  : {
        'net_0': {
            'lr'       : 0.005,
            'lr_decay' : 0.6,
            'lr_cycle' : 50,
            'optimizer': 'adam',
            'opt_args' : {},
            'loss'     : 'cross_entropy',
            'loss_args': {},
        }
    },
    'cycles'    : {
        'cycle_0': {
            'steps'            : 200,
            'unit_running_time': 40,
        }
    },
}

experience_dic_3 = {
    'batch_size': 128,
    'lr'        : 0.001,
    'lr_decay'  : 0.4,
    'lr_cycle'  : 40,
    'optimizer' : 'adam',
    'opt_args'  : {},
    'loss'      : 'cross_entropy',
    'loss_args' : {},
    'networks'  : {
        'net_0': {}
    },
    'cycles'    : {
        'cycle_0': {
            'steps'            : 200,
            'unit_running_time': 40,
        }
    },
}

# should be invalid: no batch size
experience_dic_4 = {
    'networks'  : {
        'net_0': {
            'lr'       : 0.005,
            'lr_decay' : 0.6,
            'lr_cycle' : 50,
            'optimizer': 'adam',
            'opt_args' : {},
            'loss'     : 'cross_entropy',
            'loss_args': {},
        }
    },
    'cycles'    : {
        'cycle_0': {
            'steps'            : 200,
            'unit_running_time': 40,
        }
    },
}

# should be invalid: no lr
experience_dic_5 = {
    'batch_size': 128,
    'lr_decay'  : 0.4,
    'lr_cycle'  : 40,
    'optimizer' : 'adam',
    'opt_args'  : {},
    'loss'      : 'cross_entropy',
    'loss_args' : {},
    'networks'  : {
        'net_0': {}
    },
    'cycles'    : {
        'cycle_0': {
            'steps'            : 200,
            'unit_running_time': 40,
        }
    },
}

# should be invalid: no lr
experience_dic_6 = {
    'batch_size': 128,
    'lr_decay'  : 0.4,
    'lr_cycle'  : 40,
    'optimizer' : 'adam',
    'opt_args'  : {},
    'loss'      : 'cross_entropy',
    'loss_args' : {},
    'networks'  : {
        'net_0': {}
    },
    'cycles'    : {
        'cycle_0': {
            'steps'            : 200,
            'unit_running_time': 40,
        }
    },
}
