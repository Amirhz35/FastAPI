from sqlalchemy import Boolean,Column,String,Integer

from database import Base


class URL(Base):
    __tablename__ = "URL"

    id = Column(Integer,primary_key=True,index=True)
    original_url = Column(String)
    short_url = Column(String)

    