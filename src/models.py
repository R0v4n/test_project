from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Date, \
    Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    code = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)


class ValueType(Base):
    __tablename__ = 'types'

    type = Column(Integer,
                  primary_key=True,
                  nullable=False,
                  autoincrement=True)
    desc = Column(String(20), nullable=False)


class DataRecord(Base):
    __tablename__ = 'records'

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.code'))
    file_version = Column(Integer, ForeignKey('files.version'))
    date = Column(Date, nullable=False)
    value = Column(Float)
    kind = Column(Integer, ForeignKey('types.type'))

    projects = relationship('Project', backref='records')
    types = relationship('ValueType', backref='records')


class File(Base):
    __tablename__ = 'files'

    version = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DateTime, nullable=False)
    name = Column(String(20), nullable=False)
