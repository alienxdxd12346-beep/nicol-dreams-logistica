@app.on_event("startup")
def poblar_datos_iniciales():
    db = database.SessionLocal()
    if db.query(database.Proveedor).count() == 0:
        t1 = database.Proveedor(
            nombre="Taller Qorikancha Plata", tipo_joya="Anillos",
            material_pureza="Plata Ley 950", con_grabado=True,
            capacidad=50, costo_unitario=65.0, nivel_rotacion=9
        )
        t2 = database.Proveedor(
            nombre="Artesanías San Blas Oro", tipo_joya="Anillos",
            material_pureza="Oro 18k", con_grabado=True,
            capacidad=25, costo_unitario=320.0, nivel_rotacion=9
        )
        t3 = database.Proveedor(
            nombre="Orfebrería Valle Sagrado", tipo_joya="Collares",
            material_pureza="Plata Ley 950", con_grabado=False,
            capacidad=40, costo_unitario=95.0, nivel_rotacion=8
        )
        t4 = database.Proveedor(
            nombre="Atelier Písac Gemas & Oro", tipo_joya="Aretes",
            material_pureza="Oro 18k", con_grabado=False,
            capacidad=30, costo_unitario=240.0, nivel_rotacion=7
        )
        db.add_all([t1, t2, t3, t4])
        db.commit()

        modelos_demo = [
            database.Producto(
                proveedor_id=t2.id, nombre_modelo="Solitario Inti de Oro 18K",
                categoria="Anillos", material_pureza="Oro 18k",
                foto_url="https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&q=80",
                precio_venta=790.0, stock_actual=6
            ),
            database.Producto(
                proveedor_id=t2.id, nombre_modelo="Alianza Clásica Valle Sagrado",
                categoria="Anillos", material_pureza="Oro 18k",
                foto_url="https://images.unsplash.com/photo-1598560917505-59a3ad559071?w=800&q=80",
                precio_venta=620.0, stock_actual=8
            ),
            database.Producto(
                proveedor_id=t1.id, nombre_modelo="Anillo Sello Cusqueño Plata 950",
                categoria="Anillos", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=800&q=80",
                precio_venta=165.0, stock_actual=14
            ),
            database.Producto(
                proveedor_id=t1.id, nombre_modelo="Anillo Media Alianza Brillante",
                categoria="Anillos", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&q=80",
                precio_venta=140.0, stock_actual=11
            ),
            database.Producto(
                proveedor_id=t1.id, nombre_modelo="Anillo Orgánico Textura Andina",
                categoria="Anillos", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&q=80",
                precio_venta=155.0, stock_actual=9
            ),
            database.Producto(
                proveedor_id=t3.id, nombre_modelo="Collar Gargantilla Killa",
                categoria="Collares", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&q=80",
                precio_venta=210.0, stock_actual=12
            ),
            database.Producto(
                proveedor_id=t3.id, nombre_modelo="Dije Gota de Luz Plata 950",
                categoria="Collares", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1611085583191-a3b181a88401?w=800&q=80",
                precio_venta=185.0, stock_actual=7
            ),
            database.Producto(
                proveedor_id=t4.id, nombre_modelo="Aretes Candonga Oro 18K",
                categoria="Aretes", material_pureza="Oro 18k",
                foto_url="https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&q=80",
                precio_venta=490.0, stock_actual=5
            ),
            database.Producto(
                proveedor_id=t1.id, nombre_modelo="Topos Esfera Pulida Plata 950",
                categoria="Aretes", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1630019852942-f89202989a59?w=800&q=80",
                precio_venta=95.0, stock_actual=18
            ),
            database.Producto(
                proveedor_id=t1.id, nombre_modelo="Pulsera Eslabón Artesanal",
                categoria="Pulseras", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&q=80",
                precio_venta=230.0, stock_actual=10
            ),
            database.Producto(
                proveedor_id=t2.id, nombre_modelo="Pulsera Rígida Fina Oro 18K",
                categoria="Pulseras", material_pureza="Oro 18k",
                foto_url="https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=800&q=80",
                precio_venta=740.0, stock_actual=4
            ),
            database.Producto(
                proveedor_id=t3.id, nombre_modelo="Collar Cadena Veneciana 950",
                categoria="Collares", material_pureza="Plata Ley 950",
                foto_url="https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&q=80",
                precio_venta=175.0, stock_actual=15
            ),
        ]
        db.add_all(modelos_demo)
        db.commit()
    db.close()