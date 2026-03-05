# services/nastan_service.py
from typing import List, Optional

from sqlalchemy.orm import Session

from database.connection import SessionLocal
from models.nastan import Nastan


class NastanService:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def _get_session(self) -> Session:
        return self._session_factory()

    def list_nastani(self, firma_id: int | None = None) -> List[Nastan]:
        with self._get_session() as db:
            q = db.query(Nastan)
            if firma_id is not None:
                q = q.filter(Nastan.firma_id == firma_id)
            return q.order_by(Nastan.data.desc()).all()

    def get_nastan(self, nastan_id: int) -> Optional[Nastan]:
        with self._get_session() as db:
            return db.query(Nastan).filter(Nastan.nastan_id == nastan_id).first()

    def create_nastan(self, **data) -> Nastan:
        with self._get_session() as db:
            nastan = Nastan(**data)
            db.add(nastan)
            db.flush()
            return nastan

    def update_nastan(self, nastan_id: int, **data) -> Optional[Nastan]:
        with self._get_session() as db:
            nastan = db.query(Nastan).filter(Nastan.nastan_id == nastan_id).first()
            if not nastan:
                return None
            for k, v in data.items():
                if hasattr(nastan, k):
                    setattr(nastan, k, v)
            db.commit()
            return nastan

    def delete_nastan(self, nastan_id: int) -> bool:
        with self._get_session() as db:
            nastan = db.query(Nastan).filter(Nastan.nastan_id == nastan_id).first()
            if not nastan:
                return False
            db.delete(nastan)
            db.commit()
            return True
