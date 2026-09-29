"""
🐝 Bee Emo-tional — The Y2K Sentiment Analyzer Blog
Aplicación Streamlit adaptada a la estética de Blog de los 2000s (MSN / Myspace / Blogger)

Instalación recomendada:
    pip install streamlit textblob googletrans==4.0.0-rc1 pandas pillow

Ejecución:
    streamlit run app.py
"""

import streamlit as st
from textblob import TextBlob
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# Configuración de página
st.set_page_config(
    page_title="★~ Bee Emo-tional ~★ Blog Spot",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# TRADUCTOR DE RESPALDO (ROBUSTO)
# ─────────────────────────────────────────────
def traducir_a_ingles(texto):
    """Traduce el texto a inglés usando googletrans con manejo de errores."""
    try:
        from googletrans import Translator
        translator = Translator()
        translation = translator.translate(texto, src="es", dest="en")
        return translation.text
    except Exception:
        # Fallback simple en caso de que googletrans falle por límites de API
        return texto

def crear_imagen_emoticones():
    """Genera una imagen retro Y2K si no existe emoticos.jpg localmente."""
    img = Image.new('RGB', (800, 150), color='#ff007f')
    d = ImageDraw.Draw(img)
    # Dibujar patrón divertido estilo 2000
    for x in range(0, 800, 40):
        d.line([(x, 0), (x+20, 150)], fill='#00ffff', width=3)
    return img

# ─────────────────────────────────────────────
# ESTILOS BLOG DE LOS 2000s (Y2K / MYSPACE STYLE)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,700;1,400&family=Press+Start+2P&display=swap');

    /* Fondo hiper-colorido y vivo */
    .stApp {
        background: linear-gradient(135deg, #ff99dd 0%, #ffcc00 25%, #66ffff 50%, #ff66cc 75%, #cc66ff 100%) !important;
        background-attachment: fixed !important;
        font-family: 'Comic Sans MS', 'Comic Neue', cursive, sans-serif !important;
    }

    /* Sidebar estilo Perfil de Myspace / MSN */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ff007f 0%, #7928ca 100%) !important;
        border-right: 4px dashed #ffff00 !important;
        box-shadow: 5px 0px 15px rgba(0,0,0,0.3);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-family: 'Comic Sans MS', cursive !important;
    }

    /* Encabezado del Blog Y2K */
    .blog-header {
        background: #ffff00;
        border: 4px solid #ff007f;
        box-shadow: 8px 8px 0px #00ffff, 16px 16px 0px #ff007f;
        padding: 20px;
        text-align: center;
        margin-bottom: 30px;
        border-radius: 15px;
    }
    
    .blog-title {
        font-family: 'Press Start 2P', 'Comic Sans MS', cursive !important;
        color: #ff007f !important;
        text-shadow: 3px 3px 0px #00ffff, 6px 6px 0px #000000;
        font-size: 2.2rem;
        margin: 0;
    }

    .blog-subtitle {
        color: #7928ca;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 10px;
    }

    /* Post de Blog Contenedor */
    .blog-post {
        background: #ffffff;
        border: 4px solid #000000;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 8px 8px 0px #ff007f;
    }

    .post-header {
        background: #00ffff;
        padding: 10px 15px;
        border-radius: 10px;
        border: 2px solid #000000;
        font-weight: bold;
        color: #000000;
        margin-bottom: 15px;
    }

    /* Cajas de entrada de texto */
    input[type="text"] {
        background-color: #ffffcc !important;
        border: 3px solid #ff007f !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-size: 1.1rem !important;
        font-family: 'Comic Sans MS', cursive !important;
    }

    /* Botones Neón Pop */
    .stButton > button {
        background: linear-gradient(180deg, #ff007f 0%, #ff66cc 100%) !important;
        color: #ffffff !important;
        border: 3px solid #000000 !important;
        border-radius: 15px !important;
        font-family: 'Comic Sans MS', cursive !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        box-shadow: 4px 4px 0px #000000 !important;
        text-shadow: 1px 1px 0px #000 !important;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #00ffff !important;
    }

    /* Badge de Sentimientos retro */
    .badge-positive {
        background: #00ff66;
        border: 3px solid #000;
        padding: 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 1.4rem;
        text-align: center;
        box-shadow: 4px 4px 0px #000;
    }
    .badge-negative {
        background: #ff3366;
        color: white;
        border: 3px solid #000;
        padding: 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 1.4rem;
        text-align: center;
        box-shadow: 4px 4px 0px #000;
    }
    .badge-neutral {
        background: #ffff00;
        border: 3px solid #000;
        padding: 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 1.4rem;
        text-align: center;
        box-shadow: 4px 4px 0px #000;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER ESTILO BLOG 2000s
# ─────────────────────────────────────────────
st.markdown("""
<div class="blog-header">
    <h1 class="blog-title">★~ Bee Emo-tional ~★</h1>
    <p class="blog-subtitle">✨ Welcome to my Emo & Emotional Feelings Diary Blog ~ XOXO ✨</p>
    <marquee style="color:#ff007f; font-weight:bold; margin-top:10px;">
        🐝 Bienvenido a Bee Emo-tional 🐝 :: Analizando buenas y malas vibras desde el 2006 :: Listen to My Chemical Romance & Smile!
    </marquee>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR ESTILO PERFIL MYSPACE / MSN
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🐝 About The Blogger")
    st.markdown("<b>User:</b> Bee_Emo_Queen<br><b>Mood:</b> Analyzing Text... 🎧<br><b>Status:</b> Online on MSN", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("📚 Diccionario Emo-cional")
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 10px; border: 2px solid #ffff00;">
        <h4 style="margin-top:0; color:#ffff00 !important;">📊 Polaridad</h4>
        <p style="font-size: 0.9rem;">Indica si el sentimiento expresado en el texto es positivo, negativo o neutral.</p>
        <p style="font-size: 0.85rem;"><b>Escala:</b> -1 (Muy triste/negativo 😔) a +1 (Muy feliz/positivo 😊).</p>
        
        <hr style="border: 1px dashed #fff;">
        
        <h4 style="margin-top:0; color:#ffff00 !important;">🧠 Subjetividad</h4>
        <p style="font-size: 0.9rem;">Mide cuánto del contenido es opinión/emoción personal frente a datos objetivos.</p>
        <p style="font-size: 0.85rem;"><b>Escala:</b> 0 (Totalmente objetivo/hecho) a 1 (Totalmente subjetivo/opinión).</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<b>Music Playing:</b><br>🎵 *Welcome to the Black Parade*", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CUERPO PRINCIPAL DEL BLOG
# ─────────────────────────────────────────────

# Cargar Imagen Banner
try:
    image = Image.open('emoticones.jpg')
except Exception:
    image = crear_imagen_emoticones()

col_post, col_widgets = st.columns([2.5, 1], gap="large")

with col_post:
    # POST 1: BANNER E INTRODUCCIÓN
    st.markdown("""
    <div class="blog-post">
        <div class="post-header">
            📝 POSTED BY Bee_Emo_Queen | 🕒 CATEGORY: SENTIMENT ANALYZER 2000
        </div>
    """, unsafe_allow_html=True)
    
    st.image(image, use_container_width=True)
    
    st.markdown("### ✨ ¿Cómo te sientes hoy? ¡Cuéntale a mi Blog!")
    st.write("Escribe aquí abajo la frase o pensamiento que quieras analizar. Mi robot Emo traducirá tus palabras y medirá tus sentimientos al instante ~ ★")
    
    # Campo de texto de entrada
    user_text = st.text_input('✍️ Escribe tu frase aquí:', placeholder='Ej: Hoy es un día súper genial para escuchar música...')
    
    if user_text:
        with st.spinner("🤖 Traduciendo y decodificando vibras Emo-cionales..."):
            # Traducción
            trans_text = traducir_a_ingles(user_text)
            
            # Análisis con TextBlob
            blob = TextBlob(trans_text)
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)
            
            st.markdown("---")
            st.markdown("#### 💬 RESULTADOS DEL ANÁLISIS")
            
            # Columnas para métricas
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f"<div style='background:#ffff99; border:2px solid #000; padding:10px; border-radius:10px; text-align:center;'><b>Polaridad:</b><br><span style='font-size:1.8rem; color:#ff007f;'>{polarity}</span></div>", unsafe_allow_html=True)
            with m2:
                st.markdown(f"<div style='background:#99ffff; border:2px solid #000; padding:10px; border-radius:10px; text-align:center;'><b>Subjetividad:</b><br><span style='font-size:1.8rem; color:#7928ca;'>{subjectivity}</span></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Diagnóstico de sentimiento
            if polarity > 0.0:
                st.markdown('<div class="badge-positive">Es un sentimiento Positivo 😊 🎉 <br><small>¡Súper buenas vibras!</small></div>', unsafe_allow_html=True)
            elif polarity < 0.0:
                st.markdown('<div class="badge-negative">Es un sentimiento Negativo 😔 🖤 <br><small>Momento Emo... ¡Ánimo!</small></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="badge-neutral">Es un sentimiento Neutral 😐 ☁️ <br><small>Equilibrio total.</small></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col_widgets:
    # WIDGET LATERAL DE BLOG
    st.markdown("""
    <div class="blog-post" style="padding:15px;">
        <h4 style="margin-top:0; color:#ff007f; border-bottom:2px solid #000;">💖 Blogroll Friends</h4>
        <ul style="padding-left:15px; font-size:0.95rem;">
            <li>xX_EmoBoy_2006_Xx</li>
            <li>Glitter_Girl_Y2K</li>
            <li>Punk_Rocker_99</li>
        </ul>
    </div>
    
    <div class="blog-post" style="padding:15px;">
        <h4 style="margin-top:0; color:#7928ca; border-bottom:2px solid #000;">🏷️ Blog Tags</h4>
        <span style="background:#ff99cc; border:1px solid #000; padding:2px 6px; border-radius:5px; font-size:0.8rem;">#TextBlob</span>
        <span style="background:#66ffff; border:1px solid #000; padding:2px 6px; border-radius:5px; font-size:0.8rem;">#Streamlit</span>
        <span style="background:#ffff66; border:1px solid #000; padding:2px 6px; border-radius:5px; font-size:0.8rem;">#Y2K</span>
    </div>
    """, unsafe_allow_html=True)
