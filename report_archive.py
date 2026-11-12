def can_archive_report(owner_id, requester_id, report_state):
    return bool(owner_id and requester_id and owner_id == requester_id and report_state == "closed")
