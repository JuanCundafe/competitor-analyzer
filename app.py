
import streamlit as st
import openai
import trafilatura
import requests
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Analizador de Competencia con IA", layout="centered")

st.title("🕵️‍♂️ Analizador de Competencia con IA")
st.markdown("Compara a tus competidores y encuentra tu oportunidad de diferenciación.")

urls_input = st.text_area("Introduce los sitios web de tus competidores (una por línea):", height=120)
own_description = st.text_input("Describe brevemente tu negocio (opcional):")

def extract_text_from_url(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        return trafilatura.extract(downloaded)
    except:
        return None

def analyze_with_gpt(content, own_desc=None):
    prompt = f"""Analiza el siguiente contenido de una página web de un competidor:\n\n{content}\n\n"""
    if own_desc:
        prompt += f"Mi negocio es: {own_desc}\n\n"
    prompt += """Devuélveme lo siguiente en formato Markdown:
1. Propuesta de valor detectada
2. Fortalezas del sitio
3. Oportunidades para diferenciarme
4. Tono de comunicación"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content

if st.button("🔍 Analizar"):
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
    if not urls:
        st.warning("Por favor ingresa al menos una URL.")
    else:
        for url in urls:
            st.markdown(f"### 🌐 {url}")
            with st.spinner("Extrayendo contenido..."):
                content = extract_text_from_url(url)
            if not content:
                st.error("No se pudo analizar esta URL.")
                continue
            with st.spinner("Analizando con IA..."):
                analysis = analyze_with_gpt(content, own_description)
            st.markdown(analysis)
