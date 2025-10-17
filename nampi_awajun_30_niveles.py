import streamlit as st
import random

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(page_title="Nampi Awajún", page_icon="🌿", layout="centered")

# Fondo selva amazónica
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?fit=crop&w=1400&q=80');
    background-size: cover;
    background-position: center;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
[data-testid="stToolbar"] {visibility: hidden;}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ==============================
# BASE DE DATOS DE CARTAS (30 niveles)
# ==============================
# Cada nivel tiene 2 pares adicionales, nivel 1 = 4 pares
cartas_base = [
    ("Jabalí", "wájin", "https://i.ibb.co/jWzZp6r/jabali.gif"),
    ("Tucán", "túkán", "https://i.ibb.co/8xWfM6D/tucan.gif"),
    ("Arco", "ápin", "https://i.ibb.co/F6m8Xf6/arco.gif"),
    ("Cerbatana", "tsúin", "https://i.ibb.co/5v3Vqf1/cerbatana.gif"),
    ("Plátano", "bánan", "https://i.ibb.co/xX7KJd3/platano.gif"),
    ("Yuca", "yáká", "https://i.ibb.co/2t7Y9PZ/yuca.gif"),
    ("Río", "tsáim", "https://i.ibb.co/qB2R0kL/rio.gif"),
    ("Flor", "táwen", "https://i.ibb.co/Vp0x3DJ/flor.gif"),
    ("Mono", "mátin", "https://i.ibb.co/tY3Q2MK/mono.gif"),
    ("Puma", "jásin", "https://i.ibb.co/5Gz9x9m/puma.gif"),
    ("Serpiente", "sháwin", "https://i.ibb.co/0rM1vZG/serpiente.gif"),
    ("Pez", "náwa", "https://i.ibb.co/7bPZydH/pez.gif"),
    ("Canoa", "nápan", "https://i.ibb.co/fYx0Fj2/canoa.gif"),
    ("Campo", "náwin", "https://i.ibb.co/qMw3F7J/campo.gif"),
    ("Lanza", "ápin", "https://i.ibb.co/xh4pGkD/lanza.gif"),
    ("Leña", "tájun", "https://i.ibb.co/ZLhF0Qc/lenya.gif"),
    ("Sol", "iwá", "https://i.ibb.co/HX8g9rG/sol.gif"),
    ("Luna", "nentá", "https://i.ibb.co/x2zvC4r/luna.gif"),
    ("Estrella", "pashí", "https://i.ibb.co/k9JX8gF/estrella.gif"),
    ("Montaña", "namák", "https://i.ibb.co/ySx0cG7/montana.gif"),
    ("Fuego", "jintá", "https://i.ibb.co/BsH4xjB/fuego.gif"),
    ("Agua", "nía", "https://i.ibb.co/1qTjF5b/agua.gif"),
    ("Niño", "pákem", "https://i.ibb.co/ysG7rK5/nino.gif"),
    ("Niña", "tsápen", "https://i.ibb.co/6mN7jQw/nina.gif"),
    ("Madre", "nánan", "https://i.ibb.co/5Wf4M8J/madre.gif"),
    ("Padre", "apá", "https://i.ibb.co/8cT9X2h/padre.gif"),
    ("Perro", "yáujin", "https://i.ibb.co/Lx7mN0C/perro.gif"),
    ("Gato", "mítsu", "https://i.ibb.co/3fy3K6v/gato.gif"),
    ("Pájaro", "wíin", "https://i.ibb.co/kG9kH0J/pajaro.gif"),
]

# ==============================
# FUNCIONES
# ==============================

def generar_nivel(nivel):
    pares = 4 + (nivel - 1) * 2
    cartas_nivel = random.sample(cartas_base, min(pares, len(cartas_base)))
    cartas_nivel = cartas_nivel * 2  # duplicar pares
    random.shuffle(cartas_nivel)
    return cartas_nivel

# ==============================
# INICIALIZAR ESTADO
# ==============================
if 'nivel' not in st.session_state:
    st.session_state.nivel = 1
    st.session_state.cartas_volteadas = []
    st.session_state.matched = []
    st.session_state.puntuacion = 0
    st.session_state.cartas = generar_nivel(st.session_state.nivel)

st.title(f"🌿 Nampi Awajún – Cazadores del Bosque (Nivel {st.session_state.nivel}) 🌿")
st.write("¡Explora la selva y encuentra los pares! Aprende vocabulario en Awajún mientras juegas.")

# ==============================
# MOSTRAR CARTAS
# ==============================
cols = st.columns(4)
for idx, carta in enumerate(st.session_state.cartas):
    nombre_es, nombre_aw, img_url = carta
    if idx in st.session_state.matched:
        cols[idx % 4].image(img_url, caption=f"{nombre_es} ({nombre_aw})", use_column_width=True)
    else:
        if cols[idx % 4].button("🂠", key=idx):
            if len(st.session_state.cartas_volteadas) < 2:
                st.session_state.cartas_volteadas.append(idx)

# ==============================
# LÓGICA DE COMPARACIÓN
# ==============================
if len(st.session_state.cartas_volteadas) == 2:
    idx1, idx2 = st.session_state.cartas_volteadas
    c1, c2 = st.session_state.cartas[idx1], st.session_state.cartas[idx2]
    if c1[1] == c2[1] and idx1 != idx2:
        st.session_state.puntuacion += 5
        st.session_state.matched.extend([idx1, idx2])
        st.success(f"✅ ¡Correcto! {c1[0]} = {c1[1]}")
    else:
        st.error("❌ Intenta de nuevo")
    st.session_state.cartas_volteadas = []
    st.experimental_rerun()

# ==============================
# PUNTUACIÓN Y AVANCE DE NIVEL
# ==============================
st.write(f"🏆 Puntuación actual: {st.session_state.puntuacion}")

if len(st.session_state.matched) == len(st.session_state.cartas):
    st.balloons()
    st.success("🎉 ¡Felicidades! Has completado el nivel.")
    if st.button("🔁 Siguiente Nivel"):
        st.session_state.nivel += 1
        if st.session_state.nivel > 30:
            st.success("🏁 ¡Completaste los 30 niveles! Felicidades 🌿")
            st.session_state.nivel = 1
            st.session_state.puntuacion = 0
        st.session_state.cartas_volteadas = []
        st.session_state.matched = []
        st.session_state.cartas = generar_nivel(st.session_state.nivel)
        st.experimental_rerun()