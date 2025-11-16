from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from core.db import Base


class OrganizationActivity(Base):
    __tablename__ = "organization_activities"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    organization = relationship("Organization", back_populates="organization_activities")
    activity = relationship("Activity", back_populates="organization_activities")


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    point = Column(Geometry("POINT", srid=4326), nullable=False)

    organizations = relationship("Organization", back_populates="building")

    @property
    def coordinates(self) -> dict:
        if self.point:
            point = to_shape(self.point)
            return {
                "lat": float(point.y),
                "lon": float(point.x)
            }


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    parent = relationship("Activity", remote_side=[id], backref="children")
    organization_activities = relationship("OrganizationActivity", back_populates="activity")


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")
    phones = relationship("OrganizationPhone", back_populates="organization", cascade="all, delete-orphan")
    organization_activities = relationship("OrganizationActivity", back_populates="organization")

    @property
    def activities(self):
        """Доступ к активностям через промежуточную таблицу"""
        if hasattr(self, 'organization_activities'):
            return [oa.activity for oa in self.organization_activities if oa.activity]
        return []


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    phone = Column(String, nullable=False)

    organization = relationship("Organization", back_populates="phones")
