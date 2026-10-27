### Gestión de Suscripciones API

Este proyecto es una API asincrónica de nivel de producción desarrollada con **FastAPI**, **Pydantic** y **SQLAlchemy 2.0**. Está diseñada siguiendo una arquitectura modular orientada al dominio, garantizando la escalabilidad, la separación limpia de responsabilidades y un rendimiento optimizado mediante el manejo de E/S no bloqueante. 

###  Tecnologías y Librerías Utilizadas

El entorno y las dependencias de este proyecto están gestionados de forma eficiente con uv. A continuación, se detalla el rol fundamental de cada librería instalada: 

* **fastapi**: El framework web principal. Es asincrónico por naturaleza, extremadamente rápido (gracias a Starlette y Uvicorn) y genera automáticamente la documentación interactiva OpenAPI/Swagger basándose en el tipado de Python.
* **uvicorn**: El servidor ASGI (Asynchronous Server Gateway Interface) encargado de ejecutar la aplicación FastAPI y manejar las conexiones HTTP concurrentes de forma ultra rápida.
* **pydantic (junto a pydantic[email])**: La librería encargada de la validación de datos y gestión de configuraciones. Mapea y valida las peticiones entrantes (JSON a objetos de Python) y las salidas de la API. El complemento email añade soporte nativo para validar tipos de datos complejos como EmailStr.
* **pydantic-settings**: Extensión de Pydantic utilizada para gestionar de forma segura las variables de entorno (.env) garantizando que las credenciales o URLs de la base de datos se validen correctamente al arrancar el servidor.
* **sqlalchemy**: El ORM (Object-Relational Mapping) estándar de la industria en Python. En este proyecto se utiliza exclusivamente su especificación **SQLAlchemy 2.0** de forma asincrónica (asyncio), permitiendo mapear clases de Python a tablas de bases de datos relacionales sin bloquear el hilo de ejecución principal.
* **aiosqlite**: El driver asincrónico para SQLite. SQLAlchemy no puede comunicarse directamente con una base de datos sin un driver; aiosqlite permite realizar operaciones de lectura y escritura en el archivo .db usando async/await.
* **greenlet**: Una dependencia interna requerida por SQLAlchemy para poder ejecutar la abstracción asincrónica sobre ciertos componentes del motor del ORM que tradicionalmente eran sincrónicos.

### Arquitectura y Estructura del Código

El proyecto abandona las estructuras planas para simular un desarrollo empresarial real, dividiendo el código según su responsabilidad: 


```text
src/
├── core/               # Infraestructura técnica global independiente del negocio
│   ├── database.py     # Configuración del motor asincrónico de SQLAlchemy y sesión inyectable
│   └── excepciones.py  # Errores personalizados del negocio y middleware de captura global
├── modelos/            # Definición de las tablas de la base de datos relacional (Modelos ORM)
│   └── suscripcion.py  # Entidad 'Suscripcion' mapeada con tipado estricto (Mapped/mapped_column)
├── schemas/            # Contratos de validación de datos para entrada y salida de datos
│   └── suscripcion.py  # Esquemas Pydantic que validan reglas del negocio (precios, formatos de email)
├── api/                # Capa de transporte y controladores HTTP
│   └── v1/
│       ├── router.py   # Enrutador central que unifica todos los módulos de la versión 1
│       └── endpoints/
│           └── suscripciones.py # Controladores asincrónicos exclusivos de la lógica de suscripciones
└── main.py             # Punto de entrada de la aplicación. Configura lifespan, middlewares y rutas generales
```


###  Explicación del Flujo del Código

### 1. Inicialización y Ciclo de Vida (src/main.py)

Utiliza un administrador de contexto asincrónico (lifespan). Al iniciar el servidor, dispara el evento init_db() para verificar y crear automáticamente las tablas en el archivo SQLite si no existen. Además, inyecta un manejador global que intercepta cualquier error de tipo CustomAppException para transformarlo en una respuesta JSON estandarizada. 

### 2. Sesiones de Base de Datos Eficientes (src/core/database.py)

En lugar de abrir y cerrar conexiones manualmente, define una función generadora asincrónica get_db(). Esta se utiliza como una dependencia inyectable (Depends(get_db)) en los endpoints de FastAPI. Garantiza que cada petición HTTP reciba su propia sesión de base de datos aislada y que esta se cierre de forma segura al finalizar la petición, evitando fugas de memoria. 

### 3. Operaciones Asincrónicas Completas (src/api/v1/endpoints/suscripciones.py)

Tanto la creación como la obtención de registros ejecutan consultas SQL mediante sentencias asincrónicas: 

* Al crear, se usa db.add() seguido de await db.commit() para delegar la persistencia de forma no bloqueante.
* Al buscar, se ejecuta de manera explícita await db.execute(select(...)) asegurando que el servidor pueda procesar otras peticiones concurrentes mientras espera la respuesta del disco.

###  Instrucciones de Ejecución

Para iniciar el servidor de desarrollo con recarga automática, ejecuta el siguiente comando en la raíz del proyecto: 

```bash
uv run uvicorn src.fastapi_practice.main:app --reload
```

Una vez levantado, puedes acceder a la documentación interactiva en: 

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

##  Despliegue con Docker

Este proyecto está completamente contenedorizado utilizando compilaciones multi-etapa optimizadas con `uv`. Para levantar la API de forma aislada en cualquier entorno, asegúrate de tener Docker instalado y ejecuta:

```bash
# Clonar el proyecto y entrar al directorio
cd fastapi-practice

# Construir y levantar el contenedor en segundo plano
docker compose up --build -d
```

La documentación interactiva estará disponible automáticamente en:
* [http://localhost:8000/docs](http://localhost:8000/docs)