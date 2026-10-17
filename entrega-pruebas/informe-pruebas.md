# Informe de pruebas — API Académica

**Estudiante:** Juan David Herrera Gonzalez
**Fecha:** 16/10/2026 
**Repositorio:** https://github.com/Zelazer/api_acad-mica


## Proyecto base

### Caso P01
| Campo | Información |
| --- | --- |
| Endpoint | `POST /courses` |
| Datos enviados | `{"name":"Desarrollo Web II","credits":3,"active":true}` |
| Resultado esperado | Curso creado con ID generado |
| Código HTTP esperado | 201 |
| Resultado obtenido | Curso creado correctamente con `id: 1`, `name: "Desarrollo Web II"`, `credits: 3`, `active: true`. |
| Código HTTP obtenido | 201 |
| Estado | Aprobado |
| Evidencia | `evidencias/P01.png` |

### Caso P02
| Campo | Información |
| --- | --- |
| Endpoint | `POST /courses` |
| Datos enviados | `{"name":"Redes","credits":3}` |
| Resultado esperado | Curso creado; active queda en true |
| Código HTTP esperado | 201 |
| Resultado obtenido | Curso creado con `id: 2`, `name: "Redes"`, `credits: 3`. Al omitir `active`, quedó en `true` por defecto. |
| Código HTTP obtenido | 201 |
| Estado | Aprobado |
| Evidencia | `evidencias/P02.png` |

### Caso P03
| Campo | Información |
| --- | --- |
| Endpoint | `GET /courses` |
| Datos enviados | `—` |
| Resultado esperado | Lista con los cursos creados |
| Código HTTP esperado | 200 |
| Resultado obtenido | Lista con los 2 cursos creados: id 1 (Desarrollo Web II) e id 2 (Redes). |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/P03.png` |

### Caso P04
| Campo | Información |
| --- | --- |
| Endpoint | `GET /courses/1` |
| Datos enviados | `—` |
| Resultado esperado | Curso con id 1 |
| Código HTTP esperado | 200 |
| Resultado obtenido | Devolvió el curso con `id: 1`, `name: "Desarrollo Web II"`, `credits: 3`, `active: true`. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/P04.png` |


## Reto 1 — DELETE

### Caso D01
| Campo | Información |
| --- | --- |
| Endpoint | `DELETE /courses/2` |
| Datos enviados | `—` |
| Resultado esperado | {"message":"Course deleted"} |
| Código HTTP esperado | 200 |
| Resultado obtenido | El curso 2 se eliminó y la API respondió `{"message": "Course deleted"}`. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/D01.png` |

### Caso D02
| Campo | Información |
| --- | --- |
| Endpoint | `GET /courses/2` |
| Datos enviados | `—` |
| Resultado esperado | Course not found |
| Código HTTP esperado | 404 |
| Resultado obtenido | Al consultar el curso 2 eliminado, la API respondió `{"detail": "Course not found"}`. |
| Código HTTP obtenido | 404 |
| Estado | Aprobado |
| Evidencia | `evidencias/D02.png` |

### Caso D03
| Campo | Información |
| --- | --- |
| Endpoint | `GET /courses` |
| Datos enviados | `—` |
| Resultado esperado | Los demás cursos siguen existiendo |
| Código HTTP esperado | 200 |
| Resultado obtenido | La lista solo contiene el curso 1 (Desarrollo Web II); el curso 1 no se vio afectado por el borrado del curso 2. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/D03.png` |

### Caso D04
| Campo | Información |
| --- | --- |
| Endpoint | `DELETE /courses/2 (repetido)` |
| Datos enviados | `—` |
| Resultado esperado | Course not found |
| Código HTTP esperado | 404 |
| Resultado obtenido | Al intentar eliminar de nuevo el curso 2, la API respondió `{"detail": "Course not found"}`. |
| Código HTTP obtenido | 404 |
| Estado | Aprobado |
| Evidencia | `evidencias/D04.png` |

### Caso D05
| Campo | Información |
| --- | --- |
| Endpoint | `DELETE /courses/abc` |
| Datos enviados | `—` |
| Resultado esperado | Error de validación (ID no entero) |
| Código HTTP esperado | 422 |
| Resultado obtenido | El servidor rechazó el ID `abc` con error de validación: "Input should be a valid integer". Se ejecutó con `curl.exe` porque Swagger UI bloquea el valor en el cliente y no envía la petición. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/D05.png` |

### Caso D06
| Campo | Información |
| --- | --- |
| Endpoint | `GET /courses (tras reiniciar Uvicorn)` |
| Datos enviados | `—` |
| Resultado esperado | El curso eliminado sigue sin aparecer |
| Código HTTP esperado | 200 |
| Resultado obtenido | Tras reiniciar Uvicorn, la lista solo contiene el curso 1 (Desarrollo Web II). El curso 2 eliminado no reapareció. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/D06.png` |


## Reto 2 — PUT

### Caso U01
| Campo | Información |
| --- | --- |
| Endpoint | `PUT /courses/1` |
| Datos enviados | `{"name":"Programación II","credits":4,"active":false}` |
| Resultado esperado | Curso actualizado, mismo id |
| Código HTTP esperado | 200 |
| Resultado obtenido | El curso se actualizó conservando `id: 1`; ahora tiene `name: "Programación II"`, `credits: 4` y `active: false`. No se creó un curso nuevo. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/U01.png` |

### Caso U02
| Campo | Información |
| --- | --- |
| Endpoint | `GET /courses` |
| Datos enviados | `—` |
| Resultado esperado | Misma cantidad de cursos que antes; active=false |
| Código HTTP esperado | 200 |
| Resultado obtenido | La lista contiene un solo curso (`id: 1`), por lo que la cantidad de cursos no aumentó. El curso muestra `name: "Programación II"`, `credits: 4` y `active: false`. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/U02.png` |

### Caso U03
| Campo | Información |
| --- | --- |
| Endpoint | `PUT /courses/1` |
| Datos enviados | `{"name":"Programación II","credits":0,"active":true}` |
| Resultado esperado | Error de validación |
| Código HTTP esperado | 422 |
| Resultado obtenido | La API rechazó `credits: 0` con error de validación: tipo `greater_than_equal`, "Input should be greater than or equal to 1". No se modificó el curso. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/U03.png` |

### Caso U04
| Campo | Información |
| --- | --- |
| Endpoint | `PUT /courses/1` |
| Datos enviados | `{"name":"Programación II","credits":7,"active":true}` |
| Resultado esperado | Error de validación |
| Código HTTP esperado | 422 |
| Resultado obtenido | La API rechazó `credits: 7` con error de validación: tipo `less_than_equal`, "Input should be less than or equal to 6". No se modificó el curso. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/U04.png` |

### Caso U05
| Campo | Información |
| --- | --- |
| Endpoint | `PUT /courses/1` |
| Datos enviados | `{"name":"AB","credits":3,"active":true}` |
| Resultado esperado | Error de validación (nombre corto) |
| Código HTTP esperado | 422 |
| Resultado obtenido | La API rechazó el nombre "AB" con error de validación: tipo `string_too_short`, "String should have at least 3 characters". No se modificó el curso. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/U05.png` |

### Caso U06
| Campo | Información |
| --- | --- |
| Endpoint | `PUT /courses/1` |
| Datos enviados | `{"name":"Programación II","credits":3}` |
| Resultado esperado | Error de validación (falta active) |
| Código HTTP esperado | 422 |
| Resultado obtenido | La API rechazó la petición sin `active` con error de validación: tipo `missing`, campo `body.active`, "Field required". Confirma que en el PUT los tres campos son obligatorios. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/U06.png` |

### Caso U07
| Campo | Información |
| --- | --- |
| Endpoint | `PUT /courses/999` |
| Datos enviados | `{"name":"Programación II","credits":3,"active":true}` |
| Resultado esperado | Course not found |
| Código HTTP esperado | 404 |
| Resultado obtenido | Al actualizar el ID inexistente 999, la API respondió `{"detail": "Course not found"}`. No se creó ningún curso. |
| Código HTTP obtenido | 404 |
| Estado | Aprobado |
| Evidencia | `evidencias/U07.png` |

### Caso U08
| Campo | Información |
| --- | --- |
| Endpoint | `GET /courses/1 (tras reiniciar Uvicorn)` |
| Datos enviados | `—` |
| Resultado esperado | Los cambios del PUT permanecen |
| Código HTTP esperado | 200 |
| Resultado obtenido | Tras reiniciar Uvicorn, el curso 1 conserva los cambios del PUT: `name: "Programación II"`, `credits: 4`, `active: false`. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/U08.png` |


## Reto 3 — Students

### Caso S01
| Campo | Información |
| --- | --- |
| Endpoint | `Swagger /docs` |
| Datos enviados | `—` |
| Resultado esperado | Se ven las rutas de Courses y Students |
| Código HTTP esperado | — |
| Resultado obtenido | Swagger `/docs` muestra la sección **Courses** (GET y POST `/courses`, GET, DELETE y PUT `/courses/{course_id}`) y la sección **Students** (GET y POST `/students`, GET `/students/{student_id}`). En *Schemas* aparecen `CourseUpdate`, `StudentCreate` y `StudentResponse`. |
| Código HTTP obtenido | — |
| Estado | Aprobado |
| Evidencia | `evidencias/S01.png` |

### Caso S02
| Campo | Información |
| --- | --- |
| Endpoint | `POST /students` |
| Datos enviados | `{"name":"Ana Pérez","email":"ana@universidad.edu","semester":4}` |
| Resultado esperado | Estudiante creado; active=true |
| Código HTTP esperado | 201 |
| Resultado obtenido | Estudiante creado con `id: 1`, `name: "Ana Pérez"`, `email: "ana@universidad.edu"`, `semester: 4`. Al omitir `active`, quedó en `true` por defecto. |
| Código HTTP obtenido | 201 |
| Estado | Aprobado |
| Evidencia | `evidencias/S02.png` |

### Caso S03
| Campo | Información |
| --- | --- |
| Endpoint | `POST /students` |
| Datos enviados | `{"name":"Luis Gómez","email":"luis@universidad.edu","semester":2,"active":false}` |
| Resultado esperado | Estudiante creado; active=false |
| Código HTTP esperado | 201 |
| Resultado obtenido | Estudiante creado con `id: 2`, `name: "Luis Gómez"`, `email: "luis@universidad.edu"`, `semester: 2` y `active: false`. |
| Código HTTP obtenido | 201 |
| Estado | Aprobado |
| Evidencia | `evidencias/S03.png` |

### Caso S04
| Campo | Información |
| --- | --- |
| Endpoint | `GET /students` |
| Datos enviados | `—` |
| Resultado esperado | Lista de estudiantes |
| Código HTTP esperado | 200 |
| Resultado obtenido | Lista con los 2 estudiantes creados: id 1 (Ana Pérez, `active: true`) e id 2 (Luis Gómez, `active: false`). |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/S04.png` |

### Caso S05
| Campo | Información |
| --- | --- |
| Endpoint | `GET /students/1` |
| Datos enviados | `—` |
| Resultado esperado | Estudiante con id 1 |
| Código HTTP esperado | 200 |
| Resultado obtenido | Devolvió el estudiante con `id: 1`, `name: "Ana Pérez"`, `email: "ana@universidad.edu"`, `semester: 4`, `active: true`. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/S05.png` |

### Caso S06
| Campo | Información |
| --- | --- |
| Endpoint | `GET /students/999` |
| Datos enviados | `—` |
| Resultado esperado | {"detail":"Student not found"} |
| Código HTTP esperado | 404 |
| Resultado obtenido | Al consultar el ID inexistente 999, la API respondió `{"detail": "Student not found"}`. |
| Código HTTP obtenido | 404 |
| Estado | Aprobado |
| Evidencia | `evidencias/S06.png` |

### Caso S07
| Campo | Información |
| --- | --- |
| Endpoint | `GET /students/abc` |
| Datos enviados | `—` |
| Resultado esperado | Error de validación |
| Código HTTP esperado | 422 |
| Resultado obtenido | El servidor rechazó el ID `abc` con error de validación: tipo `int_parsing`, "Input should be a valid integer" (campo `path.student_id`). Se ejecutó con `curl.exe` porque Swagger UI bloquea el valor en el cliente y no envía la petición. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/S07.png` |

### Caso S08
| Campo | Información |
| --- | --- |
| Endpoint | `POST /students` |
| Datos enviados | `{"name":"Ana Pérez","email":"ana@universidad.edu","semester":0}` |
| Resultado esperado | Error de validación |
| Código HTTP esperado | 422 |
| Resultado obtenido | La API rechazó `semester: 0` con error de validación: tipo `greater_than_equal`, "Input should be greater than or equal to 1". No se creó ningún estudiante. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/S08.png` |

### Caso S09
| Campo | Información |
| --- | --- |
| Endpoint | `POST /students` |
| Datos enviados | `{"name":"Ana Pérez","email":"ana@universidad.edu","semester":11}` |
| Resultado esperado | Error de validación |
| Código HTTP esperado | 422 |
| Resultado obtenido | La API rechazó `semester: 11` con error de validación: tipo `less_than_equal`, "Input should be less than or equal to 10". No se creó ningún estudiante. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/S09.png` |

### Caso S10
| Campo | Información |
| --- | --- |
| Endpoint | `POST /students` |
| Datos enviados | `{"name":"An","email":"ana@universidad.edu","semester":4}` |
| Resultado esperado | Error de validación (nombre corto) |
| Código HTTP esperado | 422 |
| Resultado obtenido | La API rechazó el nombre "An" con error de validación: tipo `string_too_short`, "String should have at least 3 characters". No se creó ningún estudiante. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/S10.png` |

### Caso S11
| Campo | Información |
| --- | --- |
| Endpoint | `POST /students` |
| Datos enviados | `{"name":"Ana Pérez","email":"","semester":4}` |
| Resultado esperado | Error de validación (email vacío) |
| Código HTTP esperado | 422 |
| Resultado obtenido | La API rechazó el email vacío con error de validación: tipo `string_too_short`, "String should have at least 1 character" (campo `body.email`). No se creó ningún estudiante. |
| Código HTTP obtenido | 422 |
| Estado | Aprobado |
| Evidencia | `evidencias/S11.png` |


## Persistencia

### Caso R01
| Campo | Información |
| --- | --- |
| Endpoint | `GET /students (tras reiniciar Uvicorn)` |
| Datos enviados | `—` |
| Resultado esperado | Los estudiantes siguen almacenados |
| Código HTTP esperado | 200 |
| Resultado obtenido | Tras reiniciar Uvicorn, la lista conserva los 2 estudiantes: id 1 (Ana Pérez) e id 2 (Luis Gómez), con los mismos datos. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/R01.png` |

### Caso R02
| Campo | Información |
| --- | --- |
| Endpoint | `GET /courses (tras reiniciar Uvicorn)` |
| Datos enviados | `—` |
| Resultado esperado | Los cursos siguen funcionando |
| Código HTTP esperado | 200 |
| Resultado obtenido | Tras reiniciar Uvicorn, la lista de cursos funciona y devuelve el curso 1 (`name: "Programación II"`, `credits: 4`, `active: false`) con los cambios del PUT conservados. |
| Código HTTP obtenido | 200 |
| Estado | Aprobado |
| Evidencia | `evidencias/R02.png` |