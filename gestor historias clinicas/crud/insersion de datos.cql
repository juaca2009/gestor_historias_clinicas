--datos rol usuario
copy rol_usuario (rol, nro_documento, tipo_documento, nombre, apellidos, fecha_nacimiento, ciudad, departamento, direccion, numero_cel, telefono, especialidad, razon_social)
from '/home/camilo/Documentos/proyecto ingenieria de software/codigo/GHC cassandra/gestor historias clinicas/crud/datos/rol_usuarios.csv'
with delimiter=',' and header=TRUE; 

--datos especializacion examen
copy especializacion_examenes (especializacion, tipo_examen, descripcion)
from '/home/camilo/Documentos/proyecto ingenieria de software/codigo/GHC cassandra/gestor historias clinicas/crud/datos/especializacion_examenes.csv'
with delimiter=',' and header=TRUE;

--datos asignacion examenes
copy asignacion_examenes (tipo_examen, id_enfermero, nombre, apellido)
from '/home/camilo/Documentos/proyecto ingenieria de software/codigo/GHC cassandra/gestor historias clinicas/crud/datos/asignacion_examenes.csv'
with delimiter=',' and header=TRUE;

--paciente historias
copy paciente_historia (nro_documento, id_historia, apellido_doctor, apellido_enfermero,comentarios, especialidad,fecha, nombre_doctor, nombre_enfermero, tipo_examen )
from '/home/camilo/Documentos/proyecto ingenieria de software/codigo/GHC cassandra/gestor historias clinicas/crud/datos/paciente_historia.csv'
with delimiter=',' and header=TRUE;