import pandas as pd

from models.app_build_info_model import ApplicationBuildInfo
from utils import ddb_util

pd.set_option('display.expand_frame_repr', False)

columns = ['CommitBuildId', 'ApplicationName', 'ApplicationType', 'Status', 'IssueType', 'BuildDateTime', 'Environment',
           'BuildId', 'CommitterId', 'LogReport']

reports_path = '/home/ubuntu/reports/'

# To load logs data from DDB
data = ddb_util.load_all_build_info(ApplicationBuildInfo)

records = []

for item in data:
    records.append(item.__item_to_record__())

# create data frame from records
df = pd.DataFrame.from_records(records, columns=columns)

"""
 Report:
 ------
  fetch_report() //app_name=[], app_type=[], status=[], issue_type=[], build_date_time={from= , to=}, environment=[]
  fetch_report() //all report

"""


def fetch_full_report():
    return df


# def prepare_condition(status, applications, application_type, environments, date_range):
#     status_condition = df['Status'] == status
#     app_condition_list = []
#
#
#     for application in applications:
#         app_condition_list.append(df['ApplicationName'] == application)
#
#     application_filter = prepare_application_filter(app_condition_list)
#
#     application_filter = app_condition_list[0] | app_condition_list[1]
#
#     condition = status_condition & application_filter
#
#     #print(condition)
#     return condition


# def fetch_partial_report(status, applications, application_type=(), environments=(), date_range={}):
#     condition = prepare_condition(status, applications, application_type, environments, date_range)
#     report = df[condition]
#     return report

def prepare_status_filter(status):
    if status is None:
        condition = (df['Status'] == 'FAILURE') | (df['Status'] == 'SUCCESS')
    else:
        condition = df['Status'] == status

    return condition


def prepare_date_filter(date_range):
    df['BuildDateTime'] = pd.to_datetime(df['BuildDateTime'])
    return (df['BuildDateTime'] >= date_range['from_date']) & (df['BuildDateTime'] < date_range['to_date'])


def fetch_application_wise_report(application, status, date_range):
    application_filter = df['ApplicationName'] == application
    status_filter = prepare_status_filter(status)
    if date_range is not None:
        date_filter = prepare_date_filter(date_range)
        response = df[status_filter & application_filter & date_filter]
    else:
        response = df[status_filter & application_filter]

    return response.to_html(reports_path + application + ".html")


if __name__ == '__main__':
    # full_report = fetch_full_report()
    # print(full_report)
    #

    report = fetch_application_wise_report('tm', 'SUCCESS',
                                           {'from_date': '2018-08-16 00:00:00', 'to_date': '2018-09-06 23:59:59'})
