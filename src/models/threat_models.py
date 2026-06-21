"""Threat and IOC models"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.sql import func

from src.models.database import Base


class Threat(Base):
    """Threat model"""
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    threat_type = Column(String(50), nullable=False)  # malware, ransomware, apt, etc.
    severity = Column(String(20), default="medium")  # critical, high, medium, low
    confidence = Column(Float, default=0.0)
    source = Column(String(50), nullable=True)  # MISP, OTX, VirusTotal, etc.
    source_url = Column(String(500), nullable=True)
    indicators_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_seen = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Threat(id={self.id}, name={self.name}, severity={self.severity})>"


class IOC(Base):
    """Indicator of Compromise model"""
    __tablename__ = "iocs"

    id = Column(Integer, primary_key=True, index=True)
    ioc_id = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(String(500), nullable=False, index=True)
    ioc_type = Column(String(50), nullable=False)  # ip, domain, file_hash, url, email, etc.
    threat_id = Column(Integer, nullable=True)
    source = Column(String(50), nullable=True)
    confidence = Column(Float, default=0.0)
    severity = Column(String(20), default="medium")
    first_seen = Column(DateTime(timezone=True), nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<IOC(id={self.id}, value={self.value}, type={self.ioc_type})>"


class ThreatActor(Base):
    """Threat Actor model"""
    __tablename__ = "threat_actors"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    aliases = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    origin_country = Column(String(100), nullable=True)
    target_countries = Column(String(500), nullable=True)
    target_industries = Column(String(500), nullable=True)
    motivation = Column(String(100), nullable=True)  # financial, political, espionage, etc.
    first_seen = Column(DateTime(timezone=True), nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    threat_level = Column(String(20), default="medium")
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ThreatActor(id={self.id}, name={self.name})>"


class MitreTechnique(Base):
    """MITRE ATT&CK Technique model"""
    __tablename__ = "mitre_techniques"

    id = Column(Integer, primary_key=True, index=True)
    technique_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tactic = Column(String(100), nullable=False)
    platform = Column(String(100), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<MitreTechnique(id={self.id}, name={self.name}, tactic={self.tactic})>"
