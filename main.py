# kebab_app/main.py
import json
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from typing import List

import models
from database import engine, get_db

# Crea le tabelle nel database (se non esistono)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kebab Manager Enterprise")

# Configurazione Template HTML
templates = Jinja2Templates(directory="templates")


# --- WEBSOCKET MANAGER ---
# Gestisce le connessioni in tempo reale per la dashboard del titolare
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_order(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# --- ENDPOINTS HTML ---
@app.get("/", response_class=HTMLResponse)
async def read_customer_app(request: Request):
    return templates.TemplateResponse("cliente.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def read_admin_app(request: Request):
    return templates.TemplateResponse("titolare.html", {"request": request})


# --- API REST (JSON) ---
@app.get("/api/menus")
def get_menus(db: Session = Depends(get_db)):
    """Restituisce il menu completo con varianti e ingredienti."""
    menus = db.query(models.Menu).all()
    result = []
    for m in menus:
        result.append(
            {
                "id": m.id,
                "name": m.name,
                "base_price": m.base_price,
                "variants": [{"id": v.id, "name": v.name} for v in m.variants],
                "ingredients": [{"id": i.id, "name": i.name} for i in m.ingredients],
            }
        )
    return result


@app.post("/api/orders")
async def create_order(order_data: dict, db: Session = Depends(get_db)):
    """Crea un nuovo ordine e notifica i titolari tramite WebSocket."""
    # 1. Salvataggio nel DB locale
    new_order = models.Order(
        customer_name=order_data.get("customer_name", "Cliente"),
        order_type=order_data.get("order_type"),
        total_price=order_data.get("total_price"),
        details=json.dumps(order_data.get("items")),
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # 2. Notifica WebSocket al Titolare
    order_notification = {
        "id": new_order.id,
        "customer_name": new_order.customer_name,
        "order_type": new_order.order_type,
        "status": new_order.status,
        "details": order_data.get("items"),
    }
    await manager.broadcast_order(json.dumps(order_notification))

    return {"message": "Ordine ricevuto con successo", "order_id": new_order.id}


# --- WEBSOCKET ENDPOINT ---
@app.websocket("/ws/admin")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Rimane in ascolto di eventuali comandi dall'admin (es. cambio stato)
            data = await websocket.receive_text()
            # Logica per gestire update da websocket potrebbe andare qui
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# kebab_app/main.py

# Inserisci questo blocco di codice sotto l'endpoint esistente @app.post("/api/orders")
# e prima della sezione # --- WEBSOCKET ENDPOINT ---


@app.get("/api/orders")
def get_active_orders(db: Session = Depends(get_db)):
    """
    Recupera tutti gli ordini attivi dal database.
    Filtra gli ordini che non sono ancora nello stato 'Consegnato'.
    """
    # Esegue una query SQL via ORM per ottenere ordini non consegnati
    orders = db.query(models.Order).filter(models.Order.status != "Consegnato").all()

    result = []
    for order in orders:
        result.append(
            {
                "id": order.id,
                "customer_name": order.customer_name,
                "order_type": order.order_type,
                "status": order.status,
                # Deserializza la stringa JSON dei dettagli in un oggetto Python (lista)
                "details": json.loads(order.details) if order.details else [],
            }
        )
    return result
