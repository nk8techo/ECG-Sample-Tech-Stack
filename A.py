import logging
import httpx
import boto3
from sqlalchemy import (
    create_engine, Column, Integer, String, Sequence, MetaData, Table
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()

# Define users table
users_table = Table(
    "users", metadata,
    Column("id", Integer, Sequence("user_id_seq"), primary_key=True),
    Column("name", String(50)),
    Column("email", String(50))
)

# Create table
metadata.create_all(engine)

# S3 client setup (Use proper credentials in production)
s3_client = boto3.client(
    "s3",
    region_name="us-east-1",
    aws_access_key_id="FAKEACCESSKEY",
    aws_secret_access_key="FAKESECRETKEY"
)


class DataAgent:
    def __init__(self):
        self.db_engine = engine
        self.s3_client = s3_client

    def insert_user(self, name: str, email: str):
        """Insert a new user into the database."""
        with self.db_engine.connect() as conn:
            ins = users_table.insert().values(name=name, email=email)
            result = conn.execute(ins)
            logger.debug(f"Inserted user {name} with id: {result.inserted_primary_key}")
            return result.inserted_primary_key

    def fetch_users(self):
        """Fetch all users from the database."""
        with self.db_engine.connect() as conn:
            sel = users_table.select()
            result = conn.execute(sel)
            users = result.fetchall()
            logger.debug(f"Fetched users: {users}")
            return users

    def upload_to_s3(self, bucket: str, key: str, data: str):
        """Upload data to an S3 bucket."""
        response = self.s3_client.put_object(Bucket=bucket, Key=key, Body=data)
        logger.debug(f"S3 upload response: {response}")
        return response

    def call_external_api(self, url: str):
        """Call an external API and return the response."""
        try:
            response = httpx.get(url, timeout=5.0)
            response.raise_for_status()
            logger.debug(f"External API response status: {response.status_code}")
            return response.json()
        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc.request.url!r}.")
            return None
