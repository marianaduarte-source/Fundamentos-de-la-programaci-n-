import random
print( "¡Hola!, vamos a jugar un juego")
usuario = input("Elige entre piedra, papel, o tijera: ")
eleccion = random.choice(["piedra", "papel", "tijera"])
print (eleccion)
if usuario == "piedra" and eleccion == "tijera" or usuario == "papel" and eleccion == "piedra" or usuario == "tijera" and eleccion == "papel":
    print("win")
elif usuario == eleccion: 
    print ("empatamos!")
else: 
    print("lose")