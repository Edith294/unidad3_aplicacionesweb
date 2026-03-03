# 🚀 API REST Profesional con Testing Avanzado
## Flask · SQLAlchemy · JWT · Pytest · PostgreSQL

> Proyecto académico desarrollado bajo principios de ingeniería de software moderna.  
> Enfoque en arquitectura modular, testing automatizado y buenas prácticas backend.

---

# 📌 Descripción General

Este proyecto consiste en el desarrollo de una **API REST profesional** construida con Flask, implementando:

- Arquitectura modular escalable
- App Factory Pattern
- Separación por capas (configuración, modelos, rutas)
- Autenticación segura con JWT
- Control de acceso basado en roles (RBAC)
- Pruebas unitarias, integración y End-to-End
- Cobertura de código superior al 80%
- Base de datos desacoplada para testing

El sistema simula:

- 🎓 Plataforma académica (estudiantes, materias, calificaciones)
- 🛒 Flujo completo de tienda (TechStore API)

---

# 📸 Capturas del Proyecto

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/4e6c6199-4f15-440f-9dab-4908e32ce739" />
<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/8fe16759-03a0-4991-b641-ffc0fe949027" />
<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/92e5eca6-4f48-43a6-8cb6-0fe2932a4c00" />
<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/6ac0319a-352f-43e1-acc5-4450486b632f" />

---
### 🖥️ Ejecución de pruebas
<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/fb24feda-307a-440c-b587-c7889fc40797" />
<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/c5ad5845-eaac-401c-8e28-cb3562c78d7e" />
<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/d9642151-2b87-4c47-8f15-03daef2156df" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/805ae24a-09eb-47df-aec8-ba7e57329874" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/61207197-a048-440d-8fa8-1c192081e162" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/84a62c0f-52ce-4233-9a61-e435ebfddd36" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/cedf3a5a-048d-4ece-aab5-d32e9f91cfbc" />


### 📊 Reporte de cobertura
<img width="682" height="1013" alt="image" src="https://github.com/user-attachments/assets/bb98e468-fca3-4392-8c99-4fff6eb6d94e" />
---

# 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura modular basada en:

- App Factory Pattern
- Configuración desacoplada
- Modelos organizados
- Rutas estructuradas por módulos
- Testing aislado con base de datos en memoria

---

# 📂 Estructura del Proyecto

mi_api_v2/
│
├── app/
│ ├── models/
│ ├── routes/
│ ├── config.py
│ ├── extensions.py
│ └── init.py
│
├── tests/
│ ├── conftest.py
│ ├── test_models.py
│ ├── test_auth.py
│ ├── test_routes.py
│ └── test_e2e.py
│
├── venv/
├── requirements.txt
├── run.py
├── .env
├── .gitignore
└── README.md



---

# 🛠 Tecnologías Utilizadas

- Python 3.11+
- Flask
- SQLAlchemy
- PostgreSQL (producción)
- SQLite en memoria (testing)
- Flask-JWT-Extended
- Pytest
- pytest-cov
- Factory Boy
- Faker

---

# ⚙️ Instalación y Configuración

## 1️⃣ Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/mi_api_v2.git
cd mi_api_v2
---

# ⚙️ Instalación y Configuración

## 🐍 Crear Entorno Virtual

```bash
python -m venv venv
```

### ▶️ Activar entorno virtual

```bash
venv\Scripts\activate
```

---

## 📦 Instalar Dependencias

```bash
pip install -r requirements.txt
```

---

# 🔐 Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
FLASK_ENV=development
SECRET_KEY=super_secret_key
JWT_SECRET_KEY=jwt_secret_key
DATABASE_URL=postgresql://usuario:password@localhost/mi_base
```

📌 Durante las pruebas se utiliza automáticamente SQLite en memoria.

---

# 🗄️ Base de Datos

## 🏭 Producción

- PostgreSQL  
- Configurable mediante la variable `DATABASE_URL`

## 🧪 Testing

- SQLite en memoria  
- Base creada y eliminada en cada prueba  
- Aislamiento total entre tests  

### ✔️ Beneficios

- Pruebas rápidas  
- Entorno reproducible  
- No afecta datos reales  

---

# ▶️ Ejecutar la Aplicación

```bash
flask run
```

O alternativamente:

```bash
python run.py
```

Servidor por defecto:

```
http://127.0.0.1:5000
```

---

# 🧪 Ejecutar Pruebas

## ▶️ Ejecutar todas las pruebas

```bash
pytest
```

## 📊 Ejecutar con cobertura

```bash
pytest --cov=app --cov-report=term-missing
```

## 📄 Generar reporte HTML

```bash
pytest --cov=app --cov-report=html
```

Abrir:

```
htmlcov/index.html
```

---

# 🧪 Tipos de Pruebas Implementadas

## 1️⃣ Pruebas Unitarias

- Métodos de modelos  
- Validaciones  
- Serialización de datos  
- Hashing de contraseñas  

## 2️⃣ Pruebas de Integración

- CRUD completo  
- Respuestas HTTP correctas  
- Manejo de errores (400, 404, 409)  

## 3️⃣ Pruebas de Autenticación

- Registro de usuario  
- Login  
- Tokens JWT válidos e inválidos  
- Protección de rutas  

## 4️⃣ Pruebas de Relaciones

- Registro de calificaciones  
- Cálculo de promedio  
- Kardex académico  

## 5️⃣ Pruebas End-to-End (E2E)

Flujo completo del sistema:

```
Admin crea productos
→ Cliente se registra
→ Cliente inicia sesión
→ Cliente realiza compra
→ Se descuenta stock
→ Admin consulta reporte
```

---

# 🔐 Seguridad Implementada

- Autenticación basada en JWT  
- Control de roles (admin / usuario)  
- Protección de endpoints sensibles  
- Validación de datos de entrada  
- Manejo seguro de contraseñas (hashing)  

---

# 📊 Resultados

- Más de 30 pruebas automatizadas  
- Cobertura superior al 90%  
- Arquitectura escalable  
- Código modular y mantenible  
- Flujo empresarial completo simulado  

---

# 📈 Buenas Prácticas Aplicadas

- App Factory Pattern  
- Separación de configuraciones  
- Base de datos desacoplada  
- Testing aislado  
- Uso de fixtures en pytest  
- Factory Boy para generación de datos  
- Faker para datos realistas  
- Control de versiones con Git  
- Uso correcto de `.gitignore`  

---

# 🚀 Posibles Mejoras Futuras

- Dockerización del proyecto  
- Integración continua (CI/CD)  
- Documentación Swagger / OpenAPI  
- Logging estructurado  
- Rate limiting  
- Deploy en la nube (Render / Railway / AWS)  

---

# 🎯 Objetivo Académico

Aplicar principios de:

- Testing automatizado  
- Diseño de APIs REST  
- Seguridad backend  
- Arquitectura profesional  
- Buenas prácticas en Python  

---

# 👩‍💻 Autor

**Bodoque**  
Proyecto Académico – 2026  
Aplicaciones Web Orientadas a Servicios- Desarrollado por Brenda- Derechos Reservados®
