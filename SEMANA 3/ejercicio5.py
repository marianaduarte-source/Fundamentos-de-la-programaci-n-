import random
print("hola usuario, juguemos un juego de adivinanda!")
numero = int(input("Elije un número del 1 al 5: "))
aleatorio = random.randint(1, 5)

if numero > aleatorio: 
    print("El número es más pequeño")
elif numero < aleatorio:
    print("El número es más pequeño")
else: 
    print("Felicidades, lo adivinaste 😃")
print("El número aleatorio era: ", aleatorio)