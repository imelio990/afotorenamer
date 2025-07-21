from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class ImageFileInfo:
    fname: str
    size: int
    ctime: float
    mtime: float
    exif_datetime_original: Optional[str] = None
    exif_datetime_digitized: Optional[str] = None
    exif_datetime: Optional[str] = None
    subdir: Optional[str] = None
    nuevo_nombre: Optional[str] = None
    min_date: Optional[datetime.datetime] = None
    camera_model: Optional[str] = None  # Nuevo campo para mostrar en el Treeview
