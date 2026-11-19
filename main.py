from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import database

database.crear_tablas()

app = FastAPI(title="Nícol Dreams - Logística y Tienda Virtual API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ESQUEMAS PYDANTIC ---
class ProveedorCreate(BaseModel):
    nombre: str
    tipo_joya: str
    material_pureza: str
    con_grabado: bool
    capacidad: int
    costo_unitario: float
    nivel_rotacion: int = 5

class ProductoCreate(BaseModel):
    proveedor_id: int
    nombre_modelo: str
    categoria: str
    material_pureza: str
    foto_url: str
    precio_venta: float
    stock_inicial: int = 0

class CompraCreate(BaseModel):
    producto_id: int
    cantidad: int

class SimulacionRequest(BaseModel):
    capital: float
    pct_aretes: float
    pct_pulseras: float
    pct_anillos: float
    pct_collares: float

# --- DATOS INICIALES DE EJEMPLO ---
@app.on_event("startup")
def poblar_datos_iniciales():
    db = database.SessionLocal()
    if db.query(database.Proveedor).count() == 0:
        t1 = database.Proveedor(
            nombre="Taller Qorikancha Plata", tipo_joya="Anillos",
            material_pureza="Plata Ley 950", con_grabado=True,
            capacidad=40, costo_unitario=65.0, nivel_rotacion=9
        )
        t2 = database.Proveedor(
            nombre="Artesanías San Blas Oro", tipo_joya="Anillos",
            material_pureza="Oro 18k", con_grabado=True,
            capacidad=20, costo_unitario=320.0, nivel_rotacion=8
        )
        t3 = database.Proveedor(
            nombre="Orfebrería Valle Sagrado", tipo_joya="Collares",
            material_pureza="Plata Ley 950", con_grabado=False,
            capacidad=35, costo_unitario=95.0, nivel_rotacion=7
        )
        db.add_all([t1, t2, t3])
        db.commit()

        modelos_demo = [
            database.Producto(
                proveedor_id=t1.id, nombre_modelo="Anillo Solitario Andino",
                categoria="Anillos", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600&q=80",
                precio_venta=145.0, stock_actual=12
            ),
            database.Producto(
                proveedor_id=t1.id, nombre_modelo="Alianza Trenzada Cusco",
                categoria="Anillos", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=600&q=80",
                precio_venta=130.0, stock_actual=8
            ),
            database.Producto(
                proveedor_id=t2.id, nombre_modelo="Anillo Compromiso Imperial",
                categoria="Anillos", material_pureza="Oro 18k",
                foto_url="https://images.unsplash.com/photo-1598560917505-59a3ad559071?w=600&q=80",
                precio_venta=680.0, stock_actual=4
            ),
            database.Producto(
                proveedor_id=t3.id, nombre_modelo="Collar Luna de Plata",
                categoria="Collares", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&q=80",
                precio_venta=195.0, stock_actual=10
            ),
        ]
        db.add_all(modelos_demo)
        db.commit()
    db.close()

# --- RUTAS DE PROVEEDORES ---
@app.get("/proveedores/")
def listar_proveedores(db: Session = Depends(get_db)):
    return db.query(database.Proveedor).all()

@app.post("/proveedores/")
def crear_proveedor(prov: ProveedorCreate, db: Session = Depends(get_db)):
    nuevo = database.Proveedor(**prov.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.delete("/proveedores/{prov_id}")
def eliminar_proveedor(prov_id: int, db: Session = Depends(get_db)):
    prov = db.query(database.Proveedor).filter(database.Proveedor.id == prov_id).first()
    if not prov:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(prov)
    db.commit()
    return {"ok": True}

# --- RUTAS DE CATÁLOGO POR TALLER Y TIENDA VIRTUAL ---
@app.get("/productos/")
def listar_todos_productos(db: Session = Depends(get_db)):
    productos = db.query(database.Producto).all()
    resultado = []
    for p in productos:
        resultado.append({
            "id": p.id,
            "proveedor_id": p.proveedor_id,
            "taller_nombre": p.proveedor.nombre if p.proveedor else "Taller Asociado",
            "costo_taller": p.proveedor.costo_unitario if p.proveedor else 0,
            "nombre_modelo": p.nombre_modelo,
            "categoria": p.categoria,
            "material_pureza": p.material_pureza,
            "foto_url": p.foto_url,
            "precio_venta": p.precio_venta,
            "stock_actual": p.stock_actual
        })
    return resultado

@app.get("/proveedores/{prov_id}/productos")
def listar_productos_por_proveedor(prov_id: int, db: Session = Depends(get_db)):
    return db.query(database.Producto).filter(database.Producto.proveedor_id == prov_id).all()

@app.post("/productos/")
def crear_producto(prod: ProductoCreate, db: Session = Depends(get_db)):
    prov = db.query(database.Proveedor).filter(database.Proveedor.id == prod.proveedor_id).first()
    if not prov:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    nuevo_prod = database.Producto(
        proveedor_id=prod.proveedor_id,
        nombre_modelo=prod.nombre_modelo,
        categoria=prod.categoria,
        material_pureza=prod.material_pureza,
        foto_url=prod.foto_url,
        precio_venta=prod.precio_venta,
        stock_actual=prod.stock_inicial
    )
    db.add(nuevo_prod)
    db.commit()
    db.refresh(nuevo_prod)
    return nuevo_prod

# --- RUTA DE COMPRA LOGÍSTICA (ACTUALIZA STOCK DE LA TIENDA VIRTUAL) ---
@app.post("/compras/")
def registrar_compra_mercaderia(compra: CompraCreate, db: Session = Depends(get_db)):
    if compra.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")
    prod = db.query(database.Producto).filter(database.Producto.id == compra.producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Modelo de joya no encontrado")

    costo_unit = prod.proveedor.costo_unitario if prod.proveedor else 0.0
    costo_total = round(costo_unit * compra.cantidad, 2)

    prod.stock_actual += compra.cantidad

    registro = database.CompraLogistica(
        producto_id=prod.id,
        cantidad_comprada=compra.cantidad,
        costo_total=costo_total
    )
    db.add(registro)
    db.commit()
    db.refresh(prod)

    return {
        "mensaje": f"Se agregaron {compra.cantidad} unidades de '{prod.nombre_modelo}' al inventario",
        "nuevo_stock": prod.stock_actual,
        "costo_total": costo_total
    }

# --- OPTIMIZADOR DE COMPRA INTELIGENTE ---
@app.post("/optimizar/")
def optimizar_compra(req: SimulacionRequest, db: Session = Depends(get_db)):
    proveedores = db.query(database.Proveedor).all()
    asignaciones = {
        "Aretes": req.capital * (req.pct_aretes / 100.0),
        "Pulseras": req.capital * (req.pct_pulseras / 100.0),
        "Anillos": req.capital * (req.pct_anillos / 100.0),
        "Collares": req.capital * (req.pct_collares / 100.0),
    }

    plan = []
    inversion_total = 0.0
    total_unidades = 0

    for cat, presupuesto_cat in asignaciones.items():
        if presupuesto_cat <= 0:
            continue
        candidatos = [p for p in proveedores if p.tipo_joya.lower() == cat.lower()]
        candidatos.sort(key=lambda x: (x.nivel_rotacion / max(x.costo_unitario, 1)), reverse=True)

        saldo_cat = presupuesto_cat
        for p in candidatos:
            if saldo_cat < p.costo_unitario:
                continue
            max_posible = int(saldo_cat // p.costo_unitario)
            unidades = min(max_posible, p.capacidad)
            if unidades > 0:
                subtotal = round(unidades * p.costo_unitario, 2)
                saldo_cat -= subtotal
                inversion_total += subtotal
                total_unidades += unidades
                plan.append({
                    "taller": p.nombre,
                    "categoria": p.tipo_joya,
                    "pureza": p.material_pureza,
                    "unidades": unidades,
                    "costo_unitario": p.costo_unitario,
                    "subtotal": subtotal
                })

    return {
        "inversion_ejecutada": round(inversion_total, 2),
        "saldo_remanente": round(req.capital - inversion_total, 2),
        "total_unidades": total_unidades,
        "plan": plan
    }