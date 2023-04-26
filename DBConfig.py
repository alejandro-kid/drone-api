import os

class DBConfig:

    db_name = os.getenv("DB_NAME", "drone_api")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")

    def __init__(self, db="PostgreSQL"):
        if db == "MySQL":
            self.protocol = "mysql"
        elif db == "PostgreSQL":
            self.protocol = "postgresql"
        else:
            self.protocol = None
    

    def get_uri(self):
        return f"{self.protocol}://{self.db_user}:{self.db_password}@{self.db_host}:" \
            "{self.db_port}/{self.db_name}"
    
    def get_uri_test(self):
        return f"{self.protocol}://{self.db_user}:{self.db_password}@{self.db_host}:" \
            "{self.db_port}/{self.db_name}_test"

