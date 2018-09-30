""" DDB util module"""
from models.app_build_info_model import ApplicationBuildInfo
import logging


logger = logging.getLogger('_DdbUtil_')

def is_log_table_exists():
    return ApplicationBuildInfo.exists()


def create_table():
    if not ApplicationBuildInfo.exists():
        logger.infao("Table does not exists, creating table.. ")
        ApplicationBuildInfo.create_table(wait=True, read_capacity_units=10, write_capacity_units=10)
        logger.infao("Table created")
        return
    logger.info("Table already exists.")


def save_build_info(item):
    create_table()
    logger.info(f"Saving item: {item}")
    item.save()
    logger.info("Item saved.")


def find_info_item(commit_it):
    for item in ApplicationBuildInfo.query(commit_it):
        print(item.build_info)


def load_all_build_info(model):
    return model.scan()

    # for item in model.scan():
    #     print(item)
