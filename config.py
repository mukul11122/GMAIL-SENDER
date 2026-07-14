EMAIL_SETTINGS = {
    'batch_size': 100,
    'delay_between_emails': 2,
    'delay_between_batches': 60,
    'max_emails_per_account_per_day': 450,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
}

DATABASE_SETTINGS = {
    'db_path': 'customers.db',
}

EMAIL_TEMPLATE = {
    'subject': 'New Stock Arrived - Place Your Orders Now!',
    'sender_name': 'Sales Team',
}
