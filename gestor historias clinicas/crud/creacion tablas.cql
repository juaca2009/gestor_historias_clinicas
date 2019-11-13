--creacion del key space
CREATE KEYSPACE IF NOT EXISTS historias_clinicas
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };

--CREACION TABLAS

--tabla login
CREATE TABLE login(
  nro_documento int primary key,
  correo text,
  contrasena text,
  rol text
);

--tabla asignacion examenes
CREATE TABLE asignacion_examenes(
  tipo_examen text primary key,
  id_enfermero int,
  nombre text,
  apellido text,
  nro_cola int
);

--tabla rol usuario
CREATE TABLE rol_usuario(
  rol text,
  nro_documento int,
  tipo_documento text,
  nombre text, 
  apellidos text,
  fecha_nacimiento date,
  ciudad text,
  departamento text,
  direccion text,
  numero_cel int,
  telefono int,
  especialidad text,
  razon_social text,
  primary key(rol, nro_documento)
);

--tabla paciente historia clinica
CREATE TABLE paciente_historia(
  nro_documento int,
  id_historia int,
  fecha date,
  nombre_doctor text,
  apellido_doctor text,
  especialidad text,
  nombre_enfermero text,
  apellido_enfermero text,
  tipo_examen text,
  comentarios text,
  primary key(nro_documento, id_historia)
);

--tabla colas consultas
CREATE TABLE colas_consultas(
    nro_cola int,
    nro_documento int,
    nombre_paciente text,
    apellido_paciente text,
    nombre_doctor text,
    apellido_doctor text,
    especialidad text,
    posicion int,
    primary key(nro_cola, nro_documento)
);


--tabla colas examenes
CREATE TABLE colas_examenes(
    nro_cola int,
    nro_documento int,
    nombre_paciente text,
    apellido_paciente text,
    nombre_enfermero text,
    apellido_enfermero text,
    tipo_examen text,
    posicion int,
    primary key(nro_cola, nro_documento)
);

--especializacion examenes
CREATE TABLE especializacion_examenes(
  especializacion text,
  tipo_examen text,
  descripcion text,
  primary key(especializacion, tipo_examen)
);

--tabla paciente examen
CREATE TABLE paciente_examenes(
  nro_documento int,
  tipo_examen text,
  fecha date,
  nombre_enfermero text,
  apellido_enfermero text,
  primary key(nro_documento, tipo_examen)
);

CREATE TABLE asignacion_consultas(
  nro_documento int primary key,
  especialidad text,
  nombre_doctor text,
  apellido_doctor text,
  nro_cola int
);

