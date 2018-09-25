import json
import os
from builtins import print

from dateutil import parser
from file_read_backwards import FileReadBackwards

import utils.app_util as utils
from models.app_build_info_model import ApplicationBuildInfo
from models.app_build_info_model import BuildInfo
from utils.enums import IssueType

root_folder = "/home/ubuntu/jenkins-logs/"
apps_folder = "applications"

base_log_dir = os.path.join(root_folder, apps_folder)

# list of log directories to be process
log_dirs_to_processed = []

date_dir_marked_to_be_done = set()


def get_log_directories(app_log_dir):
    for log_date in os.listdir(app_log_dir):
        date_wise_log_dir = os.path.join(app_log_dir, log_date)
        if '.done' not in os.listdir(date_wise_log_dir):
            before_count = len(log_dirs_to_processed)
            for build_id in os.listdir(date_wise_log_dir):
                build_log_dir = os.path.join(date_wise_log_dir, build_id)
                if '.done' not in os.listdir(build_log_dir):
                    log_dirs_to_processed.append(build_log_dir)
            after_count = len(log_dirs_to_processed)

            if before_count == after_count:
                # mark dir app_log_date_loc as done
                mark_dir_processed(date_wise_log_dir)


def get_log_file_path(log_file_path):
    for item in os.listdir(log_file_path):
        log_file = os.path.join(log_file_path, item)
        if os.path.isfile(log_file) and "final" in log_file:
            return log_file


def process_log_file(file):
    '''
    :param file:
    :return: str
     1. load log file from down [Do not load whole file in once load line by line from bottom]
     2.  Check last line []
    '''
    with FileReadBackwards('wfo-saas-webapp-promote-prod-admin_198_final.txt', encoding='utf-8') as frb:
        while True:
            line = frb.readline().rstrip('\n')
            print(line)
            if line == "Finished: SUCCESS":
                print("Success is done ! breaking")
                break
            else:
                print("continue working using regex")
    return "log-report"


def mark_dir_processed(log_file_dir):
    file_path = os.path.join(log_file_dir, '.done')
    with open(file_path, 'w') as log_loc:
        log_loc.write("Log Dir Processed Successfully.")


def prepare_build_info_item(build_details_file, log_report):

    with open(build_details_file, 'r') as bdf:
        build_details = json.load(bdf)
        app_build_info = ApplicationBuildInfo()
        app_build_info.application_name = build_details["application_name"]
        app_build_info.application_type = build_details["application_type"]
        app_build_info.commit_build_id = f'{build_details["git_commit_id"]}_{build_details["build_id"]}'
        app_build_info.build_date_time = parser.parse(build_details['build_date_time'])
        app_build_info.status = build_details["status"].upper()
        app_build_info.environment = build_details["environment"]
        build_info = BuildInfo(build_details["build_id"], build_details["committer_id"], log_report)
        app_build_info.build_info = json.dumps(build_info.__dict__)

        #TODO: decide type of issue from log report
        app_build_info.issue_type = str(IssueType.code)
        return app_build_info


def process_logs():
    for log_file_loc in log_dirs_to_processed:
        log_file = get_log_file_path(log_file_loc)
        build_details_file = os.path.join(log_file_loc, "build_details.json")

        if log_file is not None and build_details_file is not None:
            try:
                log_report = process_log_file(log_file)
                build_info_item = prepare_build_info_item(build_details_file, log_report)
                utils.save_build_info(build_info_item)

                if log_report is not None and mark_dir_processed(log_file_loc):
                    date_dir_marked_to_be_done.add(os.path.dirname(log_file_loc))

            except IOError as e:
                print(e)

    # Processing done mark date log dir as done
    for date_dir in date_dir_marked_to_be_done:
        mark_dir_processed(date_dir)


if __name__ == "__main__":
    '''
     Main method to start execution to get logs directories
        '''
    # list log target directories
    for application in os.listdir(base_log_dir):
        app_log_dir = os.path.join(base_log_dir, application)
        get_log_directories(app_log_dir)

    process_logs()

    #utils.find_info_item("abcdesf1324sgde_1634")

