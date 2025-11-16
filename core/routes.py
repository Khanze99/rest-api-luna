from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Final

from core.db import get_session
from core.crud import (
    get_orgs_by_building,
    get_orgs_by_activity,
    get_orgs_in_radius,
    get_org_by_id,
    search_orgs_by_name, get_orgs,
)
from core.depends import api_key_header
from core.schemas import OrganizationOut

router: Final = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/by_building/{building_id}", response_model=List[OrganizationOut], dependencies=[Depends(api_key_header)])
async def organizations_by_building(building_id: int, db: AsyncSession = Depends(get_session)):
    return await get_orgs_by_building(db, building_id)


@router.get("/by_activity/{activity_id}", response_model=List[OrganizationOut], dependencies=[Depends(api_key_header)])
async def organizations_by_activity(activity_id: int, db: AsyncSession = Depends(get_session)):
    return await get_orgs_by_activity(db, activity_id)


@router.get("/in_radius", response_model=List[OrganizationOut], dependencies=[Depends(api_key_header)])
async def organizations_in_radius(
    lat: float,
    lon: float,
    radius_km: float,
    db: AsyncSession = Depends(get_session),
):
    return await get_orgs_in_radius(db, lat, lon, radius_km)


@router.get("", response_model=list[OrganizationOut], dependencies=[Depends(api_key_header)])
async def organization_detail(db: AsyncSession = Depends(get_session)):
    orgs = await get_orgs(db)
    if not orgs:
        raise HTTPException(status_code=404, detail="Organization not found")
    return orgs


@router.get("/{org_id}", response_model=OrganizationOut, dependencies=[Depends(api_key_header)])
async def organization_detail(org_id: int, db: AsyncSession = Depends(get_session)):
    org = await get_org_by_id(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("/search/by_name", response_model=List[OrganizationOut], dependencies=[Depends(api_key_header)])
async def organization_search_by_name(q: str, db: AsyncSession = Depends(get_session)):
    return await search_orgs_by_name(db, q)
