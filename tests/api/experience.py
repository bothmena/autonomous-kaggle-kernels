from unittest import TestCase
from akk.api.experience import PyTorchExperience
from torch import nn
from torch import optim
from akk.cli.experience import is_exp_valid
from ..cli.samples import experience_dic, experience_dic_2, experience_dic_3, experience_dic_4, experience_dic_5, experience_dic_6, experience_dic_7, \
    experience_dic_8, experience_dic_9, experience_dic_10, experience_dic_11, experience_dic_12, experience_dic_13


class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.seq = nn.Sequential(
            nn.Linear(10, 100),
            nn.Linear(100, 10)
        )

    def forward(self, x):
        pass


class ExperienceTest(TestCase):

    def test_set_attributes(self):

        exp = PyTorchExperience(**experience_dic)

        # test batch_size + other attributes on depth = 0
        self.assertEqual(exp.batch_size, experience_dic['batch_size'])
        self.assertEqual(exp.get_hp('delta'), 0.002)
        self.assertEqual(exp.get_hp('resnet_blocks'), 4)

        # test optimizer + loss function for both networks: make sure it chooses the right place to get the needed value
        self.assertEqual(exp.optimizer('refiner'), 'adam')
        self.assertEqual(exp.optimizer('discriminator'), 'rmsprop')

        self.assertEqual(exp.opt_args('refiner'), {})
        self.assertEqual(exp.opt_args('discriminator'), {'alpha': 0.98})

        self.assertEqual(exp.loss('refiner'), 'custom')
        self.assertEqual(exp.loss('discriminator'), 'cross_entropy')

        self.assertEqual(exp.loss_args('refiner'), {'a': 0, 'b': 1})
        self.assertEqual(exp.loss_args('discriminator'), {})

        self.assertIsNone(exp.get_loss(net_id='refiner'))
        self.assertIsInstance(exp.get_loss('discriminator'), nn.CrossEntropyLoss)

        self.assertIsInstance(exp.get_optimizer(Network().parameters(), net_id='refiner'), optim.Adam)
        self.assertIsInstance(exp.get_optimizer(Network().parameters(), net_id='discriminator'), optim.RMSprop)

        # test lr, lr_decay, lr_cycle
        self.assertEqual(exp.lr('refiner'), 0.005)
        self.assertEqual(exp.lr('discriminator'), 0.001)

        self.assertEqual(exp.lr_decay('refiner'), 0.6)
        self.assertIsNone(exp.lr_decay('discriminator'))

        self.assertEqual(exp.lr_cycle('refiner'), 50)
        self.assertIsNone(exp.lr_cycle('discriminator'), 'rmsprop')

        self.assertEqual(exp.get_lr('discriminator'), 0.001)

        # test cycle steps
        self.assertEqual(exp.steps('ref_pre_train'), 1000)
        self.assertEqual(exp.steps('disc_pre_train'), 50)
        self.assertEqual(exp.steps('combined_train'), 10000)

    def test_experience_validity(self):
        for i, valid_exp in enumerate([experience_dic, experience_dic_2, experience_dic_3]):
            self.assertTrue(is_exp_valid(valid_exp), "Experience #{} in list is not valid".format(i))

        exps = [experience_dic_4, experience_dic_5, experience_dic_6, experience_dic_7, experience_dic_8, experience_dic_9, experience_dic_10, experience_dic_11,
                 experience_dic_12, experience_dic_13]
        for i, invalid_exp in enumerate(exps):
            self.assertFalse(is_exp_valid(invalid_exp), "Experience #{} in list is valid".format(i))

    def test_lr_decay(self):
        pass

    def test_lr_restarts(self):
        pass
