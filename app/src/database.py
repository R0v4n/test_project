import datetime
from typing import Dict

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Project, Base, ValueType, File, DataRecord
from excel_file import write_excel

engine = create_engine('postgresql+psycopg2://admin:admin@postgres')
Session = sessionmaker(bind=engine)
session = Session()


def init_db() -> None:
    """
    Function to initialize DB
    :return: None
    """
    Base.metadata.create_all(bind=engine)
    type_plan = ValueType(desc='plan')
    type_fact = ValueType(desc='fact')
    session.add_all((type_plan, type_fact))
    session.commit()


def add_data(data: Dict, version: int) -> None:
    """
    Add data from dictionary to DB with signed version of uploaded file.
    :param data: data received from uploaded file
    :param version: version of uploaded file
    :return: None
    """
    projects = []
    records = []
    exist_project = list(map(lambda x: x[0],
                             session.query(Project.code).all()))
    for key in data:
        if key not in exist_project:
            projects.append(Project(code=key, name=data[key]['name']))
        for record in data[key]:
            if isinstance(record, datetime.date):
                record_plan = DataRecord(
                    file_version=version,
                    project_id=key,
                    date=record,
                    value=data[key][record][0],
                    kind=1
                )
                record_fact = DataRecord(
                    file_version=version,
                    project_id=key,
                    date=record,
                    value=data[key][record][1],
                    kind=2
                )
                records.extend([record_plan, record_fact])
    session.add_all(projects)
    session.commit()
    session.add_all(records)
    session.commit()


def download_data(version: int) -> None:
    """
    Get data with required version of uploaded file and write to Excel file
    :param version: version of uploaded file
    :return: None
    """
    data = (session.query(DataRecord)
            .filter(DataRecord.file_version == version)
            .join(DataRecord.projects).all())
    dict = {}
    for record in data:
        if record.project_id not in dict:
            dict[record.project_id] = {
                'name': record.projects.name
            }
        if record.date not in dict[record.project_id]:
            dict[record.project_id][record.date] = [None, None]
        if record.kind == 1:
            dict[record.project_id][record.date][0] = record.value
        if record.kind == 2:
            dict[record.project_id][record.date][1] = record.value
    write_excel(dict)


def get_diagram_data(version: int, year: int, kind_of_value: str) -> Dict:
    """
    Get data with required parameters for diagram
    :param version: version of uploaded file
    :param year: year for required data
    :param kind_of_value: kind of value in table - plan or fact
    :return: dictionary with required data
    """
    if kind_of_value == 'plan':
        kind = 1
    elif kind_of_value == 'fact':
        kind = 2
    else:
        raise ValueError('Kind of value should be plan or fact!')
    data = (session.query(DataRecord.date, func.sum(DataRecord.value))
            .filter(
        DataRecord.date >= datetime.date(year=year, month=1, day=1),
        DataRecord.date <= datetime.date(year=year, month=12, day=31),
        DataRecord.file_version == version,
        DataRecord.kind == kind)
            .group_by(DataRecord.date).all())
    data_dict = {}
    for item in data:
        data_dict[str(item[0])] = round(item[1], 4)
    return data_dict


def add_file(name: str) -> int:
    """
    Add info about new uploaded file to DB
    :param name: name of uploaded file
    :return: version of uploaded file
    """
    new_file = File(date_time=datetime.datetime.now(), name=name)
    session.add(new_file)
    session.commit()
    return new_file.version
