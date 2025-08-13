# src/config.py
from __future__ import annotations
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import streamlit as st

load_dotenv()

def _db_url() -> str:
    host = os.getenv("PG_HOST", "localhost")
    port = os.getenv("PG_PORT", "5432")
    db   = os.getenv("PG_DB")
    user = os.getenv("PG_USER")
    pwd  = os.getenv("PG_PASS", "")
    return f"postgresql+psycopg://{user}:{quote_plus(pwd)}@{host}:{port}/{db}"

@st.cache_resource(show_spinner=False)
def get_engine():
    return create_engine(_db_url(), pool_pre_ping=True)

@st.cache_resource(show_spinner=False)
def get_session():
    engine = get_engine()
    schema = os.getenv("PG_SCHEMA")
    if schema:
        with engine.connect() as conn:
            conn.execute(text(f"SET search_path TO {schema}"))
    return sessionmaker(bind=engine)()

def test_connection() -> str:
    try:
        with get_engine().connect() as conn:
            v = conn.execute(text("select version()")).scalar_one()
        return f"Conectado: {v}"
    except Exception as e:
        return f"ERROR: {e}"
