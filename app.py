import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Proje kök dizinini Python yoluna ekle
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from src.analyzer import AudioAnalyzer
from src.utils import save_audio_file, display_results, cleanup_old_files
from src.config import (
    APP_TITLE, 
    APP_DESCRIPTION, 
    ALLOWED_AUDIO_TYPES, 
    UPLOAD_DIR, 
    CLEANUP_INTERVAL_MINUTES
)
def main():
    # Uygulama yapılandırması
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🎤",
        layout="wide"
    )
    
    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)
    
    # Upload klasörünü oluştur
    UPLOAD_DIR.mkdir(exist_ok=True)
    
    # Eski dosyaları temizle
    cleanup_old_files(CLEANUP_INTERVAL_MINUTES)
    
    # API Key yönetimi
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        key="api_key_input",
        help="API anahtarınızı girin"
    )
    
    if api_key:
        st.session_state.api_key = api_key
    
    if not st.session_state.api_key:
        st.warning("Lütfen Gemini API anahtarınızı girin.")
        return
    
    # Ses dosyası yükleme alanları
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Referans Ses")
        reference_audio = st.file_uploader(
            "Referans ses dosyasını yükleyin",
            type=ALLOWED_AUDIO_TYPES,
            key="reference"
        )
    
    with col2:
        st.subheader("Test Sesi")
        test_audio = st.file_uploader(
            "Test ses dosyasını yükleyin",
            type=ALLOWED_AUDIO_TYPES,
            key="test"
        )
    
    # Harf seçimi
    letter = st.text_input(
        "Analiz edilecek harfi girin:",
        max_chars=1
    ).upper()
    
    # Analiz butonu
    if st.button(
        "Analiz Et",
        disabled=not (letter and reference_audio and test_audio),
        help="Ses dosyalarını karşılaştır"
    ):
        with st.spinner("Ses analizi yapılıyor..."):
            try:
                # Ses dosyalarını kaydet
                ref_path = save_audio_file(reference_audio)
                test_path = save_audio_file(test_audio)
                
                if ref_path and test_path:
                    # Analiz yap
                    analyzer = AudioAnalyzer(st.session_state.api_key)
                    results = analyzer.analyze(letter, str(ref_path), str(test_path))
                    
                    if results:
                        st.success("Analiz tamamlandı!")
                        display_results(results)
                        
                        # Sonuçları JSON olarak indirme
                        st.download_button(
                            "Sonuçları İndir",
                            data=json.dumps(results, indent=2, ensure_ascii=False),
                            file_name=f"analiz_sonucu_{letter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    # Geçici dosyaları temizle
                    if ref_path:
                        ref_path.unlink(missing_ok=True)
                    if test_path:
                        test_path.unlink(missing_ok=True)
                        
            except Exception as e:
                st.error(f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()