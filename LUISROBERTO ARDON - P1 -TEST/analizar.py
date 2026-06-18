import os
import numpy as np
import pandas as pd
import librosa
import streamlit as st


#Página web:

st.set_page_config(         #Configuramos la pestaña para la página web
    page_title= "🎵 Mis Canciones Favoritas",
    page_icon = "🎵",
    layout = "wide",
    initial_sidebar_state = "expanded"
)


CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))     #Creamos carpeta para análisis de las canciones descargadas
CARPETA_CANCIONES = os.path.join(CARPETA_SCRIPT, "Canciones_favs")  #Carpeta caniones con el path hacia la carpeta "Canciones_favs"

#Puntuación subjetiva
#Organizado en tuplas

#Tempo (BPM, Beats per minute)
RANGOS_TEMPO = [
    (0, 60, 40, 50),      #(valor_min  valor_max (BPS)  puntaje_min   puntaje_max)
    (60, 90, 51, 65),
    (90, 110, 66, 80),
    (110, 130, 81, 90),
    (130, 200, 91, 100),
]

#Energía (RMS) - qué tan "fuerte"/inteso suena en promedio

RANGOS_ENERGIA = [
    (0.00, 0.05, 40, 55),
    (0.05, 0.10, 56, 75),
    (0.10, 0.15, 71, 90),
    (0.15, 0.30, 91, 100),
]

#Brillantez (Hz) - sonido "brillante" vs "oscuro"

RANGOS_BRILLANTEZ = [
    (0, 1000, 40, 55),
    (1000, 2000, 56, 70),
    (2000, 3000, 71, 85),
    (3000, 5000, 86, 100),
]

#Ancho de banda espectral - qué tan "amplio/variado" es el sonido

RANGOS_ANCHO_BANDA = [
    (0, 1000, 40, 55),
    (1000, 2000, 56, 70),
    (2000, 3000, 71, 85),
    (3000, 5000, 86, 100),
]

#Zero Crossing Rate - relacionado con percusividad/ruido

RANGOS_ZCR = [
    (0.00, 0.03, 40, 55),
    (0.03, 0.06, 56, 70),
    (0.06, 0.10, 71, 85),
    (0.10, 0.30, 86, 100),
]

#Contraste especial - diferencia entre picos y valles de frecuencia
#Valores altos = sonido "nítido"/"definido" (graves y agudos marcados)

RANGOS_CONTRASTE = [
    (0, 15, 40, 55),
    (15, 20, 56, 70),
    (20, 25, 71, 85),
    (25, 40, 86, 100),
]

#2. Ponderación para el puntaje final

#Define que tanto influye cada característica en el puntaje de "cuanto te gusta la cancion". La suma
#debe ser 1.0

PONDERACION = {
    "tempo": 0.35,
    "energia": 0.25,
    "brillantez": 0.15,
    "ancho_banda": 0.10,
    "zcr": 0.05,
    "contraste": 0.10
}

#3. Funciones de operación

def asignar_puntaje(valor, rangos):  #1ra definición -- asignamos puntaje utilizando interpolación lineal del rango establecido previamente
    """
    Convierte un valor númerico en un puntaje subjetivo,
    usando interpolación lineal dentro del rango correspondiente
    """
    for (v_min, v_max, p_min, p_max) in rangos:
        if v_min <= valor <= v_max:   #que la interpolación comience en el valor del medio para ponderar
            if v_max == v_min:
                return p_min
            proporcion = (valor - v_min) / (v_max - v_min)   #
            return p_min + proporcion * (p_max - p_min)
        
    if valor < rangos[0][0]:  #Solo por si el valor cae fuera de todos los rangos definidos, se asigna al extremo mas cercano
        return rangos[0][2]
    return rangos[-1][3]

def extraer_caracteristicas(ruta):     #2da definición -- extraemos características cuantitativas de las canciones por medio de la librería
    """
    Carga un archivo de audio y extrae las caracteristicas 
    cuantificables más relevantes con Librosa
    """

    y, sr = librosa.load(ruta)  #y, sr son las variables que asignamos para obtener las variables (se usan dos porque la librería pide 2 parámetros)

#TEMPO (BPM)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(np.atleast_1d(tempo)[0])

#Energía (RMS)

    rms = librosa.feature.rms(y=y) #El RMS es la medición del volumen promedio o la potencia real y continua de una señal de audio
    energia = float(np.mean(rms)) #el np.mean convierte todos los valores que arroja el rms en un promedio que sea mas facil de cuantificar
    rms_maximo = float(np.mean(rms))
    rango_dinamico = rms_maximo - energia

#Brillantez (centroide espectral)

    centroide = librosa.feature.spectral_centroid(y=y, sr=sr)
    brillantez = float(np.mean(centroide))

#Ancho de banda espectral

    ancho_banda = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    ancho_banda = float(np.mean(ancho_banda))

#Zero Crossing Rate

    zcr = librosa.feature.zero_crossing_rate(y)
    zcr = float(np.mean(zcr))

#Contraste espectral

    contraste = librosa.feature.spectral_contrast(y=y, sr=sr)
    contraste_promedio = float(np.mean(contraste))

#Duración total

    duracion = librosa.get_duration(y=y, sr=sr)

#Picos de energía

    onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")
    tiempo_primer_pico = float((onsets[0]) if len(onsets) > 0 else 0.0)
 
    return {               #Nos devuelve los datos númericos que extrajimos y los asignamos a las variables con el mismo nombre
        "tempo": tempo,
        "energia": energia,
        "brillantez": brillantez, 
        "ancho_banda": ancho_banda,
        "zcr": zcr, 
        "contraste": contraste_promedio,
        "duracion": duracion,
        "tiempo_primer_pico": tiempo_primer_pico,
    }

def calcular_puntajes(caracteristicas):  #3ra definición -- Por medio de cálculos matemáticos calculamos los puntajes subjetivos sobre la "raw_data"
    """
    Aplica los rangos subjetivos a cada característica numérica y
    calcula el puntaje final ponderado
    """
    puntaje_tempo = asignar_puntaje(caracteristicas["tempo"], RANGOS_TEMPO) #asignamos puntaje combinando la 1. definición asignar puntaje, 2. caracteristicas (variable a analizar) (es la raw_data) y 3. los rangos de la tupla
    puntaje_energia = asignar_puntaje(caracteristicas["energia"], RANGOS_ENERGIA)
    puntaje_brillantez = asignar_puntaje(caracteristicas["brillantez"], RANGOS_BRILLANTEZ)
    puntaje_ancho = asignar_puntaje(caracteristicas["ancho_banda"], RANGOS_ANCHO_BANDA)
    puntaje_zcr = asignar_puntaje(caracteristicas["zcr"], RANGOS_ZCR)
    puntaje_contraste = asignar_puntaje(caracteristicas["contraste"], RANGOS_CONTRASTE)

    puntaje_final= (
        puntaje_tempo * PONDERACION["tempo"]  #Calculamos el puntaje obtenido con la ponderación subjetiva que establecimos previamente
        + puntaje_energia * PONDERACION["energia"]
        + puntaje_brillantez * PONDERACION["brillantez"]
        + puntaje_ancho * PONDERACION["ancho_banda"]
        + puntaje_zcr * PONDERACION["zcr"]
        + puntaje_contraste * PONDERACION["contraste"]
    )

    return {
        "puntaje_tempo": round(puntaje_tempo, 2),   #Nos devuelve el puntaje (de 0 a 100) con 2 decimales
        "puntaje_energia": round(puntaje_energia, 2),
        "puntaje_brillantez": round(puntaje_brillantez, 2),
        "puntaje_ancho_banda": round(puntaje_ancho, 2),
        "puntaje_zcr": round(puntaje_zcr,2 ),
        "puntaje_contraste": round(puntaje_contraste, 2),
        "puntaje_final": round(puntaje_final, 2),
    }

#Interfaz del usuario:

st.title("🎵 Analizador de Mis Canciones Favoritas")   #Creamos los títulos y subtítulos de la página web
st.markdown(" Análisis musical con **Librosa** Parcial I - Programación")
st.divider()  #Permite esconder el código


#SIDEBAR

with st.sidebar:   #Pestaña de configuración
    st.header("⚙️ Configuración")

    #Verficar que la carpeta existe
    if not os.path.isdir(CARPETA_CANCIONES):  #Mensaje de error en caso no salga o cargue la carpeta
        st.error(
            f"No se econtró la carpeta de canciones. \n\n"
            f"Ruta buscada: \n'{os.path.abspath(CARPETA_CANCIONES)}"
        )
        st.stop()
    
    archivos_disponibles = sorted([
        f for f in os.listdir(CARPETA_CANCIONES)
        if f.lower().endswith(".mp3")
    ])

#Selección de canciones:

st.subheader("📁 Canciones")                #Crea la pestaña donde se ponen en display las canciones descargadas en la carpeta
canciones_seleccionadas = st.multiselect(
    "Elige las canciones a analizar:",
    options = archivos_disponibles,
    default = archivos_disponibles,
    help = "Puedes seleccionar 1 o más canciones"
)

st.divider()

#Slider de pesos
st.subheader("⚖️ Pesos del puntaje final")     #Barra interactiva para ajustar las ponderaciones a gusto del usuario
st.caption("Mueve los sliders para cambiar cuánto influye cada característica.")

w_tempo = st.slider("🥁 Tempo",          0, 10, 7)  #Rango del slider (inicio, fin, valor preestablecido)
w_energia = st.slider("⚡ Energía",         0, 10, 5)
w_brillantez = st.slider("✨ Brillantez",      0, 10, 3)
w_ancho = st.slider("📊 Ancho de banda",  0, 10, 2)
w_zcr = st.slider("〰️ ZCR",             0, 10, 1)
w_contraste = st.slider("🎚️ Contraste",       0, 10, 2)

#Normalizar para que sumen 1.0
total = w_tempo + w_energia + w_brillantez + w_ancho + w_zcr + w_contraste
if total ==0:
    total = 1
PONDERACION = {
    "tempo": w_tempo / total,
    "energia": w_energia / total,
    "brillantez": w_brillantez / total,
    "ancho_banda": w_ancho / total,
    "zcr": w_zcr / total,
    "contraste": w_contraste / total,
}

st.caption(          #Pestaña visible donde se actualizan los porcentajes linkeados a la barra interactiva que coloca el usuario
    f"Tempo {PONDERACION["tempo"]:.0%} · Energía {PONDERACION["energia"]: .0%} · "
    f"Brillantez {PONDERACION["brillantez"]: .0%} · Ancho {PONDERACION["ancho_banda"]: .0%} · "
    f"ZCR {PONDERACION["zcr"]: .0%} · Contraste {PONDERACION["contraste"]: .0%}"
)

st.divider()
analizar_btn = st.button(
    "🔍 Analizar canciones",
    type = "primary",
    use_container_width = True
)

#Pantalla Inicial

if not analizar_btn:
    st.info("👈 Selecciona las canciones en el panel izquierdo y ajusta los pesos." \
    "Luego presiona **Analizar canciones**.")
    st.stop()

if not canciones_seleccionadas:
    st.warning("⚠️ No seleccionaste ninguna canción. " \
    "Por favor elige al menos una en el panel izquierdo.")
    st.stop()


#ANÁLISIS

resultados = []  #Aqui se guarda la variable resultados como contador para almacenar los datos finales de la canción
barra = st.progress(0, text="Inciando análisis...")

for i, archivo in enumerate(canciones_seleccionadas):   #Ciclo que recorre todas las canciones seleccionadas
    barra.progress(i / len(canciones_seleccionadas), text = f"Analizando: {archivo}...")   #Actualiza la barra de progreso mientras revisa la data
    ruta = os.path.join(CARPETA_CANCIONES, archivo)

    try:   #Ejecutar este bloque
        caracteristicas = extraer_caracteristicas(ruta) # Aqui se analiza la canción (raw data)
        puntajes = calcular_puntajes(caracteristicas) #Calcula los puntajes con la definición establecida previamente

        nombre_limpio = os.path.splitext(archivo)[0] #quita el .mp3
        fila = {"cancion": nombre_limpio}
        fila.update(caracteristicas)
        fila.update(puntajes)
        resultados.append(fila)
    except Exception as e:
        st.warning(f"No se pudo analizar **{archivo}**: {e}")

barra.progress(1.0, text = "✅ ¡Análisis completado!")

if not resultados:
    st.error("No se pudo analizar ninguna canción. Revisa los archivos.")
    st.stop()


#Construir DataFrame

df = pd.DataFrame(resultados)  #Convierte la lista de resultados en una tabla
df = df.sort_values(by="puntaje_final", ascending=False).reset_index(drop=True) #La ordena por puntaje
df.index = df.index + 1
numericas = df.select_dtypes(include=[float, int]).columns
df[numericas] = df[numericas].round(2)


#Sección decorativa de la página web
#SECCIÓN 1: RANKING CON MÉTRICAS DESTACADAS

st.header("🏆 Ranking de canciones")

cols = st.columns(min(3, len(df)))
medallas = ["🥇", "🥈", "🥉"]
for idx, col in enumerate(cols):
    row = df.iloc[idx]
    col.metric(
        label=f"{medallas[idx]} #{idx + 1}",
        value = row["cancion"],
        delta = f"{row["puntaje_final"]} / 100 pts"
    )

st.divider()

#SECCIÓN 2: Gráfica puntaje final

st.subheader("📊 Puntaje final por canción")
chart_df = df[["cancion", "puntaje_final"]].set_index("cancion")
st.bar_chart(chart_df, height=350)

st.divider()

#SECCIÓN 3: TABLA COMPARATIVA CON COLORES

st.subheader("📋 Tabla comparativa de características")

columnas_tabla = [
    "cancion", "tempo", "energia", "brillantez", "contraste", "duracion", "puntaje_final"
]

nombres_columnas = [
    "cancion", "Tempo (BPM)", "Energía", "Brillantez (Hz)", "Contraste (dB)", "Duración (s)", "Puntaje Final"
]

df_tabla= df[columnas_tabla].copy()
df_tabla.columns = nombres_columnas

st.dataframe(
    df_tabla.style
    .background_gradient(subset=["Puntaje Final"], cmap="RdYlGn", vmin=40, vmax=100)
    .background_gradient(subset=["Tempo (BPM)"], cmap="Blues")
    .background_gradient(subset=["Energía"], cmap="Oranges")
    .background_gradient(subset=["Contraste (dB)"], cmap="Purples")
    .format({
        "Tempo": "{:.2f}",
        "Energía": "{:.2f}",
        "Brillantez": "{:.2f}",
        "Contraste": "{:.2f}",
        "Duracion": "{:.2f}",
        "Puntaje Final": "{:.2f}",
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()

#Sección 4: Detalle de puntajes por característica

st.subheader("🎯 Detalle de puntajes por característica")

columnas_pts = [
    "cancion", "puntaje_tempo", "puntaje_energia", 
    "puntaje_brillantez", "puntaje_contraste", "puntaje_final"
]

nombres_pts = [
    "cancion", "Pts. Tempo", "Pts. Energía", "Pts. Brillantez", "Pts. Contraste", "Puntaje Final"
]

df_pts = df[columnas_pts].copy()
df_pts.columns = nombres_pts
cols_pts_num = [c for c in nombres_pts if c != "cancion"]

st.dataframe(
    df_pts.style
    .background_gradient(subset=cols_pts_num, cmap="RdYlGn", vmin=40, vmax=100)
    .format("{:.2f}", subset=cols_pts_num),
    use_container_width=True,
    hide_index=True
)

st.divider()


#SECCIÓN 5: Gráficas por características (pestañas)

st.subheader("📈 Comparativa individual por característica")

tab1, tab2, tab3, tab4 = st.tabs([
    "🥁 Tempo", "⚡ Energía", "✨ Brillantez", "🎚️ Contraste"
])

with tab1:
    st.caption("Beats por minuto (BPM) — canciones más arriba = más rápidas/movidas")
    st.bar_chart(df.set_index("cancion")[["tempo"]], height=300)

with tab2:
    st.caption("Energía promedio (RMS) — valores altos = suenan más fuerte/intensas")
    st.bar_chart(df.set_index("cancion")[["energia"]], height=300)
 
with tab3:
    st.caption("Brillantez (Hz) — valores altos = más agudos/brillantes")
    st.bar_chart(df.set_index("cancion")[["brillantez"]], height=300)
 
with tab4:
    st.caption("Contraste espectral (dB) — valores altos = sonido más nítido y definido")
    st.bar_chart(df.set_index("cancion")[["contraste"]], height=300)

st.divider()

#SECCIÓN 6: Exportar CSV

st.subheader("💾 Exportar resultados")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar resultados como CSV",
    data=csv,
    file_name="resultados_analisis.csv",
    mime="text/csv",
    use_container_width=True
)