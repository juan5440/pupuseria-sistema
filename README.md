# Sistema de Ventas - Pupusería "El Sabor de Casa"

Un sistema de punto de venta (POS) moderno y eficiente diseñado específicamente para pupuserías, desarrollado en Python con una interfaz gráfica intuitiva.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)

## 📋 Características

- **Punto de Venta (POS)**:
  - Interfaz visual para selección rápida de productos.
  - Cálculo automático de totales y cambio.
  - Generación de tickets de venta.
  - **Impresión de Tickets**: Integración con la impresora predeterminada del sistema.
  
- **Gestión de Menú**:
  - Agregar, editar y eliminar productos fácilmente.
  - Actualización de precios en tiempo real.

- **Historial de Ventas**:
  - Registro detallado de todas las transacciones.
  - Visualización de detalles por venta.
  - Almacenamiento con zona horaria de Centroamérica (UTC-6).

- **Diseño Moderno**:
  - Modo Oscuro / Claro.
  - Interfaz limpia y responsiva.

## 🚀 Instalación y Uso

### Requisitos previos
- Python 3.x instalado en su sistema.

### Pasos para ejecutar

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/juan5440/pupuseria-sistema.git
   cd pupuseria-sistema
   ```

2. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```
   *(O `py main.py` dependiendo de su configuración de Python en Windows)*

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3
- **Interfaz Gráfica**: Tkinter (Biblioteca estándar)
- **Base de Datos**: SQLite3
- **Control de Versiones**: Git

## 📂 Estructura del Proyecto

```
sispupuseria/
├── main.py              # Punto de entrada de la aplicación
├── database.py          # Lógica de base de datos y modelos
├── ui/                  # Componentes de la interfaz gráfica
│   ├── pos_frame.py     # Módulo de ventas
│   ├── menu_frame.py    # Gestión de productos
│   ├── history_frame.py # Historial de ventas
│   └── styles.py        # Configuración de estilos y temas
└── pupuseria.db         # Archivo de base de datos (se crea automáticamente)
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Siéntase libre de usarlo y modificarlo.

---
Desarrollado con ❤️ para la comunidad de pupuserías.
