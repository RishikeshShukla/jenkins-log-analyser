from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute


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


def is_table_exist():
    return ApplicationBuildInfo.exists()


class BuildInfo:

    def __init__(self, build_id, committer, log_report):
        self.build_id = build_id
        self.committer_id = committer
        self.log_report = log_report
