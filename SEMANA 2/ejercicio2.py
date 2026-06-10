temperatura=float(input("Temperatura en Celsius: "))
if temperatura >46.8:
    print("Temperatura fuera de rango, Guatemala no ha registrado temperaturas tan altas")
elif temperatura >30 and temperatura <=46.8: 
    print("Hace calor, toma agua")
elif temperatura >=15 and temperatura <=30: 
    print("CLIMA AGRADABLE")
elif temperatura >=-12 and temperatura <15:
    print("Hace fío, abrígate")
else: 
    print("Temperatura fuera de rango")
    print("Históricamente, Guatemala ha registrado temperaturas mínimas de -12 °C y máximas de 30 °C")
print( "Temperatura registrada: " + str(temperatura) + " °C")
