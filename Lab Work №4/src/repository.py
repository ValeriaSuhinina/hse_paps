from typing import Union

from sqlalchemy import select, update, delete

from database import ConstructionObjectOrm, new_session, ViolationOrm, UserOrm
from schemas import SConstructionObjectAdd, SConstructionObject, SViolationAdd, SViolation, SUser, SUserAdd


class ConstructionSupervisionRepository:
    @classmethod
    async def add_user(cls, user: SUserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump()
            new_user = UserOrm(**data)
            session.add(new_user)
            await session.flush()
            await session.commit()
            return new_user.id

    @classmethod
    async def add_construction_object(cls, construction_object: SConstructionObjectAdd) -> int:
        async with new_session() as session:
            data = construction_object.model_dump()
            new_construction_object = ConstructionObjectOrm(**data)
            session.add(new_construction_object)
            await session.flush()
            await session.commit()
            return new_construction_object.id

    @classmethod
    async def get_all_construction_objects(cls) -> list[SConstructionObject]:
        async with new_session() as session:
            query = select(ConstructionObjectOrm)
            result = await session.execute(query)
            construction_object_models = result.scalars().all()
            construction_object_schemas = [SConstructionObject.model_validate(construction_object_model) for
                                           construction_object_model in construction_object_models]
            return construction_object_schemas

    @classmethod
    async def add_violation(cls, violation: SViolationAdd) -> int:
        async with new_session() as session:
            data = violation.model_dump()
            new_violation = ViolationOrm(**data)
            session.add(new_violation)
            await session.flush()
            await session.commit()
            return new_violation.id

    @classmethod
    async def get_violations_by_contractor_id(cls, contractor_id: int) -> list[SViolation]:
        async with new_session() as session:
            query = select(ViolationOrm).where(ViolationOrm.contractor_id == contractor_id)
            result = await session.execute(query)
            violation_models = result.scalars().all()
            violation_schemas = [SViolation.model_validate(violation_model) for violation_model in violation_models]
            return violation_schemas

    @classmethod
    async def get_violations_by_construction_object_id(cls, construction_object_id: int) -> list[SViolation]:
        async with new_session() as session:
            query = select(ViolationOrm).where(ViolationOrm.construction_object_id == construction_object_id)
            result = await session.execute(query)
            violation_models = result.scalars().all()
            violation_schemas = [SViolation.model_validate(violation_model) for violation_model in violation_models]
            return violation_schemas

    @classmethod
    async def get_violation_by_id(cls, violation_id: int) -> Union[SViolation, None]:
        async with new_session() as session:
            query = select(ViolationOrm).where(ViolationOrm.id == violation_id)
            result = await session.execute(query)
            violation_model = result.scalar()
            if violation_model:
                return SViolation.model_validate(violation_model)
            return None

    @classmethod
    async def update_violation_status(cls, violation_id: int, new_status: str) -> None:
        async with new_session() as session:
            query = update(ViolationOrm).where(ViolationOrm.id == violation_id).values(resolution_status=new_status)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_violation(cls, violation_id: int) -> None:
        async with new_session() as session:
            query = delete(ViolationOrm).where(ViolationOrm.id == violation_id)
            await session.execute(query)
            await session.commit()
