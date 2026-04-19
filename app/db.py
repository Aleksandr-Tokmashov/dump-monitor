from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:postgres@db:5432/dumps"

engine = create_engine(DATABASE_URL)