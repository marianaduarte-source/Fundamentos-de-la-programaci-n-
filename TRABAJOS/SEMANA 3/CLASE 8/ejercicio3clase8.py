import random
n = int(input("¿Cuántos dados quieres tirar?"))
suma = 0
for i in range (n): 
    tiro = random.randint(1, 6) 
    print (f"Tirada {i+1}: {tiro}")
    suma = suma + tiro
    promedio = suma/n
print (f"suma total: {suma}")
print (f"promedio: {promedio}")
if promedio > 3.5: 
    print ("buena racha!")