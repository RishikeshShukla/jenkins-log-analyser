from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute
from pynamodb.models import Model
import json

class ApplicationBuildInfo(Model):
    """
     ApplicationBuildInfo model for build storing information
    """

    class Meta:
        table_name = 'application-build-info'
        region = 'us-west-1'
        host = "http://localhost:8000"

    # unique hash is combination of git commit id and build id separated by '_'
    commit_build_id = UnicodeAttribute(hash_key=True)
    application_name = UnicodeAttribute()
    application_type = UnicodeAttribute()
    build_info = JSONAttribute()
    status = UnicodeAttribute()
    issue_type = UnicodeAttribute()
    build_date_time = UTCDateTimeAttribute()
    environment = UnicodeAttribute()

    def __repr__(self):
        return f"ApplicationBuildInfo{ self.commit_build_id, self.application_name, self.application_type,self.build_info, self.status, self.issue_type, self.build_date_time, self.environment}"

    def __item_to_record__(self):
        build_info = json.loads(self.build_info)
        return (self.commit_build_id, self.application_name, self.application_type, self.status,
                self.issue_type, self.build_date_time, self.environment, build_info['build_id'],
                build_info['committer_id'], build_info['log_report'])


class BuildInfo:

    def __init__(self, build_id, committer, log_report):
        self.build_id = build_id
        self.committer_id = committer
        self.log_report = log_report
