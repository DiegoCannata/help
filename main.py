import streamlit as st
from transformers import pipeline
import torch
import os

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Sentimientos IA", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos mejorados
st.markdown(
    """
    <style>
    /* Fondo con gradiente moderno */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0b6efd 0%, #0051b3 50%, #0b6efd 100%);
        color: #ffffff;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        padding: 20px;
    }
    
    /* Contenedor principal para centrar contenido */
    .main-container {
        max-width: 800px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Contenedor de imagen centrado */
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 10px;
        margin-top: 0px;
    }

    /* Mejorar la legibilidad del texto */
    h1, h2, h3, .stMarkdown p, .stText, .stCaption {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        text-align: center;
    }

    /* Contenedor de contenido */
    .content-box {
        background: rgba(255, 255, 255, 0.08);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 30px;
        width: 100%;
    }

    /* Botones más atractivos */
    .stButton>button {
        background: linear-gradient(135deg, #0062e6 0%, #0051b3 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        border: none !important;
        font-size: 18px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    /* Caja de texto mejorada */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 16px;
        padding: 16px !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        background: rgba(255, 255, 255, 0.12) !important;
    }

    /* Placeholder más visible */
    textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Etiquetas de los campos */
    .stTextArea label, .stTextInput label {
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 700 !important;
        font-size: 18px;
        margin-bottom: 10px;
    }

    /* Resultado destacado */
    .result-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 24px;
        border-radius: 16px;
        border-left: 5px solid #ffffff;
        margin: 20px 0;
    }
    
    .rating-stars {
        font-size: 32px;
        letter-spacing: 4px;
        margin: 10px 0;
        text-align: center;
    }
    
    .confidence-bar {
        height: 10px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
        margin: 15px 0;
        overflow: hidden;
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #4cd964 0%, #5ac8fa 100%);
        border-radius: 5px;
    }

    /* Ajustes responsivos */
    @media (max-width: 768px) {
        .content-box {
            padding: 20px;
        }
        
        .stButton>button {
            padding: 12px 24px !important;
        }
        
        .rating-stars {
            font-size: 24px;
        }
    }
    
    /* Ocultar elementos de Streamlit por defecto */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Logo centrado en la parte superior

# Mostrar ambas imágenes alineadas horizontalmente


img1_path = "images2.png"
img2_path = "f63ec0c9-c272-4641-95bb-c5a12105b151-removebg-preview.png"
logo_width = 800
logo_width2 = 175

img1_exists = os.path.exists(img1_path)
img2_exists = os.path.exists(img2_path)

st.markdown('<div class="image-container">', unsafe_allow_html=True)
if img1_exists and img2_exists:
    col_img1, col_img2 = st.columns([2, 1])
    with col_img1:
        st.image(img1_path, width=500)
    with col_img2:
        st.image(img2_path, width=180)
elif img1_exists:
    st.image(img1_path, use_column_width=True)
elif img2_exists:
    st.image(img2_path, use_column_width=True)
else:
    logo_file = st.file_uploader("Sube logo (PNG/JPG/JFIF)", type=["png", "jpg", "jpeg", "jfif"], label_visibility="collapsed")
    if logo_file is not None:
        st.image(logo_file, width=logo_width)
st.markdown('</div>', unsafe_allow_html=True)


# Mensaje principal mejorado
st.markdown("""
<div style='margin-bottom: 18px;'>
    <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>✨ Analizador de Sentimientos</h1>
    <p style='font-size: 1.2rem;'>Descubre el sentimiento detrás de cualquier texto con tecnología de inteligencia artificial</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 12px; margin: 20px 0;'>
    <h3>📝 ¿Cómo funciona?</h3>
    <ol>
        <li>Escribe o pega cualquier texto en el cuadro inferior</li>
        <li>Presiona el botón "Analizar Sentimiento"</li>
        <li>La IA te mostrará si el texto es positivo, negativo o neutral</li>
        <li>Verás una puntuación de 1 a 5 estrellas y el nivel de confianza del análisis</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Carga del modelo (cacheada para no recargar en cada interacción)
try:
    cache_decorator = st.cache_resource
except AttributeError:
    cache_decorator = lambda f: st.cache(allow_output_mutation=True)(f)

@cache_decorator
def load_sentiment_pipeline():
    device = 0 if torch.cuda.is_available() else -1
    return pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        device=device,
    )

with st.spinner("🔄 Cargando modelo de análisis de sentimientos..."):
    sentiment_model = load_sentiment_pipeline()

# Input de usuario
st.markdown('</div>', unsafe_allow_html=True)

# Mostrar input y resultado en dos columnas

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 Introduce el texto a analizar:")
    text = st.text_area(
        "Escribe o pega tu texto aquí:", 
        height=120,
        placeholder="Ej: 'Me encanta este producto, es exactamente lo que necesitaba.'",
        label_visibility="collapsed"
    )
    submitted = st.button("📊 Analizar Sentimiento", use_container_width=True)

with col2:
    st.markdown("### 📈 Resultados del Análisis")
    if submitted:
        if not text or not text.strip():
            st.error("Por favor, escribe algún texto antes de analizar.")
        else:
            with st.spinner("🤖 Analizando el sentimiento de tu texto..."):
                preds = sentiment_model(text)

            label = preds[0].get("label", "")
            score = preds[0].get("score", None)
            try:
                rating = int(label.split()[0])
            except Exception:
                rating = None
            stars = "⭐" * rating if rating else label
            if rating:
                interpretations = {
                    1: "Muy negativo 😔",
                    2: "Negativo 🙁",
                    3: "Neutral 😐",
                    4: "Positivo 🙂",
                    5: "Muy positivo 😄",
                }
                sentiment_text = interpretations.get(rating, "N/A")
            else:
                sentiment_text = label
            st.markdown(f"""
            <div class="result-box" style="margin-top:0; padding:10px 12px; border-radius:10px; font-size:0.95rem; max-width:260px; margin-left:auto; margin-right:auto;">
                <h3 style='margin-top:0; font-size:1.1rem;'>Sentimiento detectado: {sentiment_text}</h3>
                <div class="rating-stars" style='font-size:1.5rem; margin:6px 0;'>{stars}</div>
                <p style="text-align: center; font-size:0.95rem;"><strong>Clasificación del modelo:</strong> {label}</p>
            </div>
            """, unsafe_allow_html=True)
            if score is not None:
                st.markdown(f"**Nivel de confianza:** {score:.2%}")
                st.markdown(f"""
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {score*100}%"></div>
                </div>
                """, unsafe_allow_html=True)
                if score > 0.8:
                    st.success("✅ El modelo tiene alta confianza en este resultado")
                elif score > 0.6:
                    st.info("ℹ️  El modelo tiene confianza moderada en este resultado")
                else:
                    st.warning("⚠️  El modelo tiene baja confianza en este resultado")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255, 255, 255, 0.7);'>
    <p>Modelo usado: nlptown/bert-base-multilingual-uncased-sentiment</p>
    <p>✨ Tecnología Transformer para análisis de sentimientos en texto ✨</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
