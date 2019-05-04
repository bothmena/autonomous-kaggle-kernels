from akk.lib.services import MongodbORM


orm = MongodbORM()


def clean_db(level: int):
    if level >= 1:
        print('cleaning commits...')
        orm.commits.delete_many({})
        print('done cleaning commits.')
    if level >= 2:
        print('cleaning experiences...')
        orm.experiences.delete_many({})
        print('done cleaning experiences.')
    if level >= 3:
        print('cleaning search spaces...')
        orm.search_spaces.delete_many({})
        print('done cleaning search spaces.')
    if level >= 4:
        print('cleaning projects...')
        orm.projects.delete_many({})
        print('done cleaning projects.')
