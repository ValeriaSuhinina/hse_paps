from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine("sqlite+aiosqlite:///constructionSupervision.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class UserOrm(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    role = Column(String)


class ConstructionObjectOrm(Model):
    __tablename__ = 'construction_objects'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    type: Mapped[str | None]

    violations = relationship("ViolationOrm", back_populates="construction_object")


class ViolationOrm(Model):
    __tablename__ = 'violations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    resolution_status = Column(String)
    contractor_id = Column(Integer)
    supervisor_id = Column(Integer)
    construction_object_id = Column(Integer, ForeignKey('construction_objects.id'))
    violation_classifier = Column(String)

    construction_object = relationship("ConstructionObjectOrm", back_populates="violations")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
