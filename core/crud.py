from geoalchemy2 import WKTElement
from sqlalchemy import select, func, Integer
from sqlalchemy.orm import selectinload, aliased
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Organization, Building, Activity, OrganizationActivity


async def get_activity_and_descendants_ids(db: AsyncSession, activity_id: int):
    parent = aliased(Activity)
    child = aliased(Activity)

    base = select(parent.id, func.cast(1, Integer).label("level")).where(parent.id == activity_id)
    cte = base.cte(name="activity_tree", recursive=True)

    recursive = select(
        child.id,
        (cte.c.level + 1).label("level")
    ).join(
        cte, child.parent_id == cte.c.id
    ).where(
        cte.c.level < 3
    )

    cte = base.union_all(recursive).cte(name="t", recursive=True)
    stmt = select(cte.c.id)
    result = await db.execute(stmt)
    return [row[0] for row in result]


async def get_orgs_by_building(db: AsyncSession, building_id: int):
    stmt = select(
        Organization
    ).where(
        Organization.building_id == building_id
    ).options(
        selectinload(Organization.phones),
        selectinload(Organization.building),
        selectinload(Organization.organization_activities).selectinload(OrganizationActivity.activity),
    )

    res = await db.scalars(stmt)
    return res.unique().all()


async def get_orgs_by_activity(db: AsyncSession, activity_id: int):
    ids = await get_activity_and_descendants_ids(db, activity_id)
    stmt = select(
        Organization
    ).join(
        OrganizationActivity
    ).where(
        OrganizationActivity.activity_id.in_(ids)
    ).options(
        selectinload(Organization.phones),
        selectinload(Organization.building),
        selectinload(Organization.organization_activities).selectinload(OrganizationActivity.activity),
    )

    res = await db.scalars(stmt)
    return res.unique().all()


async def search_orgs_by_name(db: AsyncSession, name: str):
    stmt = select(
        Organization
    ).where(
        Organization.name.ilike(f"%{name}%")
    ).options(
        selectinload(Organization.building),
        selectinload(Organization.phones),
        selectinload(Organization.organization_activities).selectinload(OrganizationActivity.activity),
    )

    res = await db.scalars(stmt)
    return res


async def get_orgs_in_radius(db: AsyncSession, lat: float, lon: float, radius_km: float):
    search_point = WKTElement(f"POINT({lon} {lat})", srid=4326)

    stmt = select(
        Organization
    ).join(
        Building
    ).where(
        func.ST_DWithin(
            func.ST_GeographyFromText(func.ST_AsText(Building.point)),
            func.ST_GeographyFromText(func.ST_AsText(search_point)),
            radius_km * 1000  # convert to meters
        )
    ).options(
        selectinload(Organization.building),
        selectinload(Organization.phones),
        selectinload(Organization.organization_activities).selectinload(OrganizationActivity.activity),
        )

    res = await db.scalars(stmt)
    return res.all()


async def get_org_by_id(db: AsyncSession, org_id: int):
    stmt = select(
        Organization
    ).where(
        Organization.id == org_id
    ).options(
        selectinload(Organization.building),
        selectinload(Organization.phones),
        selectinload(Organization.organization_activities).selectinload(OrganizationActivity.activity),
    )

    res = await db.scalars(stmt)
    return res.first()


async def get_orgs(db: AsyncSession):
    stmt = select(
        Organization
    ).options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.organization_activities).selectinload(OrganizationActivity.activity),
        )

    res = await db.scalars(stmt)
    return res.all()
