import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-fertiliser-app'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Akhilraj%402005@db.qtokozkqkklbpefjqxzx.supabase.co:5432/postgres?sslmode=require"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 10 