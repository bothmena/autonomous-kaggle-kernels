from unittest import TestCase
from lib.command.commit import CodeSourceImporter


class TestCommit(TestCase):

    def test_get_pkg_modules(self):
        self.assertListEqual(
            list(zip([None], ['aa'])),
            list(CodeSourceImporter.get_pkg_modules('import aa')),
            "Failed test 1"
        )
        self.assertEqual(
            list(zip(['package'] * 3, ['aa', 'bb', 'cc'])),
            list(CodeSourceImporter.get_pkg_modules('from package import aa, bb, cc')),
            "Failed test 2"
        )
        self.assertEqual(
            list(zip([None], ['aa'])),
            list(CodeSourceImporter.get_pkg_modules('   import aa  \n\n')),
            "Failed test 3"
        )
        self.assertEqual(
            list(zip(['package'] * 3, ['aa', 'bb', 'cc'])),
            list(CodeSourceImporter.get_pkg_modules('   from package import aa, bb, cc   ')),
            "Failed test 4"
        )
        self.assertEqual(
            list(zip(['package'] * 3, ['aa', 'bb', 'cc'])),
            list(CodeSourceImporter.get_pkg_modules('   from    package    import aa, bb, cc \n\n')),
            "Failed test 5"
        )
        self.assertEqual(
            list(zip(['package'] * 3, ['aa', 'bb', 'cc'])),
            list(CodeSourceImporter.get_pkg_modules('   from    package    import aa, bb, cc \n\n')),
            "Failed test 6"
        )
        self.assertEqual(
            list(zip([None] * 3, ['aa', 'bb', 'cc'])),
            list(CodeSourceImporter.get_pkg_modules('   import aa, bb, cc \n\n')),
            "Failed test 7"
        )
        self.assertListEqual(
            list(zip([None, None], ['aa', 'bb'], ['a', 'b'])),
            list(CodeSourceImporter.get_pkg_modules('   import   aa    as   a  ,   bb   as   b   \n')),
            "Failed test 8, the method does not handle aliases correctly"
        )
        self.assertListEqual(
            list(zip(['package'] * 2, ['aa', 'bb'], ['a', 'b'])),
            list(CodeSourceImporter.get_pkg_modules('   from   package    import    aa   as   a  ,    bb   as   b  \n\t\n')),
            "Failed test 9, the method does not handle aliases correctly"
        )
