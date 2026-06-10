#sistema de acceso
#si es mayor de 18 anios, puede entrar; si tiene entre 15 y 17, debe ingresar con un adulto y si tiene menos de 15 anios, no puede entrar
edad = int(input("Ingresa por favor tu edad: ")) # int input para que usuario ingrese su edad
nombre = input ("¿Cómo te llamas?")

if edad >=18: 
    print("Bienvenido", nombre + ", puedes entrar al establecimiento") # esto se ejecuta si la persona e smayor de edad. 
elif edad >=15 and edad <17:
    print("Hola", nombre + ", puedes entrar al establecimiento pero debes ingresar con un adulto") # esto se ejecuta si la persona tiene entre 15 y 17 anios
else:
    print("Lo lamento", nombre + ", no puedes entrar al establecimieto")
