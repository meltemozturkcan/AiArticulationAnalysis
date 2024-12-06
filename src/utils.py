import streamlit as st
from pathlib import Path
from datetime import datetime
from .config import UPLOAD_DIR

def save_audio_file(uploaded_file):
    """Yüklenen ses dosyasını kaydeder"""
    if uploaded_file is None:
        return None
    
    file_path = UPLOAD_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def display_results(results):
    """Analiz sonuçlarını gösterir"""
    if not results:
        return
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Telaffuz Puanı", f"{results['pronunciation_score']:.1f}/100")
    with col2:
        st.metric("Güven Skoru", f"{results['confidence_score']:.1f}/100")
    
    st.subheader("İyileştirilmesi Gereken Alanlar")
    st.write(results['areas_of_improvement'])
    
    st.subheader("Detaylı Geri Bildirim")
    feedback = results['detailed_feedback']
    
    cols = st.columns(3)
    with cols[0]:
        st.info("Ünlü Sesler")
        st.write(feedback['vowel_sounds'])
    
    with cols[1]:
        st.info("Ünsüz Sesler")
        st.write(feedback['consonant_sounds'])
    
    with cols[2]:
        st.info("Netlik")
        st.write(feedback['clarity'])

def cleanup_old_files(max_age_minutes=30):
    """Eski dosyaları temizler"""
    current_time = datetime.now()
    for file_path in UPLOAD_DIR.glob("*"):
        if file_path.name == ".gitkeep":
            continue
        file_age = (current_time - datetime.fromtimestamp(file_path.stat().st_mtime))
        if file_age.total_seconds() > (max_age_minutes * 60):
            file_path.unlink(missing_ok=True)