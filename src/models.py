"""from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .db import Base

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String(64), index=True, nullable=True)
    source = Column(String(64), index=True)
    severity = Column(String(32), index=True)
    summary = Column(Text)
    published_date = Column(DateTime, nullable=True)
    raw = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'cve_id': self.cve_id,
            'source': self.source,
            'severity': self.severity,
            'summary': self.summary,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
"""