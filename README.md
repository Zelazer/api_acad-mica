# API Académica

API educativa construida con **FastAPI, SQLModel y SQLite**. Permite administrar **cursos** (CRUD completo) y **estudiantes** (crear y consultar), y sirve para estudiar cómo una petición HTTP atraviesa un proyecto organizado por responsabilidades: router, schema, service, model, sesión y base de datos.

La explicación detallada del proyecto base, la práctica con Swagger y los ejercicios están en la [guía para estudiantes](docs.md). Los retos que originaron esta ampliación están en [ejercicio.md](ejercicio.md) y las pruebas realizadas en [entrega-pruebas/informe-pruebas.md](entrega-pruebas/informe-pruebas.md).

## Contenido

1. [Funcionalidades](#funcionalidades)
2. [Tecnologías](#tecnologías)
3. [Inicio rápido](#inicio-rápido)
4. [Cómo funciona la aplicación](#cómo-funciona-la-aplicación)
5. [Endpoints](#endpoints)
6. [Recurso Courses](#recurso-courses)
7. [Recurso Students](#recurso-students)
8. [Códigos de estado HTTP](#códigos-de-estado-http)
9. [Persistencia de datos](#persistencia-de-datos)
10. [Pruebas realizadas](#pruebas-realizadas)
11. [Estructura del proyecto](#estructura-del-proyecto)

## Funcionalidades

- **Cursos:** crear, listar, consultar por ID, actualizar (`PUT`, reemplazo completo) y eliminar.
- **Estudiantes:** crear, listar y consultar por ID. Es un recurso independiente de los cursos.
- Validar los datos de entrada y responder con los errores HTTP adecuados (`404` y `422`).
- Conservar los registros en una base de datos SQLite local (`database.db`) que sobrevive a los reinicios del servidor.
- Documentación interactiva generada automáticamente con Swagger UI.

## Tecnologías

| Herramienta | Uso |
| --- | --- |
| FastAPI | Aplicación web, rutas y documentación interactiva. |
| Uvicorn | Servidor que ejecuta la API. |
| SQLModel | Modelos de tablas y operaciones de base de datos. |
| Pydantic | Esquemas y validación de datos. |
| SQLite | Almacenamiento en el archivo local `database.db`. |

Las versiones utilizadas están en [requirements.txt](requirements.txt). El proyecto se ha ejecutado con **Python 3.12** y también con 3.14.

## Inicio rápido

Abre una terminal en la carpeta del proyecto, donde está `main.py`.

### 1. Crear y activar el entorno virtual

En Linux o macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

En Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si el entorno `venv` ya existe, basta con activarlo.

### 2. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 3. Ejecutar la API

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

`main:app` identifica el objeto `app` del archivo `main.py`. La opción `--reload` recarga el servidor cuando editas el código durante el desarrollo. Para detenerlo, presiona `Ctrl+C`.

Abre la [documentación interactiva Swagger](http://127.0.0.1:8000/docs) para probar los endpoints con **Try it out → Execute**. Verás dos secciones: **Courses** (5 endpoints) y **Students** (3 endpoints).

La base de datos y sus tablas se crean al iniciar la aplicación. Ejecuta el comando siempre desde la raíz del proyecto para usar el mismo archivo `database.db`.

## Cómo funciona la aplicación

### El recorrido de una petición

```text
Cliente (Swagger, curl, navegador)
        ↓  petición HTTP
Router      recibe la petición y la dirige a la función correcta
        ↓
Schema      valida el JSON de entrada (si falla: 422)
        ↓
Service     ejecuta la operación sobre los datos (si no existe: 404)
        ↓
Model       representa la tabla en Python
        ↓
Session     realiza la operación en la base de datos
        ↓
SQLite      guarda los datos en database.db
        ↓
Respuesta JSON, moldeada por el schema de salida
```

### Responsabilidad de cada capa

| Capa | Carpeta | Qué hace | Qué NO hace |
| --- | --- | --- | --- |
| **Router** | `routers/` | Define las rutas y métodos HTTP, recibe los parámetros y delega en el service. | No contiene lógica de datos. |
| **Schema** | `schemas/` | Define y valida los datos que entran y salen de la API (Pydantic). | No es una tabla. |
| **Service** | `services/` | Contiene las operaciones: crear, buscar, actualizar, eliminar. Lanza el `404` si no existe el registro. | No conoce HTTP más allá de `HTTPException`. |
| **Model** | `models/` | Clase con `table=True` que representa una tabla de la base de datos. | No valida la entrada del cliente. |
| **Database** | `database/` | Crea el motor, las tablas y entrega una sesión por petición. | No sabe nada de cursos ni estudiantes. |

La diferencia entre **schema** y **model**: el schema describe qué datos acepta o devuelve la API (con sus reglas de validación), y el model describe cómo se guardan en la tabla. Por eso `CourseCreate` pide `name`, `credits` y `active`, mientras que `CourseResponse` agrega el `id` que genera la base de datos.

### `main.py`: arranque de la aplicación

`main.py` crea la aplicación `FastAPI` y registra los dos routers con `include_router`: el de cursos y el de estudiantes. La función `lifespan` ejecuta `create_db_and_tables()` antes de aceptar peticiones.

Al importar cada router, Python importa también su service y su model. Así `Course` y `Student` quedan registrados en `SQLModel.metadata` antes de que `create_all()` cree las tablas. Si un router no se importara en `main.py`, su tabla no se crearía.

### `database/database.py`: conexión y sesiones

- `DATABASE_URL = "sqlite:///database.db"` apunta a un archivo local. La ruta es relativa a la carpeta desde la que se ejecuta Uvicorn.
- `engine` administra las conexiones al archivo.
- `create_db_and_tables()` ejecuta `SQLModel.metadata.create_all(engine)`: crea el archivo y las tablas que falten, pero no modifica tablas existentes.
- `get_session()` entrega una `Session` por petición y la cierra al terminar. Los endpoints la reciben con `Depends(get_session)` (inyección de dependencias).

Los dos recursos usan **la misma base de datos**. Dentro de `database.db` hay dos tablas:

```text
database.db
├── course
└── student
```

### Las tres operaciones de escritura de la sesión

```python
session.add(objeto)       # incorpora el objeto a la sesión
session.commit()          # confirma la transacción y guarda en SQLite
session.refresh(objeto)   # recarga el objeto (por ejemplo, el ID generado)
```

Para eliminar se usa `session.delete(objeto)` seguido de `session.commit()`.

## Endpoints

| Método | Ruta | Operación | Estado de éxito |
| --- | --- | --- | --- |
| `POST` | `/courses` | Crear un curso. | `201` |
| `GET` | `/courses` | Listar todos los cursos. | `200` |
| `GET` | `/courses/{course_id}` | Consultar un curso por ID. | `200` |
| `PUT` | `/courses/{course_id}` | Actualizar un curso (los 3 campos obligatorios). | `200` |
| `DELETE` | `/courses/{course_id}` | Eliminar un curso. | `200` |
| `POST` | `/students` | Crear un estudiante. | `201` |
| `GET` | `/students` | Listar estudiantes. | `200` |
| `GET` | `/students/{student_id}` | Consultar un estudiante por ID. | `200` |

La ruta `/` no está definida: utiliza `/docs` o `/courses`.

## Recurso Courses

### Reglas de entrada

| Campo | `CourseCreate` (POST) | `CourseUpdate` (PUT) |
| --- | --- | --- |
| `name` | Obligatorio; entre 3 y 80 caracteres. | Obligatorio; entre 3 y 80 caracteres. |
| `credits` | Obligatorio; entero entre 1 y 6. | Obligatorio; entero entre 1 y 6. |
| `active` | **Opcional**; por defecto `true`. | **Obligatorio**; booleano. |

`CourseCreate` y `CourseUpdate` son schemas distintos porque `active` se comporta distinto: al crear puede omitirse, pero la actualización es un **reemplazo completo** y exige los tres campos. Omitir `active` en un `PUT` devuelve `422`.

### Crear: `POST /courses`

```bash
curl -i -X POST http://127.0.0.1:8000/courses \
  -H 'Content-Type: application/json' \
  -d '{"name": "Programación I", "credits": 3, "active": true}'
```

Responde `201 Created`. El ID lo asigna SQLite, no se envía:

```json
{ "id": 1, "name": "Programación I", "credits": 3, "active": true }
```

### Listar y consultar: `GET /courses` y `GET /courses/{course_id}`

`GET /courses` devuelve una lista (vacía `[]` si no hay cursos) e incluye cursos activos e inactivos. `GET /courses/1` devuelve un curso, o `404` con `{"detail": "Course not found"}` si no existe.

### Actualizar: `PUT /courses/{course_id}`

```bash
curl -i -X PUT http://127.0.0.1:8000/courses/1 \
  -H 'Content-Type: application/json' \
  -d '{"name": "Programación II", "credits": 4, "active": false}'
```

Responde `200 OK` con el curso actualizado:

```json
{ "id": 1, "name": "Programación II", "credits": 4, "active": false }
```

Cómo funciona por dentro (`update_course` en `services/course_service.py`):

1. Busca el curso con `get_course`; si no existe, se lanza el `404` y no se modifica nada.
2. Reemplaza `name`, `credits` y `active` en el objeto que ya existe.
3. Ejecuta `commit()`: al ser un objeto ya guardado, SQLModel genera un `UPDATE`, no un `INSERT`.

Por eso **el ID se conserva** y **no se crea un curso nuevo**: se modifica el registro existente.

### Eliminar: `DELETE /courses/{course_id}`

```bash
curl -i -X DELETE http://127.0.0.1:8000/courses/2
```

Responde `200 OK`:

```json
{ "message": "Course deleted" }
```

Cómo funciona por dentro (`delete_course` en el service):

1. Busca el curso con `get_course`; si no existe, `404` con `{"detail": "Course not found"}`.
2. Ejecuta `session.delete(course)` y `session.commit()`.

Eliminar el mismo ID por segunda vez devuelve `404`, y `/courses/abc` devuelve `422` porque el ID debe ser un entero. La lógica vive en el service y no en el router, para mantener cada capa con una sola responsabilidad.

## Recurso Students

Los estudiantes siguen exactamente la misma arquitectura que los cursos, pero en archivos propios: **no se mezcla nada con `Course`**.

### Archivos del recurso

| Archivo | Contenido |
| --- | --- |
| `models/student.py` | Clase `Student` con `table=True`: crea la tabla `student`. |
| `schemas/student.py` | `StudentCreate` (entrada) y `StudentResponse` (salida). |
| `services/student_service.py` | `create_student`, `list_students` y `get_student`. |
| `routers/students.py` | Router con prefijo `/students` y etiqueta `Students`. |
| `main.py` | Registra el router con `app.include_router(students_router)`. |

### Modelo y reglas de entrada

| Campo | Tipo | Regla |
| --- | --- | --- |
| `id` | Entero | Clave primaria generada por SQLite. No se envía. |
| `name` | Texto | Obligatorio; entre 3 y 80 caracteres. |
| `email` | Texto | Obligatorio y no vacío (mínimo 1 carácter). No se valida el formato del correo. |
| `semester` | Entero | Obligatorio; entre 1 y 10. |
| `active` | Booleano | Opcional; por defecto `true`. |

### Crear: `POST /students`

```bash
curl -i -X POST http://127.0.0.1:8000/students \
  -H 'Content-Type: application/json' \
  -d '{"name": "Ana Pérez", "email": "ana@universidad.edu", "semester": 4}'
```

Responde `201 Created`. Como se omitió `active`, queda en `true`:

```json
{
  "id": 1,
  "name": "Ana Pérez",
  "email": "ana@universidad.edu",
  "semester": 4,
  "active": true
}
```

Cómo funciona por dentro (`create_student` en el service):

1. FastAPI valida el cuerpo con `StudentCreate`; si falla, responde `422` y el service no se ejecuta.
2. El service convierte el schema en un objeto `Student` (el modelo de la tabla).
3. `session.add()`, `session.commit()` y `session.refresh()` lo guardan y recuperan el `id` generado.
4. El router devuelve el resultado moldeado con `StudentResponse`.

### Listar y consultar: `GET /students` y `GET /students/{student_id}`

`GET /students` devuelve la lista completa, con estudiantes activos e inactivos. `GET /students/1` devuelve un estudiante. Si el ID no existe:

```json
{ "detail": "Student not found" }
```

con estado `404`. Un ID que no es entero, como `/students/abc`, devuelve `422`.

### Por qué Students usa la misma base de datos

El `engine` y la función `get_session` no dependen de ningún recurso: solo apuntan al archivo `database.db`. Al importar `Student` con `table=True`, su tabla se registra en los mismos metadatos de SQLModel, y `create_all()` la crea junto a `course` en el mismo archivo. No hace falta crear `students.db`.

Como `database.db` ya podía existir con la tabla `course`, `create_all()` solo agrega la tabla `student` que falta y no toca los cursos guardados.

## Códigos de estado HTTP

| Estado | Cuándo ocurre |
| --- | --- |
| `200` | Consulta, actualización o eliminación correcta. |
| `201` | Curso o estudiante creado correctamente. |
| `404` | El curso o estudiante no existe (`Course not found` / `Student not found`). |
| `422` | Los datos incumplen el schema, falta un campo obligatorio o el ID no es un entero. |

**404 y 422 no significan lo mismo:** el `404` indica que la petición era válida pero el recurso no existe; el `422` indica que la petición en sí no cumple lo que la API espera, y se rechaza antes de ejecutar el service.

## Persistencia de datos

Los datos no viven en memoria: se guardan en el archivo `database.db` mediante `commit()`. Por eso:

- Al detener Uvicorn con `Ctrl+C` y volver a ejecutarlo, los cursos y estudiantes siguen ahí.
- Los cambios hechos con `PUT` permanecen.
- Los cursos eliminados con `DELETE` siguen eliminados.

El archivo `database.db` es local y **no se sube al repositorio** (está en `.gitignore`), igual que el entorno virtual `venv/`. Si lo borras y reinicias la API, se crea una base nueva y vacía.

## Pruebas realizadas

Las pruebas se hicieron manualmente desde Swagger (`/docs`) y están documentadas caso por caso en [entrega-pruebas/informe-pruebas.md](entrega-pruebas/informe-pruebas.md), con su captura en [entrega-pruebas/evidencias/](entrega-pruebas/evidencias/).

| Bloque | Casos | Qué se comprueba |
| --- | --- | --- |
| Proyecto base | P01–P04 | Crear y consultar cursos. |
| Reto 1: DELETE | D01–D06 | Eliminar, `404` al repetir, `422` con ID no entero y persistencia. |
| Reto 2: PUT | U01–U08 | Actualizar conservando el ID, validaciones, `404` y persistencia. |
| Reto 3: Students | S01–S11 | Crear, listar, consultar, `404`, `422` y validaciones de campos. |
| Persistencia | R01–R02 | Los datos siguen tras reiniciar Uvicorn. |

Los casos con `422` por un ID no entero (`D05` y `S07`) se ejecutaron con `curl.exe`, porque Swagger UI bloquea ese valor en el navegador y nunca envía la petición.

## Estructura del proyecto

```text
api_acad-mica/
├── main.py                     # Aplicación y ciclo de vida
├── database/
│   └── database.py             # Motor SQLite, creación de tablas y sesiones
├── models/
│   ├── course.py               # Tabla de cursos
│   └── student.py              # Tabla de estudiantes
├── schemas/
│   ├── course.py               # CourseCreate, CourseUpdate, CourseResponse
│   └── student.py              # StudentCreate, StudentResponse
├── routers/
│   ├── courses.py              # Endpoints de cursos
│   └── students.py             # Endpoints de estudiantes
├── services/
│   ├── course_service.py       # Crear, listar, consultar, actualizar, eliminar
│   └── student_service.py      # Crear, listar, consultar
├── entrega-pruebas/
│   ├── informe-pruebas.md      # Informe de pruebas
│   └── evidencias/             # Capturas de Swagger
├── requirements.txt            # Dependencias
├── docs.md                     # Guía didáctica detallada
├── ejercicio.md                # Retos propuestos
└── README.md                   # Presentación e inicio rápido
```