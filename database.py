from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./nicol_dreams.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProveedorDB(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo_joya = Column(String)       # Aretes, Pulseras, Anillos, Collares
    material_pureza = Column(String) # Plata Ley 950, Plata 925, Oro 18K
    con_grabado = Column(String)     # Incluido, Personalizado, Sin Grabado
    capacidad = Column(Integer)
    costo_unitario = Column(Float)
    nivel_rotacion = Column(Integer) # Escala 1 al 10 (Qué tanto se vende/calidad)

def init_db():
    Base.metadata.create_all(bind=engine)