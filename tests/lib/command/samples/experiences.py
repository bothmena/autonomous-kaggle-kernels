# valid experience
experience_dic = {
    'batch_size'   : 64,
    'delta'        : 0.002,
    'k_r'          : 50,
    'k_d'          : 1,
    'nb_features'  : 64,
    'resnet_blocks': 4,
    'optimizer'    : 'adam',
    'steps'        : 50,
    'lr'           : 0.005,
    'networks'     : {
        'refiner'      : {
            'lr_decay'    : 0.6,
            'lr_cycle'    : 50,
            'loss'        : 'custom',
            'loss_args'   : {'a': 0, 'b': 1},
            'loss_sc'     : 'loss function source code, FUTURE feature',
            'loss_hash'   : 'loss function hash, FUTURE feature',
            'loss_version': 'loss function version, hash source code (str), try to find the same hash in the history of experiences, if not found create a new version, '
                            'FUTURE feature',
        },
        'discriminator': {
            'lr'       : 0.001,
            'optimizer': 'rmsprop',
            'opt_args' : {'alpha': 0.98},
            'loss'     : 'cross_entropy',
        },
    },
    'cycles'       : {
        'ref_pre_train' : {
            'steps'       : 1000,
            'unit_runtime': 40,
        },
        'disc_pre_train': {
            'unit_runtime': 20,
        },
        'combined_train': {
            'steps'       : 10000,
            'unit_runtime': 90,
        },
    },
}

# valid experience
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
            'steps'       : 200,
            'unit_runtime': 40,
        }
    },
}

# valid experience
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
            'steps'       : 200,
            'unit_runtime': 40,
        }
    },
}

# should be invalid: no batch size
experience_dic_4 = {
    'networks': {
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
    'cycles'  : {
        'cycle_0': {
            'steps'       : 200,
            'unit_runtime': 40,
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
            'steps'       : 200,
            'unit_runtime': 40,
        }
    },
}

# should be invalid: no optimizer
experience_dic_6 = {
    'batch_size': 128,
    'lr'        : 0.001,
    'lr_decay'  : 0.4,
    'lr_cycle'  : 40,
    'opt_args'  : {},
    'loss'      : 'cross_entropy',
    'loss_args' : {},
    'networks'  : {
        'net_0': {}
    },
    'cycles'    : {
        'cycle_0': {
            'steps'       : 200,
            'unit_runtime': 40,
        }
    },
}

# should be invalid: loss type is not str
experience_dic_7 = {
    'batch_size': 128,
    'lr'        : 0.001,
    'lr_decay'  : 0.4,
    'lr_cycle'  : 40,
    'optimizer' : 'adam',
    'opt_args'  : {},
    'loss'      : 548,
    'loss_args' : {},
    'networks'  : {
        'net_0': {}
    },
    'cycles'    : {
        'cycle_0': {
            'steps'       : 200,
            'unit_runtime': 40,
        }
    },
}

# should be invalid: no cycles
experience_dic_8 = {
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
}

# should be invalid: no networks
experience_dic_9 = {
    'batch_size': 128,
    'lr_decay'  : 0.4,
    'lr_cycle'  : 40,
    'optimizer' : 'adam',
    'opt_args'  : {},
    'loss'      : 'cross_entropy',
    'loss_args' : {},
    'cycles'    : {
        'cycle_0': {
            'steps'       : 200,
            'unit_runtime': 40,
        }
    },
}

# should be invalid: cycles not a dict
experience_dic_10 = {
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
    'cycles'    : 87,
}

# should be invalid: cycles content not a dict
experience_dic_11 = {
    'batch_size': 128,
    'lr'        : 0.4,
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
        'cycle': 87
    },
}

# should be invalid: networks not a dict
experience_dic_12 = {
    'batch_size': 128,
    'lr'        : 0.4,
    'lr_decay'  : 0.4,
    'lr_cycle'  : 40,
    'optimizer' : 'adam',
    'opt_args'  : {},
    'loss'      : 'cross_entropy',
    'loss_args' : {},
    'networks'  : 897,
    'cycles'    : {
        'cycle_0': {
            'steps'       : 200,
            'unit_runtime': 40,
        }
    },
}

# should be invalid: networks content not a dict
experience_dic_13 = {
    'batch_size': 128,
    'lr'        : 0.4,
    'lr_decay'  : 0.4,
    'lr_cycle'  : 40,
    'optimizer' : 'adam',
    'opt_args'  : {},
    'loss'      : 'cross_entropy',
    'loss_args' : {},
    'networks'  : {
        'net_0': 85
    },
    'cycles'    : {
        'cycle_0': {
            'steps'       : 200,
            'unit_runtime': 40,
        }
    },
}

# should be invalid: cycle step not an int
experience_dic_14 = {
    'batch_size': 128,
    'lr'        : 0.4,
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
            'steps'       : '200',
            'unit_runtime': 40,
        }
    },
}
