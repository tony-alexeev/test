def can_download_invoice(customer_id, requester_id, invoice_status):
    return bool(customer_id) and customer_id == requester_id and invoice_status == "issued"
