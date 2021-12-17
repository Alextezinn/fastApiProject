from sqlalchemy import Column, Integer, String, Text

from fastApiProject.db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String)
    subject = Column(String)
    content = Column(Text)
    rating = Column(Integer)


posts = Post.__table__
