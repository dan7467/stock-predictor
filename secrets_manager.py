import os

credentials = {
    "postgresql":
        {
            "db_user": os.environ['postgresql_admin_username'],
            "db_pass": os.environ['postgresql_admin_pass']
        }
}

def get_credentials(service_name):
    return credentials[service_name]