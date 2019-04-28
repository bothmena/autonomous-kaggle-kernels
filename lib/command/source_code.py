import os
import importlib
import inspect
from lib.exception.implementation import NoExperienceException, ManyExperiencesException


class CodeSourceImporter:
    def __init__(self, main_fn: str, project_dir: str, output_fn: str = 'output.py', mark_cells: bool = False):
        """
        :param main_fn: main python file filename
        :param project_dir: where the main file is located.
        :param output_fn: output file filename
        """
        self.main_fn = main_fn
        if project_dir[-1] == '/':
            project_dir = project_dir[:-1]
        self.project_dir = project_dir
        if not output_fn.endswith('.py'):
            output_fn += '.py'
        self.output_fn = output_fn
        self.mark_cells = mark_cells

        self.local_imports = {}
        self.imports = set()

    @classmethod
    def get_pkg_modules(cls, import_statement: str) -> zip:
        """
        for a given import statement it returns a zip of every module and it's corresponding package if it exists
        examples: "from package import a, b, c" => zip(['package', 'package', 'package'], ['a', 'b', 'c'])
                  "import a, b => zip([None, None], ['a', 'b'])

        :param import_statement: import statement as a string
        :return: zip object of every module and it's corresponding package
        """
        import_statement = import_statement.strip()
        parts = import_statement.split()
        for i in range(len(parts)):
            if parts[i] == 'as':
                parts[i] = '__'
        if import_statement.startswith('from '):
            pkg = parts[1]
            modules = ''.join(parts[3:])
        else:
            pkg = None
            modules = ''.join(parts[1:])

        modules_parts = []
        aliases = []
        for mod_part in modules.split(','):
            if '__' in mod_part:
                m, a = mod_part.split('__')
            else:
                m, a = mod_part, None
            modules_parts.append(m)
            aliases.append(a)

        return zip([pkg] * len(modules_parts), modules_parts, aliases)

    def get_imports(self, line: str) -> list:
        relative_imports = []
        if line.startswith('from .'):
            z = self.get_pkg_modules(line)
            for pkg, mod, _ in z:
                relative_imports.append(pkg[1:] + '.' + mod)
        elif line.startswith(('import', 'from')):
            z = self.get_pkg_modules(line)
            for pkg, mod, alias in z:
                self.imports.add((pkg, mod, alias))

        return relative_imports

    def add_prioritized_dep(self, dep: str, priority: int) -> None:
        """
        Add new dependencies to the deps dictionary if it does not exist, if the dependency already exists,
        it updates it's priority, only the highest priority will be kept.
        :param dep: dependency, from an import statement
        :param priority: priority of the dependency, on which the import order will be based
        """
        if self.local_imports.get(dep) is None:
            self.local_imports[dep] = priority
        else:
            if priority > self.local_imports.get(dep):
                self.local_imports[dep] = priority

    def find_file_deps(self, filename: str = None, depth: int = 0) -> None:
        """
        Loop through the main and relative imports source to build the dependency tree
        :param filename:
        :param depth:
        :return:
        """
        if filename is None:
            filename = self.main_fn
        paths = filename.split('.')
        if len(paths) > 1:
            paths = paths[:-1]
        paths[-1] += '.py'
        abs_path = os.path.join(self.project_dir, *paths)
        if os.path.isfile(abs_path):
            with open(abs_path, 'r') as f:
                for line in f.readlines():
                    ri = self.get_imports(line)
                    for item in ri:
                        item = item.strip()
                        self.find_file_deps(item, depth + 1)
                        self.add_prioritized_dep(item, depth + 1)

    def get_import_statements(self):
        """
        :return: the import statement as a string
        """
        for pkg, mod, alias in self.imports:
            if pkg is None:
                yield 'import {}'.format(mod) if alias is None else 'import {} as {}'.format(mod, alias)
            else:
                yield 'from {} import {}'.format(pkg, mod) if alias is None else 'from {} import {} as {}'.format(pkg, mod, alias)

    def get_ri_source_code(self):
        """
        :return: the source code of the relative imports
        """
        experiences = 0
        for module in sorted(self.local_imports, key=self.local_imports.get, reverse=True):
            parts = module.split('.')
            pkg = os.path.basename(self.project_dir)
            imp_st = '{}.{}'.format(pkg, '.'.join(parts[:-1]))

            imp = importlib.import_module(imp_st)
            obj = eval('imp.' + parts[-1])

            if isinstance(obj, dict):
                is_experience = True
                for key in ['batch_size', 'epochs', 'lr', 'optimizer', 'loss']:
                    if key not in obj.keys():
                        print('ERROR! not saving experience #{}, missing a required field: {}'.format(i, key))
                        is_experience = False
                        break
                if is_experience:
                    experiences += 1
                    continue

            yield inspect.getsource(obj).strip()

        if experiences == 0:
            raise NoExperienceException()
        elif experiences > 1:
            raise ManyExperiencesException()

    def write_output(self):
        with open(os.path.join(self.project_dir, self.output_fn), 'w') as output:
            output.write('# __imp__\n')
            for line in self.get_import_statements():
                if self.mark_cells:
                    output.write('# __cell__\n')
                output.write(line + '\n')
            output.write('\n\n')

            output.write('# __dec__\n')
            for sc in self.get_ri_source_code():
                if self.mark_cells:
                    output.write('# __cell__\n')
                output.write(sc + '\n\n\n')

            output.write('# __mc__\n')
            with open(os.path.join(self.project_dir, self.main_fn + '.py'), 'r') as f:
                for line in f.readlines():
                    if not line.startswith(('from ', 'import ')):
                        line = line.rstrip()
                        if len(line) == 0:
                            output.write('\n# __cell__\n' if self.mark_cells else '\n')
                        else:
                            output.write(line.rstrip() + '\n')
