from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./nicol_dreams.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo_joya = Column(String)
    material_pureza = Column(String)
    con_grabado = Column(Boolean, default=False)
    capacidad = Column(Integer)
    costo_unitario = Column(Float)
    nivel_rotacion = Column(Integer, default=5)

    productos = relationship("Producto", back_populates="proveedor", cascade="all, delete-orphan")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    nombre_modelo = Column(String, index=True)
    categoria = Column(String)       # Anillos, Aretes, Pulseras, Collares
    material_pureza = Column(String) # Plata Ley 950, Plata 925, Oro 18k
    foto_url = Column(String)
    precio_venta = Column(Float)
    stock_actual = Column(Integer, default=0)

    proveedor = relationship("Proveedor", back_populates="productos")

class CompraLogistica(Base):
    __tablename__ = "compras_logistica"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad_comprada = Column(Integer)
    costo_total = Column(Float)
    fecha = Column(DateTime, default=datetime.utcnow)

def crear_tablas():
    Base.metadata.create_all(bind=engine)