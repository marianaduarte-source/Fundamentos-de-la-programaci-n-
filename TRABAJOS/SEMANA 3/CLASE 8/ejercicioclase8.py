n = int(input("Ingresa una cifra del 1 al 10"))
for i in range (1, 11):
    resultado= n*i
    if resultado >= 30 and resultado % 2 == 0:
        print (f"{n} x{i} = {resultado}" + "←grande, par") 
    elif resultado >= 30 and not resultado % 2 == 0:
        print (f"{n} x{i} = {resultado}" + "←grande")
    elif resultado < 30 and resultado % 2 == 0: 
        print (f"{n} x{i} = {resultado}" + "←par")
    else: 
        print (f"{n} x{i} = {resultado}") 