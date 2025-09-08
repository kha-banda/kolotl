# Configuración simple (usar variables de entorno en producción)
import os

DB_HOST = os.environ.get("DB_HOST", "69.62.71.171")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "caravanadestrucs")
DB_NAME = os.environ.get("DB_NAME", "scorpions")
DB_POOL_NAME = "mypool"
DB_POOL_SIZE = int(os.environ.get("DB_POOL_SIZE", 10))

HERE_API_KEY = os.environ.get("HERE_API_KEY", "1F91LCxBz_coxRzfxs5qybZKq0a-09Q40EyQMsP_ehA")
OPEN_WEATHER_KEY = os.environ.get("OPEN_WEATHER_KEY", "0c92193205b8016c9c0cedc51ebd650b")
WEATHERAPI_KEY = os.environ.get("WEATHERAPI_KEY", "ec66f746a0e14f57ac1152001242911")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
SECRET_KEY = os.environ.get("SECRET_KEY", "kolotl_unca")
