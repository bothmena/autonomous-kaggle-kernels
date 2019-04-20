# def new_project_handler(group=None, category=None, sort_by=None, page=1, search=None, csv_display=False):
def init_exp(*args, **kwargs):
    print('-' * 50)
    print('experience init command / Not yet implemented')
    print('-' * 50)


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
    print('-' * 50)
    print('experience list command / Not yet implemented')
    print('-' * 50)


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
