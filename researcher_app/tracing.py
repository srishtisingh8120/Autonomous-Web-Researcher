import os
import smartllmops
from dotenv import load_dotenv

load_dotenv()

# Initialize Tracer
tracer = smartllmops.init(
    cosmos_conn=os.getenv("COSMOS_CONN_WRITE"),
    db_name=os.getenv("COSMOS_DB"),
    container_name=os.getenv("COSMOS_CONTAINER", "raw_traces"),
    application_name="Autonomous-Web-Researcher"
)
