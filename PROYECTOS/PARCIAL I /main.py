import gradio as gr #importamos Gradio
import random
def generar_itinerario(destino, tipo_viaje): # def funciona para definir nuestra propia función, la cual (en este caso) necesita el destino y el tipo de viaje.
    if destino == "":
        return "Por favor ingresa tu destino" #
    if tipo_viaje == "Aventura y Naturaleza": 
        # OPCIÓN 1 DE VIAJE "Aventura y Naturaleza"
        itinerario = f"""
        ITINERARIO DE {tipo_viaje.upper()} PARA {destino.upper()}
        • 07:00 AM - Salida hacia senderos naturales.
        • 09:00 AM - Caminata extrema y ascenso guiado.
        • 01:00 PM - Almuerzo de campo al aire libre.
        • 06:00 PM - Regreso al punto de partida.
        """
        return itinerario
    #OPCIÓN 2 DE VIAJE "Cultura e Historia"
    elif tipo_viaje == "Cultural e Histórico": 
        itinerario = f"""
         ITINERARIO DE {tipo_viaje.upper()} PARA {destino.upper()}
        • 09:00 AM - Visita guiada a museos y monumentos históricos.
        • 01:00 PM - Almuerzo en restaurante de comida típica tradicional.
        • 03:00 PM - Recorrido por plazas coloniales y mercados de artesanías.
        """
        return itinerario
    #OPCIÓN 3 DE VIAJE "Gastronomía"
    elif tipo_viaje == "Gastronómico": 
         itinerario = f"""
          ITINERARIO DE {tipo_viaje.upper()} PARA {destino.upper()}
        • 08:30 AM - Desayuno típico en el mercado local.
        • 11:00 AM - Tour guiado para conocer la preparación de café o chocolate.
        • 02:00 PM - Almuerzo de degustación con platillos de la región.
        """
         return itinerario
    #CASO FINAL, opción de caso mixta
    elif tipo_viaje == "Un poco de todo (Mix)":
         itinerario = f"""
         ITINERARIO DE {tipo_viaje.upper()} PARA {destino.upper()}
        • 08:00 AM - Desayuno tradicional ligero en el centro histórico.
        • 09:30 AM - Caminata guiada y exploración de la naturaleza local.
        • 01:00 PM - Almuerzo típico de degustación (¡Lo mejor de la región!).
        • 03:00 PM - Recorrido cultural por museos, plazas y tiendas artesanales.
        • 06:00 PM - Café de especialidad y cierre del día.
        """
         return itinerario
    else: 
        return "Opción de viaje no identificada. Por favor seleccionar alguna de las opciones en el menú"

#PARTE VISUAL (GRADIO)

with gr.Blocks(theme=gr.Theme.from_hub("harsh8001/minimal-orange")) as parcial_web: #gr.Blocks indica que hay que crear un "lienzo web"
    gr.Markdown("# ITINERARY!") # El símbolo "#" indica que el texto va en negrita
    gr.Markdown("PARCIAL I - Gradio")
    with gr.Row(): #estas son las filas que dividen la pantalla en dos columnas
        with gr.Column():
            caja_destino = gr.Textbox(
                label="¿A donde deseas viajar?",
                placeholder="Ej. Bahamas, Canada, Guatemala..."
        )
            menu_experiencia = gr.Dropdown(
                choices= ["Aventura y Naturaleza", "Cultural e Histórico","Gastronómico", "Un poco de todo (Mix)"],
                label="¿Cual es tu experiecia ideal?",
                value= "Un poco de todo (Mix)"
         )
            boton_buscar = gr.Button("Generar itinerario", variant = "primary")
        with gr.Column():
            pantalla_salida = gr.Textbox(
            label = "Tu plan de viaje sugerido",
            lines = 12,
            interactive = False #hace que solo sea de lectura
        )
# P3 - CONEXION
    boton_buscar.click(
        fn=generar_itinerario,
        inputs=[caja_destino, menu_experiencia],
        outputs=pantalla_salida
    )
if __name__ == "__main__":
    parcial_web.launch()
