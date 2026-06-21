"""Network monitoring and traffic models"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON, LargeBinary
from sqlalchemy.sql import func

from src.models.database import Base


class NetworkTraffic(Base):
    """Network traffic model"""
    __tablename__ = "network_traffic"

    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(String(100), unique=True, nullable=False, index=True)
    src_ip = Column(String(45), nullable=False, index=True)  # IPv4 or IPv6
    dst_ip = Column(String(45), nullable=False, index=True)
    src_port = Column(Integer, nullable=True)
    dst_port = Column(Integer, nullable=True)
    protocol = Column(String(20), nullable=False)  # TCP, UDP, ICMP, etc.
    packets = Column(Integer, default=0)
    bytes_sent = Column(Integer, default=0)
    bytes_received = Column(Integer, default=0)
    duration = Column(Float, default=0.0)  # seconds
    flags = Column(String(100), nullable=True)
    is_anomaly = Column(Boolean, default=False)
    is_malicious = Column(Boolean, default=False)
    threat_score = Column(Float, default=0.0)
    metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<NetworkTraffic(id={self.id}, src={self.src_ip}:{self.src_port} -> dst={self.dst_ip}:{self.dst_port})>"


class Packet(Base):
    """Packet model"""
    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(String(100), nullable=False, index=True)
    packet_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    src_ip = Column(String(45), nullable=False)
    dst_ip = Column(String(45), nullable=False)
    src_port = Column(Integer, nullable=True)
    dst_port = Column(Integer, nullable=True)
    protocol = Column(String(20), nullable=False)
    size = Column(Integer, default=0)
    ttl = Column(Integer, nullable=True)
    flags = Column(String(50), nullable=True)
    payload = Column(LargeBinary, nullable=True)  # First 256 bytes
    metadata = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Packet(id={self.id}, flow={self.flow_id}, packet={self.packet_number})>"


class Anomaly(Base):
    """Network anomaly model"""
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    anomaly_id = Column(String(100), unique=True, nullable=False, index=True)
    flow_id = Column(String(100), nullable=True, index=True)
    anomaly_type = Column(String(100), nullable=False)  # port_scan, ddos, exfiltration, etc.
    severity = Column(String(20), default="medium")  # critical, high, medium, low
    confidence = Column(Float, default=0.0)
    description = Column(String(500), nullable=True)
    src_ip = Column(String(45), nullable=True)
    dst_ip = Column(String(45), nullable=True)
    src_port = Column(Integer, nullable=True)
    dst_port = Column(Integer, nullable=True)
    is_confirmed = Column(Boolean, default=False)
    is_false_positive = Column(Boolean, default=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    detected_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Anomaly(id={self.id}, type={self.anomaly_type}, severity={self.severity})>"
