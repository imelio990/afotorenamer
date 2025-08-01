# 📦 AfoToRelocate - Ejecutables Distribuibles

## 🚀 Versiones disponibles

### 1. AfoToRelocate.exe ⭐ (Recomendado)
- **Descripción**: Versión estándar optimizada
- **Interfaz**: Sin ventana de consola (limpia)
- **Compatibilidad**: Windows 7+ (64-bit)
- **Tamaño**: ~18 MB
- **Uso**: Para la mayoría de usuarios

### 2. AfoToRelocate_Compatible.exe 🔧
- **Descripción**: Máxima compatibilidad
- **Interfaz**: Sin ventana de consola
- **Compatibilidad**: Windows Vista+ (32/64-bit)
- **Características**: Sin compresión UPX, imports explícitos
- **Uso**: Si la versión estándar no funciona

### 3. AfoToRelocate_Debug.exe 🔍
- **Descripción**: Versión de diagnóstico
- **Interfaz**: Con ventana de consola
- **Compatibilidad**: Windows Vista+ (32/64-bit)
- **Características**: Muestra errores y mensajes de debug
- **Uso**: Para resolver problemas y errores

## 📋 ¿Cuál descargar?

### ✅ Usuario normal (recomendado)
```
AfoToRelocate.exe
```
- Descarga y ejecuta directamente
- Interfaz limpia sin consola
- Funciona en la mayoría de sistemas

### 🔧 Problemas de compatibilidad
```
AfoToRelocate_Compatible.exe
```
- Si el ejecutable estándar no funciona
- Error "no es una aplicación Win32 válida"
- Sistemas Windows más antiguos

### 🛠️ Necesitas diagnosticar errores
```
AfoToRelocate_Debug.exe
```
- Si la aplicación se cierra inmediatamente
- Para ver mensajes de error específicos
- Para reportar bugs con información detallada

## 🖥️ Requisitos del sistema

### Mínimos (todas las versiones)
- **SO**: Windows Vista SP2 o superior
- **RAM**: 256 MB
- **Espacio**: 50 MB libres
- **Arquitectura**: x86 (32-bit) o x64 (64-bit)

### Recomendados
- **SO**: Windows 10/11
- **RAM**: 1 GB
- **Espacio**: 100 MB libres
- **Arquitectura**: x64 (64-bit)

## 🔧 Instalación y uso

### Paso 1: Descargar
1. Descarga el ejecutable apropiado para tu sistema
2. No requiere instalación adicional

### Paso 2: Ejecutar
```
1. Doble clic en el archivo .exe
2. Si Windows pregunta, permite la ejecución
3. La aplicación se abrirá automáticamente
```

### Paso 3: Usar la aplicación
1. **Navegación**: Usa el panel izquierdo para seleccionar carpetas
2. **Escanear**: Haz clic en "Scan" para buscar archivos multimedia
3. **Seleccionar**: Marca los archivos que quieres procesar
4. **Procesar**: Haz clic en "Renombrar" para organizarlos

## ⚠️ Solución de problemas comunes

### "No es una aplicación Win32 válida"
1. Prueba `AfoToRelocate_Compatible.exe`
2. Verifica que tu Windows sea 32/64-bit compatible
3. Descarga nuevamente el archivo (puede estar corrupto)

### "Windows no puede encontrar el archivo"
1. Verifica que el archivo se descargó completamente
2. Extrae el archivo si está en un ZIP
3. Mueve el archivo a una carpeta sin espacios ni caracteres especiales

### "El antivirus bloquea el archivo"
1. Añade excepción en tu antivirus para el archivo
2. Descarga desde fuente oficial
3. Los falsos positivos son comunes con PyInstaller

### La aplicación se cierra inmediatamente
1. Usa `AfoToRelocate_Debug.exe` para ver el error
2. Ejecuta como administrador
3. Verifica los requisitos del sistema

## 📁 Archivos de soporte

### En caso de problemas, también tienes:
- **TROUBLESHOOTING.md**: Guía detallada de solución de problemas
- **requirements.txt**: Para ejecutar desde código fuente
- **src/**: Código fuente completo

### Ejecutar desde código fuente (alternativa)
```bash
# Si los ejecutables no funcionan
git clone [repositorio]
cd afotorelocate
pip install -r requirements.txt
python src/main.py
```

## 🆕 Actualizaciones

### ¿Cómo saber si hay una versión nueva?
1. Verifica la fecha de los archivos
2. Consulta el repositorio de GitHub
3. Compara con `version.json`

### ¿Cómo actualizar?
1. Descarga la nueva versión
2. Reemplaza el archivo .exe anterior
3. No requiere desinstalación

## 📊 Información técnica

### Tecnologías incluidas
- **Python 3.13**: Intérprete
- **tkinter**: Interfaz gráfica
- **PIL/Pillow**: Procesamiento de imágenes
- **PyInstaller**: Empaquetado

### Características del ejecutable
- **Tipo**: Aplicación Windows nativa
- **Dependencias**: Todas incluidas (standalone)
- **Portabilidad**: 100% portable
- **Instalación**: No requerida

## 🎯 Casos de uso típicos

### 📸 Fotógrafos
- Organizar sesiones fotográficas por fecha
- Renombrar automáticamente con metadatos EXIF
- Agrupar por mes y año

### 🎬 Video creadores
- Organizar footage por fecha de grabación
- Renombrar archivos de video automáticamente
- Mantener orden cronológico

### 👨‍👩‍👧‍👦 Uso familiar
- Organizar fotos familiares y vacaciones
- Eliminar duplicados y archivos mal nombrados
- Crear estructura de carpetas ordenada

### 💼 Uso profesional
- Archivar material multimedia por proyectos
- Mantener convenciones de nomenclatura
- Automatizar procesos de organización
