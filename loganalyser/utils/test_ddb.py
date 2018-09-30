from models.app_build_info_model import ApplicationBuildInfo
from utils import ddb_util
import pandas as pd

pd.set_option('display.expand_frame_repr', False)


data = ddb_util.load_all_build_info(ApplicationBuildInfo)

records = []

for item in data:
    records.append(item.__item_to_record__())

columns = ['CommitBuildId', 'ApplicationName', 'ApplicationType', 'Status', 'IssueType',
           'BuildDateTime', 'Environment', 'BuildId', 'CommitterId', 'LogReport']


df = pd.DataFrame.from_records(records, columns=columns)

# head, tail, merge, join, concat, set_index, rename
print(df.tail(10))

