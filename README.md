# 🔍 GPT Image Recognition - Contador de Latas y Botellas

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20Vision-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Reconocimiento de Latas y Botellas con GPT Vision / Can and Bottle Recognition with GPT Vision**

## 🚀 Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/rafaelhernandezrios/gpt-inventory-detection.git
cd gpt-inventory-detection

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API Key
cp env_example.txt .env
# Edita .env y agrega tu API Key de OpenAI

# 4. Ejecutar la aplicación
python app.py
```

**🌐 Abre:** http://localhost:5000

## 📑 Tabla de Contenido / Table of Contents

- [🚀 Quick Start](#-quick-start)
- [📋 Descripción](#-descripción--description)
- [🚀 Características](#-características--features)
- [🛠️ Instalación](#️-instalación--installation)
- [📖 Uso](#-uso--usage)
- [🌐 Acceso desde otros dispositivos](#-acceso-desde-otros-dispositivos--access-from-other-devices)
- [📷 Opciones para Acceso a Cámara](#-opciones-para-acceso-a-cámara--camera-access-options)
- [🏗️ Estructura del Proyecto](#️-estructura-del-proyecto--project-structure)
- [🔧 Configuración Avanzada](#-configuración-avanzada--advanced-configuration)
- [🔒 Seguridad](#-seguridad--security)
- [🐛 Solución de Problemas](#-solución-de-problemas--troubleshooting)
- [📱 Compatibilidad](#-compatibilidad--compatibility)
- [🤝 Contribuir](#-contribuir--contributing)
- [📄 Licencia](#-licencia--license)

## 📋 Descripción / Description

Esta aplicación web utiliza Flask y la API de GPT Vision para reconocer y contar latas y botellas en imágenes tomadas con la cámara del dispositivo.

This web application uses Flask and the GPT Vision API to recognize and count cans and bottles in images taken with the device's camera.

## 🚀 Características / Features

- 📷 **Captura de fotos en tiempo real** / Real-time photo capture
- 🤖 **Análisis con IA usando GPT Vision** / AI analysis using GPT Vision
- 📊 **Conteo automático de latas y botellas** / Automatic counting of cans and bottles
- 🎨 **Interfaz moderna y responsiva** / Modern and responsive interface
- 📱 **Compatible con dispositivos móviles** / Mobile device compatible

## 🛠️ Instalación / Installation

### 1. Clonar el repositorio / Clone the repository
```bash
git clone <repository-url>
cd gptimagerecognition
```

### 2. Crear entorno virtual / Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias / Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key / Configure API Key

**Crea un archivo `.env` en la raíz del proyecto:**
**Create a `.env` file in the project root:**

```bash
# Copia el archivo de ejemplo
cp env_example.txt .env
```

**O crea manualmente el archivo `.env` con este contenido:**
**Or manually create the `.env` file with this content:**

```env
# OpenAI API Configuration
OPENAI_API_KEY=tu-api-key-de-openai-aqui

# Flask Configuration (opcional/optional)
FLASK_ENV=development
FLASK_DEBUG=1
```

**Para obtener tu API Key de OpenAI:**
**To get your OpenAI API Key:**

1. Ve a [OpenAI Platform](https://platform.openai.com/)
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys" en el menú
4. Crea una nueva API Key
5. Copia la clave y pégala en el archivo `.env`

**⚠️ IMPORTANTE / IMPORTANT:**
- Nunca subas tu archivo `.env` a GitHub
- Never upload your `.env` file to GitHub
- El archivo `.env` ya está incluido en `.gitignore`
- The `.env` file is already included in `.gitignore`

### 5. Ejecutar la aplicación / Run the application

**Opción 1: HTTP (Básico) / HTTP (Basic)**
```bash
python app.py
```

**Opción 2: HTTPS (Recomendado para cámara) / HTTPS (Recommended for camera)**
```bash
python app_https.py
```

**Opción 3: Con verificaciones / With checks**
```bash
python run.py
```

**URLs disponibles / Available URLs:**
- **Aplicación principal / Main app:** `http://localhost:5000` o `https://localhost:5000`
- **Test de compatibilidad / Compatibility test:** `http://localhost:5000/test`
- **Versión con subida de archivos / File upload version:** `http://localhost:5000/upload`

## 🌐 **Acceso desde otros dispositivos / Access from other devices**

### **Para acceder desde tu celular u otros dispositivos / To access from your phone or other devices:**

1. **Ejecuta la versión HTTPS / Run the HTTPS version:**
```bash
python app_https.py
```

2. **Encuentra la IP de tu PC / Find your PC's IP:**
   - Windows: `ipconfig` en CMD
   - Mac/Linux: `ifconfig` o `ip addr` en terminal

3. **En tu celular, abre el navegador y ve a:**
```
https://[IP-DE-TU-PC]:5000
```

**Ejemplo / Example:**
```
https://192.168.1.100:5000
```

### **⚠️ Requisitos / Requirements:**
- ✅ Ambos dispositivos en la misma red WiFi
- ✅ Both devices on the same WiFi network
- ✅ Aceptar el certificado autofirmado en el navegador
- ✅ Accept the self-signed certificate in the browser



## 📖 Uso / Usage

1. **Abrir la aplicación** / Open the application
   - Navega a `http://localhost:5000` en tu navegador
   - Navigate to `http://localhost:5000` in your browser

2. **Iniciar la cámara** / Start the camera
   - Haz clic en "📷 Iniciar Cámara"
   - Click on "📷 Iniciar Cámara"

3. **Tomar una foto** / Take a photo
   - Haz clic en "📸 Tomar Foto"
   - Click on "📸 Tomar Foto"

4. **Ver resultados** / View results
   - La aplicación analizará la imagen automáticamente
   - The application will analyze the image automatically
   - Verás el conteo de latas y botellas
   - You'll see the count of cans and bottles

## 🏗️ Estructura del Proyecto / Project Structure

```
gptimagerecognition/
├── app.py                 # Servidor Flask principal / Main Flask server
├── app_https.py           # Servidor Flask con HTTPS / Flask server with HTTPS
├── run.py                 # Script de inicio con verificaciones / Startup script with checks
├── config.py              # Configuración centralizada / Centralized configuration
├── templates/
│   ├── index.html        # Interfaz principal / Main interface
│   ├── test_camera.html  # Test de compatibilidad / Compatibility test
│   └── upload_version.html # Versión con subida de archivos / File upload version
├── requirements.txt      # Dependencias de Python / Python dependencies
├── env_example.txt       # Ejemplo de variables de entorno / Environment variables example
├── .gitignore           # Archivos a ignorar en Git / Files to ignore in Git
├── README.md            # Documentación / Documentation
└── .env                 # Variables de entorno (crear) / Environment variables (create)
```

## 🔧 Configuración Avanzada / Advanced Configuration

### Variables de Entorno / Environment Variables

```env
OPENAI_API_KEY=tu-api-key-de-openai
FLASK_ENV=development
FLASK_DEBUG=1
```

## 🔒 Seguridad / Security

### **Archivos Sensibles / Sensitive Files**
- ✅ `.env` - Incluido en `.gitignore` (no se sube a GitHub)
- ✅ `cert.pem` y `key.pem` - Certificados SSL autofirmados (no se suben)
- ✅ `uploads/` - Directorio de archivos subidos (no se sube)

### **API Key de OpenAI / OpenAI API Key**
- 🔐 **Nunca compartas tu API Key públicamente**
- 🔐 **Never share your API Key publicly**
- 💰 **La API Key tiene costos asociados**
- 💰 **The API Key has associated costs**
- 📧 **Si tu API Key se compromete, revócala inmediatamente**
- 📧 **If your API Key is compromised, revoke it immediately**

### Personalización del Modelo / Model Customization

Puedes modificar el prompt en `app.py` para cambiar el comportamiento del análisis:
You can modify the prompt in `app.py` to change the analysis behavior:

```python
"text": "Analiza esta imagen y cuenta específicamente cuántas latas y cuántas botellas hay..."
```

## 🐛 Solución de Problemas / Troubleshooting

### Error de Cámara / Camera Error

**Error común:** `Cannot read properties of undefined (reading 'getUserMedia')`

**🇪🇸 Soluciones:**
1. **Verificar navegador:** Usa Chrome 60+, Firefox 55+, Safari 11+, Edge 79+
2. **Permisos:** Asegúrate de permitir acceso a la cámara cuando el navegador lo solicite
3. **HTTPS:** En producción, la cámara requiere HTTPS (localhost funciona en desarrollo)
4. **Test de compatibilidad:** Visita `/test` para verificar la compatibilidad de tu navegador
5. **Cámara en uso:** Cierra otras aplicaciones que puedan estar usando la cámara

**🇺🇸 Solutions:**
1. **Check browser:** Use Chrome 60+, Firefox 55+, Safari 11+, Edge 79+
2. **Permissions:** Make sure to allow camera access when the browser requests it
3. **HTTPS:** In production, camera requires HTTPS (localhost works in development)
4. **Compatibility test:** Visit `/test` to check your browser compatibility
5. **Camera in use:** Close other applications that might be using the camera

**🔧 Test de Compatibilidad / Compatibility Test:**
```bash
# Ejecuta la aplicación y visita:
# Run the application and visit:
http://localhost:5000/test
```

## 📷 **Opciones para Acceso a Cámara / Camera Access Options**

### **1. 🌐 Localhost HTTP (Básico)**
- **Comando:** `python app.py`
- **URL:** `http://localhost:5000`
- **✅ Pros:** Simple, rápido, funciona en todos los navegadores
- **❌ Contras:** Cámara puede no funcionar en algunos navegadores móviles

### **2. 🔒 Localhost HTTPS (Recomendado)**
- **Comando:** `python app_https.py`
- **URL:** `https://localhost:5000`
- **✅ Pros:** Cámara funciona en todos los navegadores, más seguro
- **❌ Contras:** Requiere aceptar certificado autofirmado

### **3. 📁 Versión con Subida de Archivos**
- **URL:** `http://localhost:5000/upload`
- **✅ Pros:** No requiere cámara ni HTTPS, funciona en cualquier navegador
- **❌ Contras:** No puede tomar fotos en tiempo real

### Error de API / API Error
- Verifica que tu API Key sea válida
- Verify that your API Key is valid
- Asegúrate de tener créditos en tu cuenta de OpenAI
- Make sure you have credits in your OpenAI account

### Error de Dependencias / Dependencies Error
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📱 Compatibilidad / Compatibility

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 11+
- ✅ Edge 79+
- ✅ Dispositivos móviles / Mobile devices

## 🤝 Contribuir / Contributing

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia / License

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
This project is under the MIT License. See the `LICENSE` file for more details.

## 🙏 Agradecimientos / Acknowledgments

- OpenAI por la API de GPT Vision
- OpenAI for the GPT Vision API
- Flask por el framework web
- Flask for the web framework
- La comunidad de desarrolladores
- The developer community

---

**¡Disfruta usando la aplicación! / Enjoy using the application!** 🎉
