from typing import Optional


def can_view_report(owner_id: str, requester_id: Optional[str]) -> bool:
    return bool(requester_id)
