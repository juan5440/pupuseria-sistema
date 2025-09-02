# pupuseria-sistema

# 🍽️ Sistema de Ventas para Pupusería

[![PHP](https://img.shields.io/badge/PHP-8.2-blue?logo=php)](https://www.php.net/)  
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-blue?logo=mysql)](https://www.mysql.com/)  
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)](https://getbootstrap.com/)  
[![jQuery](https://img.shields.io/badge/jQuery-3.x-0769AD?logo=jquery)](https://jquery.com/)  
[![DataTables](https://img.shields.io/badge/DataTables-Plugin-green)](https://datatables.net/)  
[![SweetAlert](https://img.shields.io/badge/SweetAlert-Alerts-orange)](https://sweetalert.js.org/)  
[![License](https://img.shields.io/badge/Licencia-Libre-success)](LICENSE)  

Un sistema desarrollado en **PHP 8.2, MySQL, Bootstrap 5, AJAX y JavaScript** para la gestión de ventas en una pupusería.  
Permite administrar productos (pupusas, panes con pollo, bebidas, etc.), registrar ventas con cálculo de cambio, generar reportes y exportar información a Excel/PDF.

---

## 📖 Características principales
- **Gestión de Productos**
  - CRUD: Agregar, editar y eliminar productos.
  - Listado dinámico con DataTables.

- **Gestión de Ventas**
  - Registro de ventas con cálculo automático de cambio.
  - Edición y eliminación de ventas.
  - Detalle de ventas individuales.

- **Reportes**
  - Reporte de ventas de pupusas.
  - Reporte de ventas de bebidas.
  - Exportación a PDF o Excel.

- **Alertas Interactivas**
  - Confirmaciones y mensajes con **SweetAlert**.

---

## 📂 Estructura del Proyecto
pupuseria-sistema/
│── assets/ # Archivos estáticos (CSS, JS, imágenes)
│── backend/ # Lógica PHP (CRUD productos y ventas)
│── database/ # Script SQL para crear la base de datos
│── index.html # Página principal
│── menu.html # Menú de navegación

yaml
Copiar código

---

## 🛠️ Requisitos Técnicos
- **Servidor web**: Apache o Nginx con PHP 8.2+  
- **Base de datos**: MySQL 5.7+  
- **Extensiones PHP**: `mysqli`  
- **Frontend**: Bootstrap 5, jQuery, DataTables, SweetAlert  

---

## ⚙️ Instalación
1. Clona este repositorio o descárgalo en tu servidor local:
   ```bash
   git clone https://github.com/tuusuario/pupuseria-sistema.git
Importa la base de datos:

sql
Copiar código
database/creacion_db.sql
Configura la conexión en:

bash
Copiar código
backend/conexion.php
Ajusta usuario, contraseña y nombre de la base de datos.

Inicia tu servidor (XAMPP, Laragon, etc.) y coloca la carpeta en htdocs o www.

Accede en tu navegador:

arduino
Copiar código
http://localhost/pupuseria-sistema/index.html
🚀 Uso del Sistema
Accede a la página principal → index.html.

Navega con el menú → menu.html.

Productos → CRUD (crear, editar, eliminar, listar).

Ventas → Registrar ventas, calcular cambio, editar o eliminar.

Reportes → Filtrar por tipo de producto y exportar datos.

📊 Casos de Uso
Pupuserías y comedores que necesitan un control ágil de ventas.

Negocios pequeños que requieren facturación rápida y sencilla.

Control de inventario básico de alimentos y bebidas.

👨‍💻 Tecnologías utilizadas
Backend: PHP 8.2, MySQL

Frontend: HTML5, Bootstrap 5, jQuery, AJAX


Extras: DataTables, SweetAlert

📜 Licencia
Este proyecto es de uso libre para fines educativos y comerciales.
Si lo mejoras, ¡comparte tus aportes! 🤝

Imagenes:
<img width="1325" height="807" alt="Captura de pantalla 2025-09-02 114057" src="https://github.com/user-attachments/assets/8888bbda-20ef-4bb2-b250-38f13e280b4d" />
<img width="1322" height="730" alt="Captura de pantalla 2025-09-02 114127" src="https://github.com/user-attachments/assets/f8ddd7d9-5591-4cb7-a7c6-793c8467d32e" />
<img width="1355" height="901" alt="Captura de pantalla 2025-09-02 114018" src="https://github.com/user-attachments/assets/a7e163e4-5bab-417e-9b39-54b48a80e2d0" />


