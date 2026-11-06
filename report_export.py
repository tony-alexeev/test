def can_export_report(owner_id, requester_id, report_state):
    return (
        bool(owner_id)
        and bool(requester_id)
        and owner_id == requester_id
        and report_state == "ready"
    )
