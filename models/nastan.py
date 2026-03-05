# models/nastan.py
from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class Nastan(Base):
    __tablename__ = "nastani"

    nastan_id = Column(Integer, primary_key=True, autoincrement=False)  # ← KEY FIX
    firma_id = Column(Integer, ForeignKey("firmi.firma_id"))
    ime_nastan = Column(Text)
    data = Column(Date)
    opis = Column(Text)
    ishod = Column(Text)

    firma = relationship("Firma", back_populates="nastani")
