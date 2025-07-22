import os
import datetime
from typing import Optional
from PIL import Image, ExifTags
from .image_types import ImageFileInfo

def get_image_files(directory):
    """Retrieve a list of image files from the specified directory."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in image_extensions]

def is_image_file(filename):
    """Check if the given filename is an image file."""
    return os.path.splitext(filename)[1].lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}

def get_image_file_info(directory: str, fname: str) -> Optional[ImageFileInfo]:
    """Obtiene la información de un archivo de imagen, incluyendo fechas EXIF y de fichero."""
    fpath = os.path.join(directory, fname)
    try:
        size = os.path.getsize(fpath)
        ctime = os.path.getctime(fpath)
        mtime = os.path.getmtime(fpath)
        exif_date_cols = ["DateTimeOriginal", "DateTimeDigitized", "DateTime"]
        exif_dates = {col: None for col in exif_date_cols}
        all_dates = [datetime.datetime.fromtimestamp(ctime), datetime.datetime.fromtimestamp(mtime)]
        camera_make = None
        camera_model = None
        image = Image.open(fpath)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name in exif_date_cols and value:
                    exif_dates[tag_name] = value
                    try:
                        dt = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                        all_dates.append(dt)
                    except Exception:
                        pass
                # Obtener marca y modelo de la cámara
                if tag_name == "Make" and value:
                    camera_make = value
                if tag_name == "Model" and value:
                    camera_model = value
        min_date = min(all_dates) if all_dates else None
        subdir = min_date.strftime("%Y%m") if min_date else None
        nuevo_nombre = calcular_nuevo_nombre(fname, min_date, camera_make, camera_model)
        # Incluye el modelo en el objeto para mostrarlo en el Treeview
        return ImageFileInfo(
            fname=fname,
            size=size,
            ctime=ctime,
            mtime=mtime,
            exif_datetime_original=exif_dates["DateTimeOriginal"],
            exif_datetime_digitized=exif_dates["DateTimeDigitized"],
            exif_datetime=exif_dates["DateTime"],
            subdir=subdir,
            nuevo_nombre=nuevo_nombre,
            min_date=min_date,
            camera_model=camera_model
        )
    except Exception as e:
        return None

def calcular_nuevo_nombre(fname: str, min_date: Optional[datetime.datetime], camera_make: Optional[str] = None, camera_model: Optional[str] = None) -> str:
    import re
    base, ext = os.path.splitext(fname)
    if min_date:
        fecha_str = min_date.strftime("%Y%m%d_%H%M%S")
        # Elimina cualquier patrón de fecha al principio: yyyymmddhhmiss o yyyymmdd_hhmiss
        base = re.sub(r'^(\d{8}_\d{6}|\d{8}\d{6}|\d{8}_\d{6}_|\d{8}\d{6}_|\d{8}_\d{6}-|\d{8}\d{6}-)', '', base)
        # También elimina si hay un guion bajo o guion tras la fecha
        base = re.sub(r'^(\d{8}_\d{6}[_-]?)', '', base)
        # Solo añade el modelo si existe
        cam_info = ""
        if camera_model:
            cam_info = camera_model
        if cam_info:
            return f"{fecha_str}_{cam_info}_{base}{ext}"
        else:
            return f"{fecha_str}_{base}{ext}"
    else:
        return fname

def mover_archivo(info: ImageFileInfo, directory: str, log_func) -> bool:
    import shutil
    import re
    if not info.subdir or not info.nuevo_nombre:
        log_func(f"Faltan datos para {info.fname}, omitiendo.")
        return False
    # Forzar formato yyyy_mm para el subdirectorio
    import re
    subdir = str(info.subdir)
    # Si info.subdir es una fecha, conviértela a yyyy_mm
    match = re.match(r"(\d{4})[-_/]?(\d{2})", subdir)
    if match:
        subdir = f"{match.group(1)}_{match.group(2)}"
    src_path = os.path.join(directory, info.fname)

    # --- Nueva lógica para evitar subdirectorio hijo ---
    # Si el directorio actual ya es yyyymm, y el subdir destino es otro yyyymm, muévelo como hermano
    current_dirname = os.path.basename(directory)
    if re.fullmatch(r"\d{6}", current_dirname):
        # Si el subdir destino es diferente al actual, sube un nivel y ponlo como hermano
        if subdir != current_dirname:
            dest_dir = os.path.join(os.path.dirname(directory), subdir)
        else:
            log_func(f"El archivo ya está en el subdirectorio correcto: {subdir}")
            return False
    else:
        dest_dir = os.path.join(directory, subdir)
    os.makedirs(dest_dir, exist_ok=True)
    base, ext = os.path.splitext(info.nuevo_nombre)
    dest_path = os.path.join(dest_dir, info.nuevo_nombre)
    idx = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_dir, f"{base}_{idx}{ext}")
        idx += 1
    try:
        shutil.move(src_path, dest_path)
        log_func(f"Movido: {src_path} -> {dest_path}")
        return True
    except Exception as e:
        log_func(f"Error al mover {info.fname}: {e}")
        return False