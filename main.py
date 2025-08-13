from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os

app = FastAPI()

# MySQL connection string
MYSQL_URL = os.getenv(
    "MYSQL_URL",
    "mysql+pymysql://root:%40Entrance620@127.0.0.1:3306/my_database"
)
engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ClientDB(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)  # Specify length for VARCHAR
    invoices = relationship("InvoiceDB", back_populates="client")

class InvoiceDB(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(255))  # Specify length for VARCHAR
    clientId = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Float)
    client = relationship("ClientDB", back_populates="invoices")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Pydantic models
class Client(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True  # Updated for Pydantic v2

class Invoice(BaseModel):
    id: int
    date: str
    clientId: int
    amount: float
    class Config:
        from_attributes = True  # Updated for Pydantic v2

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get all clients
@app.get("/clients", response_model=List[Client])
def get_clients(db: Session = Depends(get_db)):
    return db.query(ClientDB).all()

# Endpoint to get invoices for a specific client using query parameter
@app.get("/invoices/client", response_model=List[Invoice])
def get_invoices_by_client_name(client_name: str = Query(..., description="Name of the client"), db: Session = Depends(get_db)):
    client = db.query(ClientDB).filter(ClientDB.name.ilike(client_name)).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db.query(InvoiceDB).filter(InvoiceDB.clientId == client.id).all()