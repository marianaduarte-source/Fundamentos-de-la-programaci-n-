import gradio as gr
from google import genai #intentaremos emplear la inteligencia artificial para crear nuestra plataforma
client = genai.Client(api_key="AQ.Ab8RN6IjeVmOpA3Ncbdq0ncCG-6u_f7rx-D-OXFDmjD_h3rvpA")
import gradio as gr #importamos Gradio
import random
def generar_itinerario(destino, tipo_viaje, rango_precio, comidas, lugares_deseados, dias_viaje, transporte_elegido): # def funciona para definir nuestra propia función, la cual (en este caso) necesita el destino y el tipo de viaje.
    if destino.strip() == "":
        return "Por favor ingresa tu destino"
    if lugares_deseados.strip() == "":
        lugares_deseados = "Ninguno en específico. Elige libremente las mejores atracciones del destino que se adapten al tipo de viaje." 
    instruccion = f"""
    Actua como un backend de planificacion de viajes de elite. Tu unica tarea es generar un itinerario detallado basado en las siguientes variables del usuario:

    - Destino: {destino.upper()}
    - Tipo de viaje: {tipo_viaje}
    - Rango de presupuesto: {rango_precio}
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
    - Almuerzo: Recomendacion gastronomica alineada a {comidas} y al presupuesto {rango_precio}.
    - Tarde: Actividad detallada considerando la logistica en {transporte_elegido}.
    - Noche: Cena y experiencia nocturna sugerida.

    ---
    ## CONSEJOS Y LOGISTICA GLOBAL
    - Transporte: Consejo especifico para moverse eficientemente usando {transporte_elegido} (menciona marcas populares si aplican).
    - Presupuesto: Como optimizar costos para la categoria {rango_precio}.
    - Tip Pro: Un dato oculto o hack especifico y real para {destino}.
    """
    respuesta_ia = client.models.generate_content(model="gemini-2.5-flash", contents = instruccion)
    return respuesta_ia.text

with gr.Blocks(theme=gr.Theme.from_hub("harsh8001/minimal-orange")) as WHERV_web: #gr.Blocks indica que hay que crear un "lienzo web"
    
 with gr.Blocks(theme=gr.Theme.from_hub("harsh8001/minimal-orange")) as parcial_web: #gr.Blocks indica que hay que crear un "lienzo web"
    gr.Markdown("# WHERV?") # El símbolo "#" indica que el texto va en negrita
    gr.Markdown("PARCIAL I - Gradio")



    with gr.Row(): #estas son las filas que dividen la pantalla en dos columnas
        with gr.Column():
            caja_destino = gr.Textbox(
                label="¿A donde deseas viajar?",
                placeholder="Ej. Bahamas, Canada, Guatemala..."
            )
            menu_experiencia = gr.Dropdown(
                choices= ["Aventura y Naturaleza", "Backpacker", "Cultural e Histórico","Solo traveler", "Shopping", "Religioso", "Gastronómico", "Business", "Wellness", "Digital Nomad", "De lujo y confort", "Familiar", "Un poco de todo (Mix)"],
                label="¿Cual es tu experiecia ideal?",
                value= "Un poco de todo (Mix)"
            )
            slider_precio = gr.Slider(
                minimum = 20,
                maximum = 2500,
                step = 50,
                label = "Presupuesto estimado por dia",
                value = 150
            )
            check_comidas = gr.CheckboxGroup(
                choices = ["Desayuno", "Almuerzo", "Cena", "Snacks y Café"],
                label = "Comidas a incluir",
                value = ["Desayuno", "Almuerzo", "Cena"]
            )
            radio_dias = gr.Radio(
                choices = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                label = "Duracion de viaje (No. de dias)",
                value = 3
            )
            menu_transporte = gr.Dropdown(
                choices= ["Taxi/Uber", "Buses turísticos (hop-on hop-off)", "Tren/Metro", "Caminando"],
                label = "Medio de transporte principal",
                value = "Caminando"
            )
            caja_lugares = gr.Textbox(
                label = "Lugares específicos que deseas visitar",
                placeholder = "Ej. Torre Eiffel, MoMa, Estatua de la libertad, etc.",
                lines = 6
            )
            boton_buscar = gr.Button("Generar itinerario", variant = "primary")
        with gr.Column():
            pantalla_salida = gr.Textbox(
            label = "Tu plan de viaje sugerido",
            lines = 32,
            interactive = False #hace que solo sea de lectura
        )
# P3 - CONEXION
    boton_buscar.click(
        fn=generar_itinerario,
        inputs=[caja_destino, menu_experiencia, slider_precio, check_comidas, caja_lugares, radio_dias, menu_transporte,],
        outputs=pantalla_salida
    )
if __name__ == "__main__":
    WHERV_web.launch(share=True)
