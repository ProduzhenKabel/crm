# services/firma_service.py
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from database.connection import SessionLocal
from models.firma import Firma


class FirmaService:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def _get_session(self) -> Session:
        return self._session_factory()

    def list_firmi(self, search: str | None = None) -> List[Firma]:
        with self._get_session() as db:
            q = db.query(Firma)
            if search:
                q = q.filter(Firma.ime.ilike(f"%{search}%"))
            return q.order_by(Firma.ime).all()

    def get_firma(self, firma_id: int) -> Optional[Firma]:
        with self._get_session() as db:
            return db.query(Firma).filter(Firma.firma_id == firma_id).first()

    def create_firma(self, **data) -> Firma:
        with self._get_session() as db:
            # Use provided firma_id or None (for manual assignment later)
            firma = Firma(**data)
            db.add(firma)
            db.flush()  # Don't commit yet, just generate/assign ID if needed
            return firma

    def update_firma(self, firma_id: int, **data) -> Optional[Firma]:
        with self._get_session() as db:
            firma = db.query(Firma).filter(Firma.firma_id == firma_id).first()
            if not firma:
                return None
            for k, v in data.items():
                if hasattr(firma, k):
                    setattr(firma, k, v)
            db.commit()
            return firma

    def delete_firma(self, firma_id: int) -> bool:
        with self._get_session() as db:
            firma = db.query(Firma).filter(Firma.firma_id == firma_id).first()
            if not firma:
                return False
            db.delete(firma)
            db.commit()
            return True
