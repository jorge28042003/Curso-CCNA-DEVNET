# gestion_usuarios.py

from passlib.hash import sha256_crypt
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la conexión a la base de datos SQLite
engine = create_engine('sqlite:///usuarios.db', echo=True)
Base = declarative_base()

# Definir la tabla de usuarios
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    contraseña = Column(String)

# Crear la tabla en la base de datos (si no existe)
Base.metadata.create_all(engine)

# Crear una sesión de SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

def hash_contraseña(contraseña):
    # Generar hash de la contraseña usando sha256_crypt
    return sha256_crypt.hash(contraseña)

def almacenar_usuario(nombre, apellido, contraseña):
    # Almacenar usuario y contraseña hasheada en la base de datos
    hash_contraseña = hash_contraseña(contraseña)
    nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, contraseña=hash_contraseña)
    session.add(nuevo_usuario)
    session.commit()

def validar_usuario(nombre, apellido, contraseña):
    # Validar usuario
    usuario = session.query(Usuario).filter_by(nombre=nombre, apellido=apellido).first()
    if usuario and sha256_crypt.verify(contraseña, usuario.contraseña):
        return True
    else:
        return False

if __name__ == "__main__":
    # Ejemplo de uso:
    # Almacenar un usuario
    nombre = "Jorge"
    apellido = "Marchant"
    contraseña = "28042003"
    almacenar_usuario(nombre, apellido, contraseña)

    # Validar usuario
    usuario_valido = validar_usuario(nombre, apellido, contraseña)
    print(f"¿El usuario es válido? {usuario_valido}")

# You can add to this file in the editor 
