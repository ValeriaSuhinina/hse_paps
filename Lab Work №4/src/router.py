from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status

from database import new_session, UserOrm
from repository import ConstructionSupervisionRepository
from schemas import SConstructionObjectAdd, SConstructionObject, SConstructionObjectId, SViolationAdd, SViolation, \
    SUserAdd, SViolationUpdateStatus

router = APIRouter()

user_router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@user_router.post("")
async def add_user(user: SUserAdd) -> SConstructionObjectId:
    # Проверяем, существует ли пользователь с таким логином
    async with new_session() as session:
        existing_user = await session.execute(select(UserOrm).where(UserOrm.login == user.login))
        if existing_user.scalar():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Пользователь с таким логином уже существует")

    # Если пользователь с таким логином не существует, добавляем нового пользователя
    new_user_id = await ConstructionSupervisionRepository.add_user(user)
    return {"id": new_user_id}


construction_object_router = APIRouter(
    prefix="/construction_object",
    tags=["Объекты Строительства"],
)


@construction_object_router.post("")
async def add_construction_object(construction_object: SConstructionObjectAdd) -> SConstructionObjectId:
    new_construction_object_id = await ConstructionSupervisionRepository.add_construction_object(construction_object)
    return {"id": new_construction_object_id}


@construction_object_router.get("")
async def get_all_construction_objects() -> list[SConstructionObject]:
    construction_objects = await ConstructionSupervisionRepository.get_all_construction_objects()
    return construction_objects


violation_router = APIRouter(
    prefix="/violation",
    tags=["Нарушения"],
)


@violation_router.post("")
async def add_violation(violation: SViolationAdd) -> SConstructionObjectId:
    new_violation_id = await ConstructionSupervisionRepository.add_violation(violation)
    return {"id": new_violation_id}


@violation_router.get("/by_contractor_id")
async def get_violations_by_contractor_id(contractor_id: int) -> list[SViolation]:
    violations = await ConstructionSupervisionRepository.get_violations_by_contractor_id(contractor_id)
    return violations


@violation_router.get("/by_construction_object_id")
async def get_violations_by_construction_object_id(construction_object_id: int) -> list[SViolation]:
    violations = await ConstructionSupervisionRepository.get_violations_by_construction_object_id(
        construction_object_id)
    return violations


@violation_router.put("")
async def update_violation_status(violation_update: SViolationUpdateStatus) -> None:
    violation_id = violation_update.id
    new_status = violation_update.new_status.value

    # Проверяем, существует ли нарушение с указанным идентификатором
    violation = await ConstructionSupervisionRepository.get_violation_by_id(violation_id)
    if not violation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Нарушение с указанным идентификатором не найдено")

    # Обновляем статус нарушения
    await ConstructionSupervisionRepository.update_violation_status(violation_id, new_status)


@violation_router.delete("{violation_id}")
async def delete_violation(violation_id: int) -> None:
    # Проверяем, существует ли нарушение с указанным идентификатором
    violation = await ConstructionSupervisionRepository.get_violation_by_id(violation_id)
    if not violation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Нарушение с указанным идентификатором не найдено")

    # Удаляем нарушение
    await ConstructionSupervisionRepository.delete_violation(violation_id)


router.include_router(user_router)
router.include_router(construction_object_router)
router.include_router(violation_router)
