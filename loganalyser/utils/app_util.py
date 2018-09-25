from models.app_build_info_model import ApplicationBuildInfo


def create_table():
    if not ApplicationBuildInfo.exists():
        ApplicationBuildInfo.create_table(wait=True, read_capacity_units=10, write_capacity_units=10)
        print("Table Created !!")
    else:
        print("Table Already Present !!")


def save_build_info(item):
    create_table()
    print("saving table item")
    item.save()
    print("item saved")


def find_info_item(commit_it):
    for item in ApplicationBuildInfo.query(commit_it):
        print(item.build_info)

