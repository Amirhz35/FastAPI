from sqlalchemy import Boolean,Column,String,Integer,ForeignKey

from database import Base


class UserModel(Base):
    __tablename__ = "CustomUser"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)



class URL(Base):
    __tablename__ = "URL"

    id = Column(Integer,primary_key=True,index=True)
    original_url = Column(String)
    short_url = Column(String)
    user_id = Column(Integer,ForeignKey("CustomUser.id"))
    count = Column(Integer, default=0)