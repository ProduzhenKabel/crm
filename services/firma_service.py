# services/firma_service.py
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

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

    def get_or_create_firma(self, ime: str, **extra_data) -> Firma:
        """
        Check if firma exists by ime ONLY.
        If exists → return it.
        If not → create new with unique firma_id.
        """
        with self._get_session() as db:
            # Check if exists (exact ime match)
            firma = db.query(Firma).filter(Firma.ime == ime).first()
            
            if firma:
                print(f"✅ Firma exists: {firma.firma_id} - {firma.ime}")
                return firma
            
            # Create new with unique ID
            firma_id = int(uuid.uuid4().hex[:8], 16) % 1000000  # Random 6-digit ID
            while db.query(Firma).filter(Firma.firma_id == firma_id).first():
                firma_id = int(uuid.uuid4().hex[:8], 16) % 1000000  # Retry if collision
            
            firma = Firma(
                firma_id=firma_id,
                ime=ime,
                **extra_data
            )
            db.add(firma)
            db.commit()
            db.refresh(firma)
            print(f"✅ Created new firma: {firma.firma_id} - {firma.ime}")
            return firma

    def create_firma(self, **data) -> Firma:
        """Manual create (for external IDs)"""
        with self._get_session() as db:
            firma = Firma(**data)
            db.add(firma)
            db.commit()
            db.refresh(firma)
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
