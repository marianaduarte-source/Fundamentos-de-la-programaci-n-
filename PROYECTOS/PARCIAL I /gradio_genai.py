import gradio as gr
from google import genai #intentaremos emplear la inteligencia artificial para crear nuestra plataforma
import requests #Sirve para URLs; protocolos HTTP
import os #nativa de Python que permite interacción con archivos 

from dotenv import load_dotenv # Permite leer archivos de configuración oculta
from pathlib import Path # Herramienta nativa que administra rutas de carpetas. 

load_dotenv(Path(__file__).parent / ".env") 
#(Path(__file__).parent: busca el lugar en el que se localiza el documento
# / ".env": busca archivo secreto y permite hallar su contenido
llave_gemini = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=llave_gemini)
#FUNCION NO. 1 - genera itineracio con base a selecciones de usuario
def generar_itinerario(
        destino: str,
     tipo_viaje: str,
     rango_precio: float,
     comidas: list[str], # lista cadenas de texto
     dias_viaje: int,
     num_personas: int,
     transporte_elegido: str,
     lugares_deseados: str
): # def funciona para definir nuestra propia función, la cual (en este caso) necesita el destino y el tipo de viaje.
    if destino.strip() == "":
        return "Por favor ingresa tu destino"
    if lugares_deseados.strip() == "":
        lugares_deseados = "Ninguno en específico. Elige libremente las mejores atracciones del destino que se adapten al tipo de viaje." 
    
    instruccion = f"""
    Actua como un backend de planificacion de viajes de elite. Tu unica tarea es generar un itinerario detallado basado en las siguientes variables del usuario:

    - Destino: {destino.upper()}
    - Tipo de viaje: {tipo_viaje}
    - Tamaño del grupo: {num_personas} persona(s)
    - Rango de presupuesto (USD): {rango_precio}
    - Preferencias gastronomicas: {comidas}
    - Lugares de interes obligatorios: {lugares_deseados}
    - Duracion: {dias_viaje} dias
    - Medio de transporte principal: {transporte_elegido}

    RESTRICCIONES ESTRICTAS DE FORMATO:
    1. Responde UNICAMENTE con el itinerario estructurado en texto Markdown limpio.
    2. NO incluyas saludos, introducciones, ni comentarios de despedida. Ve directo al grano.
    3. Utiliza titulos claros con '##' para los dias y vinetas para las actividades.

    ESTRUCTURA DE RESPUESTA REQUERIDA:
    # PLAN DE VIAJE: {destino.upper()} ({tipo_viaje})
    
    ## ITINERARIO DIARIO (Duracion: {dias_viaje} dias)
    (Repite el siguiente bloque de forma logica para cada uno de los {dias_viaje} dias, distribuyendo los lugares obligatorios: {lugares_deseados})
    
    ### Dia X: [Titulo descriptivo del dia]
    - Manana: Actividad detallada con horas estimadas.
    - Almuerzo: Recomendacion gastronomica alineada a {comidas} y al presupuesto {rango_precio} USD.
    - Tarde: Actividad detallada considerando la logistica en {transporte_elegido}.
    - Noche: Cena y experiencia nocturna sugerida.

    ---
    ## CONSEJOS Y LOGISTICA GLOBAL
    - Transporte: Consejo especifico para moverse eficientemente usando {transporte_elegido} (menciona marcas populares si aplican).
    - Presupuesto: Como optimizar costos para la categoria {rango_precio} USD.
    - Tip Pro: Un dato oculto o hack especifico y real para {destino}.
    """
    respuesta_ia = client.models.generate_content(model="gemini-2.5-flash", contents = instruccion) #SDK (Software Developing Kit) de Google GenAI, envia solicitud de contenido
    return respuesta_ia.text
#FUNCION NO. 2 - presupuesto de viaje y plan de contingencia
def posible_presupuesto(
    precio_diario: float, 
    dias: int,
    num_personas: int
    ): 
     total_base = int(precio_diario)* dias * num_personas
     contingencia = total_base*0.15 
     total_seguro= total_base + contingencia
     return(f"Presupuesto Base (USD): {total_base} | Presupuesto con 15% de contingencia (USD): {total_seguro}") 

# FUNCION NO. 3 - traduce el presupuesto a otras tasas de cambio al igual que analiza si el presupuesto está alineado con el estilo de viaje deseado
def viabilidad_financiera(#mapa del lugar
    rango_precio:float,
    dias_viaje: int,
    tipo_viaje: str,
    moneda_destino: str,
    num_personas: int
    ):
    total_usd= int(rango_precio)*dias_viaje*num_personas
    try: #intenta hacerlo de esta manera
        url_api = "https://api.exchangerate-api.com/v4/latest/USD"
        request_servidor= requests.get(url_api)
        datos_divisas = request_servidor.json() 
        #JavaScript Object Notation; estándar universal para aplicaciones, servidores y APIs en internet para enviarse información entre sí.
        #json() permite interpretar este texto plano
        tipo_cambio = datos_divisas["rates"][moneda_destino]
        estado_conexion = "(Tasa en tiempo real)"
    except: #en dado caso de que el servidor se caiga, ejecuta esta opción. 
        tasa_respaldo = {"GTQ": 7.80, "EUR": 0.92, "MXN": 16.80, "COP": 3900.0, "GBP": 0.79} #tasas de cambio fijas
        tipo_cambio = tasa_respaldo.get(moneda_destino, 1.0) #el 1.0 sirve en caso de que no encuentre la moneda (lo que se resuelve también con el Dropdown)
        estado_conexion = "(Tasa fija de contingencia)"
    presupuesto_convertido = total_usd*tipo_cambio

    diagnostico = ""
    if tipo_viaje == "De lujo y confort" and rango_precio < 300: 
        diagnostico = "presupuesto bajo para categoría seleccionada"
    elif tipo_viaje == "Backpacker" and rango_precio > 100: 
        diagnostico = "Presupuesto holgado para viaje, Altamente factible"
    else:
        diagnostico = "Equilibrado, presupuesto viable para experiencia"
    resultado = f"""
    ANÁLISIS FINANCIERO DE VIAJE: 
    - Inversión total (Base USD): ${total_usd:,.2f} USD
    - Equivalencia en {moneda_destino}: {presupuesto_convertido:,.2f} {moneda_destino} {estado_conexion}
    - Diagnostico: {diagnostico}
    """
    return resultado
#FUNCION NO. 4 - Abre una ventana web dentro del sitio para ver Google Maps; establece formato en HTML para su visualización
def actualizar_mapa(destino: str):#funcion que permite buscar imagenes del lugar seleccionado
    if not destino or destino.strip() == "":
        return "<div>Ingrese un destino para ver el mapa</div>" #<div>: estructura web; crean un contenedor o bloque vacío. También permiten agregar estilo
    destino_format = destino.replace(",","").replace(" ","+")
    html_mapa = f"""
    <iframe 
    width="100%"
    height="350"
    src="https://www.google.com/maps?q={destino_format}&output=embed"
    frameborder="0"
    style="border:0; border-radius:10px;"
    allowfullscreen>
    </iframe>
    """
    return html_mapa
#FUNCION NO. 5 - Busca imagenes relacionadas al destino 
def imagenes(destino:str):
    if not destino or destino.strip() == "":
        return[
            "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600",
            "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=600"
        ]
    destino_format = destino.replace(",","").replace(" ","+")
    imagenes_html=[
        f"https://loremflickr.com/600/450/{destino_format},skyline/all",
        f"https://loremflickr.com/600/450/{destino_format},monument/all",
        f"https://loremflickr.com/600/450/{destino_format},hotel/all"
    ]
    return imagenes_html
with gr.Blocks(theme=gr.Theme.from_hub("harsh8001/minimal-orange")) as WHERV_web: #gr.Blocks indica que hay que crear un "lienzo web"
    gr.Markdown("# WHERV?") # El símbolo "#" indica que el texto va en negrita
    gr.Markdown("PARCIAL I - Gradio")
#ESTOS ELEMENTOS DE GRADIO SUELEN TENER: 
# label: El nombre de dicho objeto
# value: un valor preestablecido
#choices: lista de opciones (para aquellos que ya tienen opciones definidas)
    with gr.Row(): #estas son las filas 
        with gr.Column(): #la pantalla se divide en dos columnas - COLUMNA NO. 1
         #caja de texto que permite escribir lugar
            caja_destino = gr.Textbox( 
                
                label="¿A donde deseas viajar?",
                placeholder="Ej. Bahamas, Canada, Guatemala..."
            )
         #Permite establecer opciones fijas edl tipo de experiencia
            menu_experiencia = gr.Dropdown(
               
                choices= ["Aventura y Naturaleza", "Backpacker", "Cultural e Histórico","Solo traveler", "Shopping", "Religioso", "Gastronómico", "Business", "Wellness", "Digital Nomad", "De lujo y confort", "Familiar", "Un poco de todo (Mix)"],
                label="¿Cual es tu experiecia ideal?",
                value= "Un poco de todo (Mix)"
            )
        #permite arrastrar mouse para elegir un precio 
            slider_precio = gr.Slider(
                minimum = 10,
                maximum = 2500,
                step = 50,
                label = "Presupuesto estimado por dia (USD) por persona",
                value = 150
            )
        #Da opciones a incluir de las comidas que se desean hacer
            check_comidas = gr.CheckboxGroup(
                choices = ["Desayuno", "Almuerzo", "Cena", "Snacks y Café"],
                label = "Comidas a incluir",
                value = ["Desayuno", "Almuerzo", "Cena"]
            )
        # Números enteros de días que se desea viajar
            radio_dias = gr.Radio(
                choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                label = "Duracion de viaje (No. de dias)",
                value = 3
            )
        #Integrantes del viaje
            slider_personas = gr.Slider(
                minimum=1,
                maximum=10,
                step=1,
                label="No. de personas",
                value=1
            )
        # Opciones a tomar como medio de transporte 
            menu_transporte = gr.Dropdown(
                choices= ["Taxi/Uber", "Buses turísticos (hop-on hop-off)", "Tren/Metro", "Caminando"],
                label = "Medio de transporte principal",
                value = "Caminando"
            )
        # Permite al usuario elegir lugares que hayan captado su interés y que desea visitar
            caja_lugares = gr.Textbox(
                label = "Lugares específicos que deseas visitar",
                placeholder = "Ej. Torre Eiffel, MoMa, Estatua de la libertad, etc.",
                lines = 6
            )
           
            boton_buscar = gr.Button("Generar itinerario", variant = "primary")
            # ANALISIS FINANCIERO
            
        with gr.Column(): #COLUMNA NO. 2
        #Área en la que el texto generado por Gemini aparecerá
            pantalla_salida = gr.Textbox(
            label = "Tu plan de viaje sugerido",
            lines = 22,
            interactive = False #hace que solo sea de lectura
            )
        #Las imágenes que hemos buscado con la función
            galeria_imagenes = gr.Gallery(
                label = "fotos del destino",
                columns = 3,
                height = "auto",
                object_fit="cover"
            )
    with gr.Row():  #FILA NO. 2 DE SITIO
        visor_mapa=gr.HTML() #Area dentro del sitio que solo comprende HTML, CSS, JavaScript. renderiza la pantalla
    gr.Markdown("---")
    gr.Markdown("ANALISIS FINANCIERO Y VIABILIDAD")
    with gr.Row(): # FILA NO. 3
        with gr.Column(scale=1):       #scale=1 --> proporción relativa a otras columnas que opcupará
        # TEXTO FUNCION 2
            salida_presupuesto_base= gr.Textbox(
                label= "Proyección de Fondos Base",
                lines = 2,
                interactive = False,
                placeholder = """El presupuesto será generado siempre y cuando el rango de precio esté alineado con la opción seleciconada"""
            )
        #Permite elegir una moneda para realizar el cambio 
            menu_moneda = gr.Dropdown(
                choices = ["GTQ", "EUR", "MXN", "COP", "GBP"],
                label = "Moneda para diagnóstico",
                value = "GTQ"
            )
        with gr.Column(scale=2):  
        # TEXTO FUNCION 3
            salida_finanzas = gr.Textbox(
                label= "Diagnóstico de presupuesto",
                lines = 5,
                interactive = False, 
            )
# P3 - CONEXION
    boton_buscar.click(
        #listener 
        fn=generar_itinerario, #funcion a activar
        inputs=[
                caja_destino, #destino: str,
                menu_experiencia, #tipo_viaje: str,
                slider_precio, #rango_precio: float,
                check_comidas, #comidas: list[str],# lista cadenas de texto
                radio_dias, #dias_viaje: int,
                slider_personas,#num_personas: int,
                menu_transporte,#transporte_elegido: str,
                caja_lugares],#lugares_deseados: str
        outputs=pantalla_salida
    )
#.click(): hace que cuando el usuario presione el boton, se activen dichas funciones
    boton_buscar.click(
        fn=imagenes,
        inputs=caja_destino,
        outputs=galeria_imagenes
    )
    boton_buscar.click(
            fn=actualizar_mapa,
            inputs=caja_destino,
            outputs=visor_mapa
        )
    # .change hace que todas las funciones se activen cuando estos datos cmabien
    slider_precio.change(
        fn=posible_presupuesto,
        inputs= [slider_precio, radio_dias, slider_personas],
        outputs = salida_presupuesto_base)
    slider_personas.change(
        fn=posible_presupuesto,
        inputs=[slider_precio, radio_dias, slider_personas],
        outputs=salida_presupuesto_base
    )
    slider_precio.change(
        fn=viabilidad_financiera,
        inputs=[slider_precio, radio_dias, menu_experiencia, menu_moneda, slider_personas],
        outputs=salida_finanzas
    )
    radio_dias.change(
        fn= viabilidad_financiera,
        inputs= [slider_precio, radio_dias, menu_experiencia, menu_moneda, slider_personas], 
        outputs= salida_finanzas
    )
    menu_experiencia.change(
        fn=viabilidad_financiera,
        inputs=[slider_precio, radio_dias, menu_experiencia, menu_moneda, slider_personas],
        outputs= salida_finanzas
    )
    menu_moneda.change(
        fn=viabilidad_financiera,
        inputs=[slider_precio, radio_dias, menu_experiencia, menu_moneda, slider_personas], 
        outputs=salida_finanzas
    )
    slider_personas.change(
        fn=viabilidad_financiera,
        inputs=[slider_precio, radio_dias, menu_experiencia, menu_moneda, slider_personas],
        outputs=salida_finanzas
    )
    #Esto es todo lo que sucede cuando la web carga
    #A falta de datos, estos se van a los que están por defecto
    WHERV_web.load(
        fn=actualizar_mapa,
        inputs=caja_destino,
        outputs=visor_mapa
        )
    WHERV_web.load(
        fn=imagenes,
        inputs=caja_destino,
        outputs=galeria_imagenes
        )
    WHERV_web.load(
        fn=posible_presupuesto,
        inputs=[slider_precio, radio_dias, slider_personas],
        outputs=salida_presupuesto_base
        )
    WHERV_web.load(
        fn=viabilidad_financiera,
        inputs=[slider_precio, radio_dias, menu_experiencia, menu_moneda, slider_personas],
        outputs=salida_finanzas
        )
if __name__ == "__main__": #condiciona a que si este se está ejecutando como el programa principal, se ejecutará el resto
    WHERV_web.launch(share=True)