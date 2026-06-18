import random
seguir = True
while seguir: 
    resultado = random.choice(["cara", "escudo"])
    print(f"salió {resultado}")
    respuesta = input("otra? (s/n)")
    if respuesta == "s":
        seguir = True
    else:
        print("Gracias por jugar")
        seguir = False