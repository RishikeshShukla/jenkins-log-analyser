from utils.enums import Status, IssueType
from datetime import datetime
import json


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


if __name__ == "__main__":

    print("creating table")
    create_table()

    # json_data = {"buildId": "134", "committer_id": "rshukla", "log_report": "build is successful!!"}
    # build_info = json.dumps(json_data)
    # item = ApplicationBuildInfo()
    # item.commit_build_id = 'abcdef1234ghi_168'
    # item.application_name = 'login'
    # item.application_type = 'web-app'
    # item.build_info = build_info
    # item.status = str(Status.success)
    # item.issue_type = str(IssueType.na)
    # item.build_date_time = datetime.now()
    # item.environment = "dev"
    #
    # save_build_info(item)

