print("Hola usuario, te solicitaremos los siguientes datos para que clasifiquemos tu triángulo")
A=int(input("Ingresa el valor del lado A: "))
B=int(input("ingresa el valor del lado B: "))
C=int(input("Ingresa el valor del lado C: "))

if A==B and B==C: 
    print("El triángulo es equilátero)")
elif A==B or B==C or A==C:
    print("El triángulo es isósceles)")
else:
    print("El triángulo es escaleno)")