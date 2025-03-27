from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import *
import os


class DataBase():
    def __init__(self):
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_name = os.getenv("DB_NAME")
        self.connect = f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'
        self.async_engine = create_async_engine(self.connect)
        self.Session = async_sessionmaker(bind=self.async_engine, class_=AsyncSession)
    
    # Функция создает таблицы в бд в соответствии с моделями    
    async def create_db(self):
        async with self.async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)
            
    # Функция получает инфу о пользователе по тг id (использ в комманде страт)
    async def get_user(self, user_id):
        async with self.Session() as request:
            result = await request.execute(select(Users).where(Users.telegram_id == user_id))
        # scalar() возвращает 1-ое значение 1-ой строки результата
        return result.scalar()
    
    # Функция добавляет запись в бд 
    async def add_user(self, name, phone, telegram_id):
        async with self.Session() as request:
            request.add(Users(
                username=name,
                userphone=phone,
                telegram_id=telegram_id
            ))
            # commit() - применить изменения в бд
            await request.commit()