from sqlalchemy import create_engine, text
from app.settings import settings

# Creates engine once globally
egine = create_engine(settings.database_url, pool_pre_ping=True) 
# pool_pre_ping will piung the databse before attempting to conenct
# if connection is dead for any reason, SQLAlchemy transparently replaces the dead connection

def check_db() -> None:
  with engine.connect() as conn:
    conn.execute(text("SELECT 1"))