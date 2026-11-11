def can_download_receipt(receipt_owner_id, requester_id, receipt_status):
    return bool(receipt_owner_id) and receipt_owner_id == requester_id and receipt_status == 'final'
