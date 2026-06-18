saldo = 1000
seguir = True
while seguir: 
    opcion = int(input("Elige una opcion (1: ver saldo, 2: depositar, 3: retirar, 4: terminar transacciones)")
    )
    if opcion == 1: 
        print (f"saldo: {saldo}" )
    elif opcion == 2: 
        monto_dep = int(input("¿Cuanto deseas depositar?"))
        total = saldo + monto_dep
        print (f"deposito: {total}")
        saldo = total
    elif opcion == 3: 
        monto_ret = int(input("¿Cuanto deseas retirar?"))
        if monto_ret < saldo:
            total = saldo - monto_ret
            print (f"retiro: {total}")
            saldo = total 
            
        else: 
            print(f"Saldo insuficiente")
            saldo = saldo  
    else: 
        seguir = False
        print("Gracias, retire la tarjeta")

