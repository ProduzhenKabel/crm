# models/firma.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from database.connection import Base


class Firma(Base):
    __tablename__ = "firmi"

    firma_id = Column(Integer, primary_key=True, autoincrement=False)  # ← KEY FIX
    ime = Column(String(255))
    contactMail = Column(String(255))
    contactNumber = Column(String(50))
    opis = Column(Text)
    status = Column(String(100))
    notes = Column(Text)

    nastani = relationship("Nastan", back_populates="firma")
