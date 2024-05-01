from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
import json

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color+"*"*90+reset_color)
        gotoxy(15,2);print(blue_color+Company.get_business_name())
        gotoxy(27,3);print(blue_color+"Registro de Cliente")
        print("-" * 90)
        print(purple_color+"Seleccione el tipo de cliente:")
        print("1. Cliente Regular")
        print("2. Cliente VIP")
        print("-" * 90)
        tipo_cliente = input("Seleccione una opción: ")
        borrarPantalla()
        
        array_datos_clients = ["Ingrese el nombre del cliente: ","Ingrese el apellido del cliente: ","Ingrese el DNI del cliente: "] 
        print("-" * 90)
        if tipo_cliente == "1":
            gotoxy(15,2);print("Cliente Regular")
            print()
            for dato in array_datos_clients:
                print(dato)
            print("¿El cliente tiene tarjeta de descuento? (s/n): ")
            gotoxy(32,3);nombre = input() 
            gotoxy(34,4);apellido = input()
            gotoxy(30,5);dni = str(input())
            gotoxy(48,6);card = input()
            json_file = JsonFile(path +'/archivos/clients.json')
            clients = json_file.read()
            found_dni = json_file.find('dni',dni)
            if found_dni:
                print()
                gotoxy(15,5);print('Ya existe un cliente registrado con ese DNI')
                time.sleep(3)
                return
            
            new_client = RegularClient(nombre, apellido, dni, card)
            clients.append(new_client.getJson())
            json_file.save(clients)
            print()
            gotoxy(15,15);print("Cliente registrado exitosamente!")
            time.sleep(3)

        elif tipo_cliente == "2":
            gotoxy(15,2); print("Cliente VIP")
            print()
            for dato in array_datos_clients:
                print(dato)
            gotoxy(32,4);nombre = input()
            gotoxy(34,5);apellido = input()
            gotoxy(30,6);dni = str(input())
            json_file = JsonFile(path +'/archivos/clients.json')
            clients = json_file.read()
            found_dni = json_file.find('dni',dni)
         
            if found_dni:
                gotoxy(15,5);print('Ya existe un cliente registrado con ese DNI')
                time.sleep(3)
            else:
                new_client = VipClient(nombre, apellido, dni)
                clients.append(new_client.getJson())
                json_file.save(clients)
                gotoxy(15,5);print("Cliente registrado exitosamente!")
                time.sleep(3)
            new_client = VipClient(nombre, apellido, dni)
        else:
            gotoxy(15,5);print("Opción inválida")
            time.sleep(4)
            return
    
    def update(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        gotoxy(15,2);print(blue_color + Company.get_business_name())
        gotoxy(27,3);print(blue_color + "Actualización de Cliente")
        print("-" * 90)

        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        dni = input('Ingrese DNI: ')
        found_dni = json_file.find('dni', dni)
        if found_dni:
            for client in found_dni:
                print(f'Su cliente es: {client["nombre"]} {client["apellido"]}')
                print(f'Descuento: {client["valor"]}')
                print("-" * 90)

            print('Que desea actualizar?')
            print('1. Cambiar el nombre del Cliente')
            print('2. Cambiar el apellido del Cliente')

            opcion = input('Elija una opcion: ')
            print("-" * 90)

            borrarPantalla()
            print("-" * 90)
            if opcion == "1":
                gotoxy(15,2);print('Cambio de nombre')
                new_name = input('Ingrese el nuevo nombre de su cliente: ')
                found_dni[0]['nombre'] = new_name
                # Reemplazar el cliente antiguo con el cliente modificado en la lista de clientes
                clients = [found_dni[0] if client['dni'] == dni else client for client in clients]
                json_file.save(clients)
                gotoxy(10,12);print('Se cambio el nombre con existo!')
                print("-" * 90)
                time.sleep(4)
                
            elif opcion == "2":
                gotoxy(15,2);print('Cambio de Apellido')
                new_lastname = input('Ingrese el nuevo apellido de su cliente: ')
                found_dni[0]['apellido'] = new_lastname
                # Reemplazar el cliente antiguo con el cliente modificado en la lista de clientes
                clients = [found_dni[0] if client['dni'] == dni else client for client in clients]
                json_file.save(clients)
                gotoxy(10,12);print('Se cambio el apellido con existo!')
                print("-" * 90)
                time.sleep(4)
            else:
                print('Opcion invalida')
                time.sleep(3)
                return
        else:
            print('DNI no existe')
            print("-" * 90)
            time.sleep(4)


    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color+"*"*90+reset_color)
        gotoxy(15,2);print(blue_color+Company.get_business_name())
        gotoxy(27,3);print(blue_color+"Eliminar Cliente")
        print("-" * 90)
        print()
        dni = input("Ingrese el DNI del cliente que desea eliminar: ")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()

        found_dni = json_file.find('dni',dni)

        if found_dni:
            for client in found_dni:
                print(f'Su cliente es: {client["nombre"]} {client["apellido"]}')
                print("-" * 90)
            opcion = input('Esta seguro de eliminar a su cliente? (s/n): ').lower()
            if opcion == "s":
                clients.remove(found_dni[0]) 
                json_file.save(clients)  
                gotoxy(15,5);print("El cliente ha sido eliminado correctamente.")
                time.sleep(3)
            else:
                gotoxy(15,5);print("Operación cancelada...")
                time.sleep(3)
                return
        else:
            gotoxy(15,5);print("No se encontró ningún cliente con el DNI proporcionado.")
            time.sleep(3)

    
    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(15,2);print(blue_color+Company.get_business_name())
        gotoxy(2,1);print(green_color+"*"*90)
        gotoxy(27,3);print("Consulta de Cliente")
        print("-" * 90) 
        gotoxy(1,);dni = input('Ingrese DNI del cliente: ')
        
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.find("dni", dni)

        if clients:
            print("-" * 90) 
            for client in clients:
                print(f'Nombre: {client["nombre"]}')
                print(f'Apellido: {client["apellido"]}')
                print(f'Descuento: {client["valor"]}')
                print("-" * 90) 
            time.sleep(3)
        else:
            gotoxy(15,6);print("Cliente no encontrado.")
            time.sleep(3)
        print()
        gotoxy(15,6);input("Presione una tecla para continuar...")  
         

class CrudProducts(ICrud):
    def create(self):
        borrarPantalla()
        gotoxy(15,1);print(blue_color + Company.get_business_name())
        gotoxy(25,2);print(blue_color + "Registro de Productos")
        print(blue_color+"-"*90 + reset_color)

        gotoxy(1,4); print('Ingrese el producto: ')
        gotoxy(1,5); print('Ingrese el precio del producto:')
        gotoxy(1,6); print('Ingrese el stock del producto:')

        gotoxy(22,4); descripcion = input()
        gotoxy(33,5); preci = float(input())
        gotoxy(32,6); stock = int(input())

        # Obtener el último ID almacenado en el archivo JSON
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()
        last_id = products[-1]["id"] + 1

        # Incrementar el ID para el nuevo producto
        new_product = Product(last_id, descripcion, preci, stock)

        # Verificar si ya existe un producto con la misma descripción
        buscar_producto = json_file.find('descripcion',descripcion)

        if buscar_producto:
            gotoxy(35,22); print(f'El producto {descripcion} ya esta registrado.')
            time.sleep(3)
            return
        else:
            products.append(new_product.getJson())
            json_file.save(products)
            gotoxy(30,25);print('El producto se ha registrado con exito!')
            time.sleep(4)



    def update(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        gotoxy(15,2);print(green_color + Company.get_business_name())
        gotoxy(27,3);print(green_color + "Actualizar productos")
        print("-" * 90)
        print()

        id = int(input('Ingrese el ID del producto que va a actualizar: '))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        found_product = None
        for product in products:
            if product['id'] == id:
                found_product = product
                break

        if found_product:
            print(f'Producto: {found_product["id"]}')
            print(f'Producto: {found_product["descripcion"]}')
            print(f'Precio: {found_product["precio"]}')
            print(f'Stock: {found_product["stock"]}')
            print("-" * 90) 
        
            print('Qué va a actualizar?')
            print('1. Nombre del producto.')
            print('2. precio del producto.')
            print('3. Stock del producto.')
            print()
            opcion = input('Elija una opción: ')
            print("-" * 90)

            if opcion == "1":
                new_name = input('Ingrese el nuevo nombre del producto: ')
                existing_product = next((prod for prod in products if prod['descripcion'].lower() == new_name.lower() and prod['id'] != id), None)
                if existing_product:
                    gotoxy(15,4);print(f"Este producto ya existe con el ID {existing_product['id']}.")
                else:
                    found_product['descripcion'] = new_name
            elif opcion == "2":
                new_preci = input('Ingrese el nuevo precio del producto: ')
                found_product['precio'] = float(new_preci)
            elif opcion == "3":
                new_stock = input('Ingrese el nuevo stock del producto: ')
                found_product['stock'] = int(new_stock)

            # Guardar los cambios en el archivo JSON
            json_file.save(products)
            gotoxy(15,4);print("Producto actualizado exitosamente!")
        else:
            gotoxy(15,4);print("Producto no encontrado.")
        time.sleep(3)

    
    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        print(blue_color + "Eliminar productos productos")
        print(blue_color + Company.get_business_name())

        id = int(input('Ingrese el ID del producto desea eliminar: '))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()
        
        found_product = None
        for product in products:
            if product['id'] == id:
                found_product = product
                products.remove(product)

        
        if found_product:
            print(f"Su producto es: {found_product}")
            respuesta = input('Esta seguro de eliminar este producto? (s/n): ').lower()
            if respuesta == 's':
                
                print('Se elimino su producto')
                for i, product in enumerate(products):
                    product['id'] = i + 1
                
                json_file.save(products)
            
                print('Se actualizaron los ID de los productos')
                time.sleep(3)
            else:
                print('Cancelando eliminacion...')
                time.sleep(3)
        else:
            print('Producto no encontrado')
            time.sleep(3)
                
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Productos"+" "*35+"██")
        gotoxy(2,4);id = int(input("Ingrese ID del producto: "))
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.find("id", id)
        
        if products:
            for product in products:
                print("-" * 30)
                print(f'ID: {product["id"]}')
                print(f'Descripcion: {product["descripcion"]}')
                print(f'Precio: {product["precio"]}')
                print(f'Stock: {product["stock"]}')
                print("-" * 30)
                
            time.sleep(3)
        else:
            print("Producto no encontrado.")
            time.sleep(3)
        input("Presione una tecla para continuar...")   

class CrudSales(ICrud):
    def create(self):
        validar = Valida()
        borrarPantalla()

        print('\033c', end='')  # Limpia la pantalla

        # Imprime la cabecera de la venta
        gotoxy(1, 1);print(green_color + "*" * 90 + reset_color)
        gotoxy(1, 2);print(blue_color + "Registro de Venta")
        gotoxy(1, 3);print(blue_color + Company.get_business_name())
        gotoxy(1, 4);print(f"Factura#: F0999999 {' ' * 3} Fecha: {datetime.datetime.now()}")
       
        gotoxy(1, 6);print("Subtotal:")
        gotoxy(1, 7);print("Descuento:")
        gotoxy(1, 8);print("Iva     :")
        gotoxy(1, 9);print("Total   :")
        gotoxy(1,10); print("Cedula :")


        dni = validar.solo_numeros("Error: Solo números", 10, 8)  # Solicita el número de cédula del cliente
        
        json_file = JsonFile(path +'/archivos/clients.json')

        client = json_file.find("dni", dni)  # Busca al cliente por su número de cédula
        
        if not client:
            gotoxy(1, 10);print("Cliente no existe")
            time.sleep(3)
            return
        client = client[0]

        cli = RegularClient(client["nombre"], client["apellido"], client["dni"],card=True)  # Crea un cliente RegularClient

        sale = Sale(cli)  # Crea una venta asociada al cliente

        print(cli.fullName())
        gotoxy(1, 11);print(green_color + "*" * 90 + reset_color)
        gotoxy(1, 12);print(purple_color + "Linea ", " Id_Articulo ", "   Descripción   ", " Precio " ," Cantidad ", " Subtotal ")
        gotoxy(1, 13);print(reset_color + "-" * 90)

        # Detalle de la venta
        follow = "s"
        line = 1

        while follow.lower() == "s":
            gotoxy(1, 14); print(f"{line}", end="   ")
            id = validar.solo_numeros("Error: Solo números", 13, 13)  # Solicita el ID del producto
            id=int(id)
            
            json_file = JsonFile( path+ '/archivos/products.json')

            prods = json_file.find("id", id)  # Busca el producto por su ID

            if not prods:
                gotoxy(1, 15);print("Producto no existe")
                
                time.sleep(3)
                break
            else:
                prods = prods[0]
                product = Product(prods["id"], prods["descripcion"], prods["precio"],prods["stock"])  # Crea un producto en la factura

                gotoxy(26,9);print(product.descrip)
                gotoxy(42,9); print(product.preci)
                qyt = int(validar.solo_numeros("Error: Solo números", 53, 9))  # Solicita la cantidad de producto

                if qyt > product.stock:
                    gotoxy(1, 15);print(f"El producto solo tiene un stock de {product.stock} ")
                    respuesta = input('Desea llevar esa cantidad? (s/n): ').lower()
                    if respuesta == 's':
                        qyt = product.stock  # Actualiza la cantidad a la disponible en stock
                        new_subtotal = product.preci * qyt  # Calcula el nuevo subtotal
                        gotoxy(53, 7); print(qyt)  # Imprime la nueva cantidad
                        gotoxy(63, 7); print(new_subtotal)  # Imprime el nuevo subtotal
                        time.sleep(3)
                        
                        sale.add_detail(product, qyt)
                        break
                        
                    else:
                        subtotal = product.preci * qyt
                        gotoxy(63,9);print(subtotal)
                        sale.add_detail(product, qyt)  # Agrega el detalle de la venta
                else:
                    subtotal = product.preci * qyt
                    gotoxy(63,9);print(subtotal)
                    sale.add_detail(product, qyt)
                    follow = input("¿Desea agregar otro producto? (s/n): ").lower()
                    if follow == "s":
                        print(green_color + "✔" + reset_color)
                        line += 1
                    else:

                        print(f"Subtotal: {round(sale.subtotal, 2)}")
                        print(f"Descuento: {round(sale.discount, 2)}")
                        print(f"Iva     : {round(sale.iva, 2)}")
                        print(f"Total   : {round(sale.total, 2)}")

        print(red_color + "¿Está seguro de grabar la venta? (s/n): ", end='')
        procesar = input().lower()  # Pregunta si se quiere grabar la venta
        if procesar == "s":
            print("😊 Venta Grabada satisfactoriamente 😊" + reset_color)
            json_file = JsonFile(path  + '/archivos/invoices.json')
            invoices = json_file.read()
            if invoices:
                ult_invoices = invoices[-1]["factura"] + 1
            else:
                ult_invoices = 1
            archivos = sale.getJson()
            archivos["factura"] = ult_invoices
            invoices.append(archivos)
            json_file = JsonFile(path  + '/archivos/invoices.json')
            json_file.save(invoices)
        else:
            print("🤣 Venta Cancelada 🤣" + reset_color)
        time.sleep(3)

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')

        json_file_invoices_archivos = JsonFile(path  + '/archivos/invoices.json')
        invoices = json_file_invoices_archivos.read()

        # Mostrar las facturas disponibles
        opciones = [f"{factura['factura']}) Factura: #{factura['factura']}" for factura in invoices]
        menu_factura = Menu("Menu Facturas", opciones, 20, 10)
        print("Seleccione la factura que desea modificar:")
        selected_invoice_str = menu_factura.menu()

        # Obtener el número de factura seleccionada
        selected_invoice_num = int(selected_invoice_str)

        # Buscar la factura seleccionada
        selected_invoice_index = None

        for index, factura in enumerate(invoices):
            if factura['factura'] == selected_invoice_num:
                selected_invoice_index = index
                break

        if selected_invoice_index is not None:
            # Mostrar detalles de la factura seleccionada
            selected_invoice = invoices[selected_invoice_index]
            print("Factura:", selected_invoice['factura'])
            print("Fecha:", selected_invoice['Fecha'])
            print("Cliente:", selected_invoice['cliente'])
            print("Subtotal:", selected_invoice['subtotal'])
            print("Descuento:", selected_invoice['descuento'])
            print("IVA:", selected_invoice['iva'])
            print("Total:", selected_invoice['total'])
            print("Detalles:")
            for detalle in selected_invoice['detalle']:
                print("\tProducto:", detalle['poducto'])
                print("\tpreci:", detalle['precio'])
                print("\tCantidad:", detalle['cantidad'])
            print()

            # Permitir al usuario seleccionar qué desea modificar
            menu_update = Menu("¿Qué opción desea modificar?", ["1) Cliente", "2) Detalles", "3) Todo"], 20, 10)

            selected_update = menu_update.menu()

            if selected_update == "1":

                print("Ingrese el numero de cédula del cliente:", end=" ")

                gotoxy(5,5);dni = int(input())  # Solicita el número de cédula del cliente
               

                json_file_client_archivos = JsonFile(path  + '/archivos/clients.json')

                client = json_file_client_archivos.find("dni", dni)  # Busca al cliente por su número de cédula

                if not client:
                    print("Cliente no existe")
                    time.sleep(3)
                    return

                client = client[0]

                cli = RegularClient(client["nombre"], client["apellido"], client["dni"],card=True)  # Crea un cliente RegularClient

                sale = Sale(cli)

                json_file = JsonFile(path + '/archivos/products.json')

                products = []

                for detalle in selected_invoice['detalle']:
                    prods_by_descrip = json_file.find('descripcion', detalle['poducto'])
                    products.append(prods_by_descrip[0]['id'])

                for i, product in enumerate(products):
                    print()

                    prods = json_file.find("id", product)  # Busca el producto por su ID

                    if not prods:
                        print("Producto no existe")
                        time.sleep(3)
                    else:
                        prods = prods[0]

                        product = Product(prods["id"], prods["descrip"], prods["preci"], prods["stock"])  # Crea un producto

                        print(product.descrip, str(product.preci), end=' ')

                        product_quantity = selected_invoice['detalle'][i]['cantidad']  # Solicita la cantidad de producto

                        subtotal = product.preci * product_quantity

                        print(str(product_quantity), subtotal)

                        sale.add_detail(product, product_quantity)  # Agrega el detalle de la venta

                        print(f"Subtotal: {round(sale.subtotal, 2)}")

                        print(f"Descuento: {round(sale.discount, 2)}")

                        print(f"Iva     : {round(sale.iva, 2)}")

                        print(f"Total   : {round(sale.total, 2)}")

                print(red_color + "¿Está seguro de actualizar el cliente? (s/n): ", end='')

                procesar = input().lower()  # Pregunta si se quiere grabar la venta
                if procesar == "s":
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    archivos = sale.getJson()
                    archivos["factura"] = selected_invoice['factura']
                    invoices[selected_invoice_index] = archivos
                    json_file = JsonFile(path  + '/archivos/invoices.json')
                    json_file.save(invoices)
                else:
                    print("🤣 Actualización Cancelada 🤣" + reset_color)
                time.sleep(2)

            elif selected_update == "2":

                json_file_client_archivos = JsonFile(path  + '/archivos/clients.json')

                cliente = selected_invoice['cliente']
                primera_palabra = cliente.split()[0]

                client = json_file_client_archivos.find("nombre", primera_palabra)  # Busca al cliente por su número de cédula

                if not client:
                    print("Cliente no existe")
                    return

                print(cliente)

                client = client[0]

                cli = RegularClient(client["nombre"], client["apellido"], client["dni"], card=True)  # Crea un cliente RegularClient

                sale = Sale(cli)

                # Detalle de la venta
                follow = "s"
                line = 1

                while follow.lower() == "s":
                    print(f"{line}".ljust(6), end="   ")
                    id = int(validar.solo_numeros("Error: Solo números", 5, 6))  # Solicita el ID del producto
                    json_file = JsonFile(path  + '/archivos/products.json')

                    prods = json_file.find("id", id)  # Busca el producto por su ID

                    if not prods:
                        print("Producto no existe")
                        time.sleep(1)
                    else:
                        prods = prods[0]
                        product = Product(prods["id"], prods["descrip"], prods["preci"], prods["stock"])  # Crea un producto
                        print(product.descrip, str(product.preci), end=' ')
                        qyt = int(
                            validar.solo_numeros("Error: Solo números", 7, 34))  # Solicita la cantidad de producto
                        subtotal = product.preci * qyt
                        print(str(qyt), subtotal)
                        sale.add_detail(product, qyt)  # Agrega el detalle de la venta
                        print(f"Subtotal: {round(sale.subtotal, 2)}")
                        print(f"Descuento: {round(sale.discount, 2)}")
                        print(f"Iva     : {round(sale.iva, 2)}")
                        print(f"Total   : {round(sale.total, 2)}")
                        follow = input("¿Desea agregar otro producto? (s/n): ") or "s"
                        print(green_color + "✔" + reset_color)
                        line += 1

                print(red_color + "¿Está seguro de grabar la venta? (s/n): ", end='')
                procesar = input().lower()  # Pregunta si se quiere grabar la venta
                if procesar == "s":
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    archivos = sale.getJson()
                    archivos["factura"] = selected_invoice['factura']
                    invoices[selected_invoice_index] = archivos
                    json_file = JsonFile(path  + '/archivos/invoices.json')
                    json_file.save(invoices)
                else:
                    print("🤣 Venta Cancelada 🤣" + reset_color)
                time.sleep(2)

            elif selected_update == "3":
                validar = Valida()
                borrarPantalla()

                print('\033c', end='')  # Limpia la pantalla

                # Imprime la cabecera de la venta
                print(green_color + "*" * 90 + reset_color)
                print(blue_color + "Registro de Venta")
                print(blue_color + Company.get_business_name())
                print(f"Factura#: F0999999 {' ' * 3} Fecha: {datetime.datetime.now()}")
                print("Subtotal:")
                print("Descuento:")
                print("Iva     :")
                print("Total   :")
                print("Cédula:")

                dni = validar.solo_numeros("Error: Solo números", 8, 9)  # Solicita el número de cédula del cliente

                json_file = JsonFile(path + '/archivos/clients.json')

                client = json_file.find("dni", dni)  # Busca al cliente por su número de cédula
                if not client:
                    print("Cliente no existe")
                    return
                client = client[0]

                cli = RegularClient(client["nombre"], client["apellido"], client["dni"], card=True)  # Crea un cliente RegularClient

                sale = Sale(cli)  # Crea una venta asociada al cliente

                print(cli.fullName())
                print(green_color + "*" * 90 + reset_color)
                print(purple_color + "Linea", "Id_Articulo", "descrip", "preci", "Cantidad", "Subtotal")
                print(reset_color + "-" * 90)

                # Detalle de la venta
                follow = "s"
                line = 1

                while follow.lower() == "s":
                    print(f"{line}", end="   ")
                    id = int(validar.solo_numeros("Error: Solo números", 5, 25))  # Solicita el ID del producto
                    json_file = JsonFile(path  + '/archivos/products.json')

                    prods = json_file.find("id", id)  # Busca el producto por su ID

                    if not prods:
                        print("Producto no existe")
                        time.sleep(1)
                    else:
                        prods = prods[0]
                        product = Product(prods["id"], prods["descrip"], prods["preci"], prods["stock"])  # Crea un producto
                        print(product.descrip, str(product.preci), end=' ')
                        qyt = int(
                        validar.solo_numeros("Error: Solo números", 4, 45))  # Solicita la cantidad de producto
                        subtotal = product.preci * qyt
                        print(str(qyt), subtotal)
                        sale.add_detail(product, qyt)  # Agrega el detalle de la venta
                        print(f"Subtotal: {round(sale.subtotal, 2)}")
                        print(f"Descuento: {round(sale.discount, 2)}")
                        print(f"Iva     : {round(sale.iva, 2)}")
                        print(f"Total   : {round(sale.total, 2)}")
                        follow = input("¿Desea agregar otro producto? (s/n): ") or "s"
                        print(green_color + "✔" + reset_color)
                        line += 1

                print(red_color + "¿Está seguro de grabar la venta? (s/n): ", end='')
                procesar = input().lower()  # Pregunta si se quiere grabar la venta
                if procesar == "s":
                    archivos = sale.getJson()
                    archivos["factura"] = selected_invoice['factura']
                    invoices[selected_invoice_index] = archivos
                    json_file = JsonFile(path  + '/archivos/invoices.json')
                    json_file.save(invoices)
                else:
                    print("🤣 Venta Cancelada 🤣" + reset_color)
                time.sleep(2)
            else:
                print("Opción no válida.")

        else:
            print("Factura no encontrada.")

    def delete(self):
        # Cargar datos de facturas desde el archivo JSON
        with open(path  + '/archivos/invoices.json', 'r') as json_file:
            invoices = json.load(json_file)

        # Mostrar las facturas disponibles
        opciones = [f"{factura['factura']}) Factura: #{factura['factura']}" for factura in invoices]
        menu_delete = Menu("Menu Eliminar", opciones, 20, 10)

        print("Seleccione la factura que desea modificar:")
        selected_invoice_str = menu_delete.menu()
        selected_invoice_num = int(selected_invoice_str.split(')')[0])

        # Buscar la factura seleccionada
        selected_invoice_index = None
        for index, factura in enumerate(invoices):
            if factura['factura'] == selected_invoice_num:
                selected_invoice_index = index
                break

        if selected_invoice_index is not None:
            # Mostrar detalles de la factura seleccionada
            selected_invoice = invoices[selected_invoice_index]
            print("Factura:", selected_invoice['factura'])
            print("Fecha:", selected_invoice['Fecha'])
            print("Cliente:", selected_invoice['cliente'])
            print("Subtotal:", selected_invoice['subtotal'])
            print("Descuento:", selected_invoice['descuento'])
            print("IVA:", selected_invoice['iva'])
            print("Total:", selected_invoice['total'])
            print("Detalles:")
            for detalle in selected_invoice['detalle']:
                print("\tProducto:", detalle['producto'])
                print("\tpreci:", detalle['preci'])
                print("\tCantidad:", detalle['cantidad'])
            print()

            print("¿Está seguro de eliminar la venta? (s/n): ", end='')
            procesar = input().lower()  # Pregunta si se quiere grabar la venta
            if procesar == "s":
                # Eliminar la factura seleccionada de la lista
                del invoices[selected_invoice_index]

                # Escribir los datos actualizados de vuelta al archivo JSON
                with open(path  + '/archivos/invoices.json', 'w') as json_file:
                    json.dump(invoices, json_file, indent=2)
                    print("Factura eliminada exitosamente.")
            else:
                print("🤣 Venta Cancelada 🤣")
        else:
            print("Factura no encontrada.")

        time.sleep(2)

    def consult(self):
        print('\033c', end='')
        print(green_color + "█" * 90)
        print("██" + " " * 34 + "Consulta de Venta" + " " * 35 + "██")
        invoice = input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path  + '/archivos/invoices.json')
            invoices = json_file.find("factura", invoice)
            print(f"Impresión de la Factura#{invoice}")
            print(invoices)
        else:
            json_file = JsonFile(path  + '/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")

            suma = reduce(lambda total, invoice: round(total + invoice["total"], 2), invoices, 0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ", total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x = input("presione una tecla para continuar...")

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()    
            menu_clients = Menu("Menu Clientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                crud_clients = CrudClients()
                crud_clients.create()
            elif opc1 == "2":
                crud_clients = CrudClients()
                crud_clients.update()
            elif opc1 == "3":
                crud_clients = CrudClients()
                crud_clients.delete()
            elif opc1 == "4":
                crud_clients = CrudClients()
                crud_clients.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                crud_product = CrudProducts()
                crud_product.create()
                
            elif opc2 == "2":
                crud_product = CrudProducts()
                crud_product.update()
            elif opc2 == "3":
                crud_product = CrudProducts()
                crud_product.delete()
            elif opc2 == "4":
                crud_product = CrudProducts()
                crud_product.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales = CrudSales()
                sales.create()  
            elif opc3 == "2":
                sales = CrudSales()
                sales.consult()
            elif opc3 == "3":
                sales = CrudSales()
                sales.update()
            elif opc3 == "4":
                sales = CrudSales()
                sales.delete()          
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()
