from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, ProveedorDB, init_db

app = FastAPI(title="Nícol Dreams - Optimización Financiera y Comercial", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    db = SessionLocal()
    if db.query(ProveedorDB).count() == 0:
        proveedores_iniciales = [
            ProveedorDB(nombre="Juan (Orfebre San Blas)", tipo_joya="Aretes", material_pureza="Plata Ley 950", con_grabado="Sin Grabado", capacidad=35, costo_unitario=45.0, nivel_rotacion=9),
            ProveedorDB(nombre="José (Taller Wanchaq)", tipo_joya="Aretes", material_pureza="Plata Ley 950", con_grabado="Sin Grabado", capacidad=40, costo_unitario=45.0, nivel_rotacion=6),
            ProveedorDB(nombre="José (Taller Wanchaq)", tipo_joya="Pulseras", material_pureza="Plata 925", con_grabado="Incluido", capacidad=30, costo_unitario=60.0, nivel_rotacion=9),
            ProveedorDB(nombre="Juan (Orfebre San Blas)", tipo_joya="Pulseras", material_pureza="Plata 925", con_grabado="Incluido", capacidad=25, costo_unitario=60.0, nivel_rotacion=5),
            ProveedorDB(nombre="Asociación Plateros", tipo_joya="Anillos", material_pureza="Plata Ley 950", con_grabado="Personalizado", capacidad=20, costo_unitario=55.0, nivel_rotacion=8)
        ]
        db.add_all(proveedores_iniciales)
        db.commit()
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProveedorCreate(BaseModel):
    nombre: str
    tipo_joya: str
    material_pureza: str
    con_grabado: str
    capacidad: int
    costo_unitario: float
    nivel_rotacion: int

class PresupuestoRequest(BaseModel):
    presupuesto_total: float
    porcentaje_aretes: float
    porcentaje_pulseras: float
    porcentaje_anillos: float
    porcentaje_collares: float

@app.post("/proveedores/")
def crear_proveedor(prov: ProveedorCreate, db: Session = Depends(get_db)):
    db_prov = ProveedorDB(**prov.dict())
    db.add(db_prov)
    db.commit()
    db.refresh(db_prov)
    return {"mensaje": "Proveedor registrado", "id": db_prov.id}

@app.get("/proveedores/")
def listar_proveedores(db: Session = Depends(get_db)):
    return db.query(ProveedorDB).all()

@app.delete("/proveedores/{prov_id}")
def eliminar_proveedor(prov_id: int, db: Session = Depends(get_db)):
    prov = db.query(ProveedorDB).filter(ProveedorDB.id == prov_id).first()
    if not prov:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(prov)
    db.commit()
    return {"mensaje": "Eliminado"}

@app.post("/optimizar-presupuesto/")
def optimizar_por_presupuesto(req: PresupuestoRequest, db: Session = Depends(get_db)):
    proveedores = db.query(ProveedorDB).all()
    if not proveedores:
        raise HTTPException(status_code=400, detail="No hay proveedores registrados.")

    # Asignación de presupuestos por categoría
    bolsillos = {
        "Aretes": req.presupuesto_total * (req.porcentaje_aretes / 100.0),
        "Pulseras": req.presupuesto_total * (req.porcentaje_pulseras / 100.0),
        "Anillos": req.presupuesto_total * (req.porcentaje_anillos / 100.0),
        "Collares": req.presupuesto_total * (req.porcentaje_collares / 100.0),
    }

    plan_compras = []
    gasto_total_real = 0.0
    piezas_totales = 0

    for categoria, dinero_disponible in bolsillos.items():
        if dinero_disponible <= 0:
            continue
        
        # Filtrar proveedores de esta categoría
        provs_cat = [p for p in proveedores if p.tipo_joya == categoria]
        
        # Ordenar por eficiencia comercial: Menor costo por punto de rotación (Prioriza alta venta y buen precio)
        provs_ordenados = sorted(provs_cat, key=lambda p: (p.costo_unitario / max(p.nivel_rotacion, 1)))
        
        saldo_categoria = dinero_disponible
        
        for prov in provs_ordenados:
            if saldo_categoria < prov.costo_unitario:
                continue
            
            # Cuántas piezas alcanza con el dinero de esta categoría sin pasar la capacidad del taller
            max_por_dinero = int(saldo_categoria // prov.costo_unitario)
            cantidad_comprar = min(max_por_dinero, prov.capacidad)
            
            if cantidad_comprar > 0:
                subtotal = cantidad_comprar * prov.costo_unitario
                plan_compras.append({
                    "origen": prov.nombre,
                    "tipo_joya": prov.tipo_joya,
                    "material_pureza": prov.material_pureza,
                    "con_grabado": prov.con_grabado,
                    "nivel_rotacion": prov.nivel_rotacion,
                    "piezas_asignadas": cantidad_comprar,
                    "costo_unitario": prov.costo_unitario,
                    "subtotal": subtotal
                })
                saldo_categoria -= subtotal
                gasto_total_real += subtotal
                piezas_totales += cantidad_comprar

    return {
        "presupuesto_asignado": req.presupuesto_total,
        "gasto_total_optimizado": gasto_total_real,
        "saldo_sobrante": req.presupuesto_total - gasto_total_real,
        "piezas_totales_adquiridas": piezas_totales,
        "plan_de_abastecimiento": plan_compras
    }