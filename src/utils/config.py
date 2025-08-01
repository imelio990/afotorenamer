import os
import json

CONFIG_FILE = "config.json"

def load_config():
    """Carga la configuración desde el archivo config.json"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_config(config):
    """Guarda la configuración en el archivo config.json"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False

def get_last_directory():
    """Obtiene el último directorio guardado"""
    config = load_config()
    return config.get('last_directory', None)

def save_last_directory(directory):
    """Guarda el último directorio utilizado"""
    config = load_config()
    config['last_directory'] = directory
    return save_config(config)
