# BookMedik API

API REST desarrollada con Django REST Framework.

## Tecnologías

- Python
- Django
- Django REST Framework
- JWT
- MySQL

## Instalación

1. Clonar repositorio
2. Crear entorno virtual
3. Instalar requirements.txt
6. Ejecutar migraciones
7. Crear superusuario
8. Ejecutar servidor

## Endpoints en Postman para probar JWT

POST /api/auth/login/
POST /api/auth/refresh/

GET /api/pacients/
GET /api/medics/
GET /api/reservations/
...

## Módulo Farmacia

`farmacia` es una app Django independiente dentro del monolito. Permite administrar un
inventario simple de medicamentos con nombre único, descripción, existencias y precio.
No permite existencias ni precios negativos. Usa el mismo JWT y la misma clase `IsAdmin`
del proyecto: cualquier usuario autenticado puede consultar; solo administradores pueden
crear, actualizar o eliminar.

### Iniciar y probar

Desde la raíz del proyecto, con el entorno virtual activo:

```powershell
python manage.py migrate
python manage.py test farmacia
python manage.py runserver
```

En este equipo también quedó disponible `.venv\Scripts\python.exe` para ejecutar esos
comandos si el entorno `venv` anterior no inicia.

Importar [la colección de Postman](postman/Farmacia.postman_collection.json), establecer
la variable `password` con la contraseña del superusuario y ejecutar las peticiones en
orden. La colección incluye los JSON de cada petición y scripts de prueba que guardan
`farmacia_access_token`, `farmacia_refresh_token` y `farmacia_medicamento_id`
automáticamente. El valor inicial de
`farmacia_base_url` es `http://127.0.0.1:8000` y `username` es `gio`.
Las variables propias del módulo evitan conflictos con un entorno Postman llamado
`Local` que ya tenga `base_url` o tokens definidos.

| Método | Ruta | Uso | Estado esperado |
| --- | --- | --- | --- |
| POST | `/api/auth/login/` | Obtener JWT | 200 |
| POST | `/api/auth/refresh/` | Renovar JWT | 200 |
| GET | `/api/farmacia/medicamentos/` | Listar | 200 |
| GET | `/api/farmacia/medicamentos/?name=para` | Buscar por nombre | 200 |
| POST | `/api/farmacia/medicamentos/` | Crear | 201 |
| GET | `/api/farmacia/medicamentos/{id}/` | Consultar | 200 |
| PUT | `/api/farmacia/medicamentos/{id}/` | Reemplazar | 200 |
| PATCH | `/api/farmacia/medicamentos/{id}/` | Actualizar un campo | 200 |
| DELETE | `/api/farmacia/medicamentos/{id}/` | Eliminar | 204 |

Para las rutas de medicamentos, enviar `Authorization: Bearer <access_token>`. La
colección configura esta cabecera. El cuerpo JSON para crear es:

```json
{
  "name": "Paracetamol 500 mg",
  "description": "Caja de 20 tabletas",
  "stock": 30,
  "price": "12.50"
}
```

`PUT` requiere el mismo cuerpo completo; `PATCH` admite solo los campos a modificar,
por ejemplo `{"stock": 20}`. `GET` y `DELETE` no llevan cuerpo. Un nombre duplicado,
precio negativo o existencias negativas devuelve 400. La petición de validación en la
colección comprueba este último caso. Si se ejecuta la colección de nuevo tras dejar
un medicamento creado, usar otro nombre o eliminar el registro anterior.
