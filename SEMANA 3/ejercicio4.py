import random
print( "¡Hola!, vamos a jugar un juego")
usuario = input("Elige entre piedra, papel, o tijera: ")
eleccion = random.choice(["piedra", "papel", "tijera"])

if usuario == "piedra" and eleccion == "tijera":
    print("Ganaste!")
elif   usuario == "papel" and eleccion == "piedra":
    print("Ganaste!")
elif   usuario == "tijera" and eleccion == "papel": 
    print("Ganaste!")  
elif usuario == eleccion: 
    print ("empatamos!")
else: 
    print ("Perdiste :(")
print("La PC eligio: ", eleccion)
print ("Gracias por jugar!")
