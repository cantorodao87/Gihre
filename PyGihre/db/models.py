from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Trabajador(Base):
    __tablename__ = 'trabajadores'

    id = Column('id_trabajador', Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    grupo = Column(Integer, nullable=False)
    grafico = Column(String)

    asignaciones = relationship("Asignacion", back_populates="trabajador")

class Clave(Base):
    __tablename__ = 'claves'

    id = Column('id_clave', Integer, primary_key=True)
    tipo = Column(String, nullable=False)
    hora_comienzo = Column(String, nullable=False)
    hora_final = Column(String, nullable=False)

    asignaciones = relationship("Asignacion", back_populates="clave")

class Asignacion(Base):
    __tablename__ = 'asignaciones'

    id = Column('id_asignacion', Integer, primary_key=True, autoincrement=True)
    dia = Column(Integer, nullable=False)
    trabajador_id = Column(Integer, ForeignKey('trabajadores.id_trabajador'), nullable=False)
    clave_id = Column(Integer, ForeignKey('claves.id_clave'), nullable=False)

    trabajador = relationship("Trabajador", back_populates="asignaciones")
    clave = relationship("Clave", back_populates="asignaciones")

class Grafico(Base):
    __tablename__ = 'graficos'
    id = Column('id_grafico', Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    turnos = Column(String, nullable=False)
