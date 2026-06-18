n = int(input("Ingresa la cantida de productos que compraste"))
total = 0
mas_caro = 0
for i  in range (n): 
    precio = float(input(f"Indica el precio del producto {i+1}: "))
    total = round(total + precio,2)
    if precio > mas_caro:
        mas_caro = precio
if total > 500: 
    total_a_pagar = round(total* 0.9,2)
    print (f"Total: {total}")
    print (f"Total: {total_a_pagar} (con 10% de descuento: ({total*0.1,})")
else: 
    print (f"Total: {total}")
print (f"producto más caro: {mas_caro}")