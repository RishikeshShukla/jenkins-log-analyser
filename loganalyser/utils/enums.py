from enum import Enum


class Status(Enum):
    success = 1
    failed = 2

    def __str__(self):
        return job_status_dict[self]


job_status_dict = {
    Status.success: 'SUCCESS',
    Status.failed: 'FAILED'
}


class IssueType(Enum):
    code = 1
    infra = 2
    na = 3

    def __str__(self):
        return issue_type_dict[self]


issue_type_dict = {
    IssueType.code: 'CODE',
    IssueType.infra: 'INFRA',
    IssueType.na: 'NA'
}
