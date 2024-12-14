import os

credentials = {
    "postgresql":
        {
            "db_user": os.environ['postgresql_admin_username'],
            "db_pass": os.environ['postgresql_admin_pass'],
            "db_name": os.environ['postgresql_db_name']
        }
}

def get_credentials(service_name):
    return credentials[service_name]