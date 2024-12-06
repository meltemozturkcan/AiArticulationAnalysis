from pathlib import Path
import logging

# Proje dizinleri
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

# Uygulama ayarları
ALLOWED_AUDIO_TYPES = ['wav', 'mp3']
MAX_FILE_SIZE_MB = 10
CLEANUP_INTERVAL_MINUTES = 30

# Uygulama başlıkları
APP_TITLE = "🎤 Ses Telaffuz Analizi"
APP_DESCRIPTION = "Ses telaffuzunuzu referans ses ile karşılaştırın."

# Model ayarları
GENERATION_CONFIG = {
    "temperature": 0.1,  # Daha deterministik yanıtlar için düşük sıcaklık
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1024,}

# Logging ayarları
logging.getLogger('google.generativeai.types').setLevel(logging.ERROR)