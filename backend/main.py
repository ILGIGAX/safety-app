from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg
from typing import List

app = FastAPI(title="Safety App API")

# Abilita CORS per permettere al frontend (su porta 3000) di fare richieste
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione restringi gli origin consentiti
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelli per la registrazione, accesso e profilo utente
class UserRegister(BaseModel):
    email: str
    password: str
    nome: str
    cognome: str
    data_nascita: str
    genere: str
    motivo_iscrizione: str = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    email: str
    nome: str
    cognome: str
    data_nascita: str
    genere: str
    motivo_iscrizione: str = None

# Dati simulati per le zone di rischio
RISK_ZONES = [
    {"zone": "Zona Centro", "risk_percentage": 80},
    {"zone": "Zona Nord", "risk_percentage": 40},
    {"zone": "Zona Sud", "risk_percentage": 60},
    {"zone": "Zona Est", "risk_percentage": 30},
]

@app.get("/risk-zones")
def get_risk_zones():
    """
    Restituisce le percentuali di rischio per le diverse zone.
    In una implementazione reale, qui verrebbe eseguito l'algoritmo che analizza gli atti criminosi.
    """
    return {"risk_zones": RISK_ZONES}

# Modello per l'alert di emergenza
class EmergencyAlert(BaseModel):
    user_id: str
    latitude: float
    longitude: float

@app.post("/emergency")
def trigger_emergency(alert: EmergencyAlert):
    """
    Attiva un alert di emergenza.
    In un'app reale questo endpoint potrebbe:
      - Contattare le forze dell'ordine
      - Inviare notifiche ai membri della community entro 1 km
    """
    # Simulazione: restituisce un messaggio di conferma
    return {"status": "Alert di emergenza attivato", "alert": alert}

@app.get("/safe-route")
def get_safe_route(from_location: str, to_location: str):
    """
    Restituisce un percorso sicuro da A a B.
    La rotta è simulata come una lista di waypoints; in una soluzione reale verrebbe calcolata
    tenendo conto dei dati sulla luce e sicurezza delle vie.
    """
    # Dati simulati: lista di waypoint (latitudine e longitudine)
    route = [
        {"lat": 40.712776, "lng": -74.005974},
        {"lat": 40.713776, "lng": -74.004974},
        {"lat": 40.714776, "lng": -74.003974},
    ]
    return {"from": from_location, "to": to_location, "route": route}

@app.get("/track/{user_id}")
def track_user(user_id: str):
    """
    Restituisce la posizione attuale di un utente per il monitoraggio in tempo reale.
    In una soluzione reale, questo endpoint potrebbe leggere dati da un sistema di tracking live.
    """
    # Posizione simulata
    location = {"latitude": 40.712776, "longitude": -74.005974}
    return {"user_id": user_id, "location": location}

@app.get("/")
def read_root():
    return {"message": "Benvenuto nella Safety App API"}

# Funzione per connettersi al database
async def get_db():
    conn = await asyncpg.connect(
        user="safety_user",
        password="safety_password",
        database="safety",
        host="db"
    )
    try:
        yield conn
    finally:
        await conn.close()

@app.post("/register", response_model=UserProfile)
async def register_user(user: UserRegister, db: asyncpg.Connection = Depends(get_db)):
    try:
        # Inserisce il nuovo utente nel database
        result = await db.fetchrow(
            """
            INSERT INTO utenti (email, password, nome, cognome, data_nascita, genere, motivo_iscrizione)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING email, nome, cognome, data_nascita, genere, motivo_iscrizione
            """,
            user.email, user.password, user.nome, user.cognome, user.data_nascita, user.genere, user.motivo_iscrizione
        )
        return UserProfile(**result)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Email già registrata.")

@app.post("/login", response_model=UserProfile)
async def login_user(credentials: UserLogin, db: asyncpg.Connection = Depends(get_db)):
    # Verifica se l'utente esiste e la password corrisponde
    result = await db.fetchrow(
        """
        SELECT email, nome, cognome, data_nascita, genere, motivo_iscrizione
        FROM utenti
        WHERE email = $1 AND password = $2
        """,
        credentials.email, credentials.password
    )
    if not result:
        raise HTTPException(status_code=401, detail="Email o password non validi.")
    return UserProfile(**result)
