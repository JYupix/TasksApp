from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configura el motor de la base de datos (SQLite en este caso)
DATABASE_URL = "sqlite:///tasks.db"
engine = create_engine(DATABASE_URL, echo=True)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)