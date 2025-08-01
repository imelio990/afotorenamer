# 🔧 Guía de Solución de Problemas - AfoToRelocate

## ❌ Error: "No es una versión válida" o "No es una aplicación Win32 válida"

### 🔍 Diagnóstico del problema

Este error puede ocurrir por varias razones:

1. **Incompatibilidad de arquitectura**: Ejecutable de 64-bit en sistema de 32-bit
2. **Versión de Windows muy antigua**: Ejecutable creado con Python nuevo en Windows viejo
3. **Archivo corrupto**: Problema durante la descarga o transferencia
4. **Antivirus**: Bloqueo del archivo por parte del antivirus

### 🛠️ Soluciones disponibles

#### Opción 1: Ejecutable de compatibilidad mejorada
```
AfoToRelocate_Compatible.exe
```
- Creado con parámetros optimizados para compatibilidad
- Sin UPX compression
- Imports explícitos para mejor detección

#### Opción 2: Ejecutable con consola de debug
```
AfoToRelocate_Debug.exe
```
- Incluye ventana de consola para ver errores
- Útil para diagnosticar problemas específicos
- Mostrará mensajes de error detallados

#### Opción 3: Ejecutable estándar (original)
```
AfoToRelocate.exe
```
- Versión original sin ventana de consola
- Más pequeño pero puede tener problemas de compatibilidad

### 📋 Pasos de solución

#### 1. Verificar compatibilidad del sistema
```cmd
# Verificar arquitectura del sistema
systeminfo | findstr /B /C:"System Type"

# Verificar versión de Windows
ver
```

#### 2. Probar versiones en orden de compatibilidad
1. **Primero**: `AfoToRelocate_Debug.exe`
   - Si funciona pero muestra consola, usar la versión compatible
2. **Segundo**: `AfoToRelocate_Compatible.exe`
   - Versión optimizada para compatibilidad
3. **Tercero**: `AfoToRelocate.exe`
   - Versión más limpia si funciona

#### 3. Verificar integridad del archivo
```cmd
# Verificar que el archivo no esté corrupto
dir AfoToRelocate*.exe

# Debería mostrar archivos de ~18MB
```

#### 4. Desactivar temporalmente el antivirus
- Algunos antivirus bloquean ejecutables generados por PyInstaller
- Crear excepción para el archivo o carpeta

#### 5. Ejecutar como administrador
- Clic derecho → "Ejecutar como administrador"
- Puede resolver problemas de permisos

### 🖥️ Requisitos mínimos del sistema

#### Para versiones estándar:
- **Windows**: 7 SP1 / 8.1 / 10 / 11
- **Arquitectura**: x64 (64-bit)
- **RAM**: 512 MB mínimo
- **Espacio**: 50 MB libres

#### Para máxima compatibilidad:
- **Windows**: Vista SP2 o superior
- **Arquitectura**: x86 (32-bit) o x64 (64-bit)
- **RAM**: 256 MB mínimo

### 🔄 Crear ejecutable para Windows más antiguos

Si necesitas compatibilidad con versiones muy antiguas de Windows:

#### Método 1: Python más antiguo
```bash
# Usar Python 3.8 o 3.9 en lugar de 3.13
python -m PyInstaller --onefile --windowed --name=AfoToRelocate_Legacy --target-arch=i386 src/main.py
```

#### Método 2: Compilación en sistema objetivo
- Compilar el ejecutable directamente en el sistema donde se va a usar
- Garantiza máxima compatibilidad con esa versión de Windows

### 🚨 Alternativas si el ejecutable no funciona

#### Opción A: Ejecutar desde código fuente
```bash
# Instalar Python 3.8+ en el sistema objetivo
python -m pip install -r requirements.txt
python src/main.py
```

#### Opción B: Versión portable de Python
1. Descargar Python portable
2. Extraer en carpeta del proyecto
3. Ejecutar con Python portable

#### Opción C: Usar máquina virtual
- VM con Windows compatible para ejecutar la aplicación

### 📞 Información de debug útil

Si necesitas reportar el problema, incluye:

```cmd
# Información del sistema
systeminfo > sistema.txt

# Información del error
# Captura de pantalla del mensaje de error

# Versión intentada
# AfoToRelocate.exe / AfoToRelocate_Compatible.exe / AfoToRelocate_Debug.exe

# Método de ejecución
# Doble clic / Línea de comandos / Como administrador
```

### ✅ Verificación de funcionamiento

Una vez que el ejecutable funcione, deberías ver:

1. **Ventana principal** con dos paneles
2. **TreeView** a la izquierda para navegación
3. **Lista de archivos** a la derecha
4. **Botones** "Scan" y "Renombrar"
5. **Área de log** en la parte inferior

Si ves esto, ¡el ejecutable está funcionando correctamente!

### 🆘 Última opción: Recrear ejecutable

Si ninguna versión funciona, puedes recrear el ejecutable:

```bash
# En el sistema donde vas a usarlo
git clone [repositorio]
cd afotorelocate
pip install pyinstaller pillow
python -m PyInstaller --onefile --console src/main.py
```

Esto garantiza compatibilidad total con el sistema objetivo.
