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
                gotoxy(15,15);print("Cliente registrado exitosamente!")
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
                gotoxy(15,10);print("El cliente ha sido eliminado correctamente.")
                time.sleep(3)
            else:
                gotoxy(15,5);print("Operación cancelada...")
                time.sleep(3)
                return
        else:
            print()
            gotoxy(15,10);print("No se encontró ningún cliente con el DNI proporcionado.")
            time.sleep(3)

    
    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(15,2);print(blue_color+Company.get_business_name())
        gotoxy(2,1);print(green_color+"*"*90)
        gotoxy(27,3);print("Consulta de Cliente")
        print("-" * 90) 
        gotoxy(1,5);dni = input('Ingrese DNI del cliente: ')
        
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
            print()
            gotoxy(15,6);print("Cliente no encontrado.")
            time.sleep(3)
            print()
        gotoxy(10,6);input("Presione una tecla para continuar...")  
         

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
            
            print(f'Producto: {found_product["descripcion"]}')
            print(f'Precio: {found_product["precio"]}')
            print(f'Stock: {found_product["stock"]}')
            print("-" * 90) 
        
            print('Qué va a actualizar?')
            print('1. Nombre del producto.')
            print('2. Precio del producto.')
            print('3. Stock del producto.')
            print()
            opcion = input('Elija una opción: ')
            print("-" * 90)
        
            borrarPantalla()
            if opcion == "1":

                gotoxy(15,0);print('Cambio de nombre del producto.')
                print()
                new_name = input('Ingrese el nuevo nombre del producto: ')
                existing_product = next((prod for prod in products if prod['descripcion'].lower() == new_name.lower() and prod['id'] != id), None)
                print("-" * 90)
                if existing_product:
                    gotoxy(10,5);print(f"Este producto ya existe con el ID {existing_product['id']}.")
                    
                else:
                    found_product['descripcion'] = new_name
                    print("-" * 90)
                    json_file.save(products)
            
                    gotoxy(10,6);print("Nombre del producto actualizado exitosamente!")
                    time.sleep(4)

            elif opcion == "2":
                
                gotoxy(15,0);print('Cambio de precio del producto.')
                print()
                new_preci = input('Ingrese el nuevo precio del producto: ')
                found_product['precio'] = float(new_preci)
                print("-" * 90)
                json_file.save(products)
            
                gotoxy(10,6);print("Precio del producto actualizado exitosamente!")
                time.sleep(4)
            elif opcion == "3":
                
                gotoxy(15,0);print('Cambio stock del producto.')
                print()
                new_stock = input('Ingrese el nuevo stock del producto: ')
                found_product['stock'] = int(new_stock)
                print("-" * 90)
                json_file.save(products)
            
                gotoxy(10,6);print("Stock del producto actualizado exitosamente!")
                time.sleep(4)

            # Guardar los cambios en el archivo JSON
        else:
            
            gotoxy(15,5);print("Producto no encontrado.")
        time.sleep(3)

    
    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        gotoxy(15,2);print(blue_color + Company.get_business_name())
        gotoxy(25,3);print(blue_color + "Eliminar productos productos")
        print("-" * 90)

        id = int(input('Ingrese el ID del producto desea eliminar: '))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()
        

        found_product = None
        for product in products:
            if product['id'] == id:
                found_product = product
                products.remove(product)

        
        if found_product:
            print("-" * 90)
            print(f"Su producto es: {found_product['descripcion']}")
            respuesta = input('Esta seguro de eliminar este producto? (s/n): ').lower()
            if respuesta == 's':
                print("-" * 90)
                gotoxy(25,8);print('Se elimino su producto')
                for i, product in enumerate(products):
                    product['id'] = i + 1
                
                json_file.save(products)
                print("-" * 90)
                gotoxy(15,9);print('Se actualizaron los ID de los productos')
                time.sleep(3)
            else:
                gotoxy(15,5);print('Cancelando eliminacion...')
                time.sleep(3)
        else:
            print('Producto no encontrado')
            time.sleep(3)
                
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90)
        gotoxy(15,2);print(blue_color + Company.get_business_name())
        gotoxy(22,3);print("Consulta de Productos")
        print("-" * 90)
        print()
        gotoxy(1,5);id = int(input("Ingrese ID del producto: "))
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.find("id", id)
        
        if products:
            for product in products:
                print("-" * 90)
                print(f'Descripcion: {product["descripcion"]}')
                print(f'Precio: {product["precio"]}')
                print(f'Stock: {product["stock"]}')
                print("-" * 90)
                
            time.sleep(3)
        else:
            gotoxy(15,8);print("Producto no encontrado.")
            time.sleep(3)
        input("Presione una tecla para continuar...")   

class CrudSales(ICrud):
    def create(self):
        validar = Valida()
        borrarPantalla()

        print('\033c', end='')  # Limpia la pantalla

        # Imprime la cabecera de la venta
        gotoxy(1, 1);print(green_color + "*" * 90 + reset_color)
        gotoxy(27, 2);print(blue_color + "Registro de Venta")
        gotoxy(14, 3);print(blue_color + Company.get_business_name())
        gotoxy(5, 4);print(f"Factura#: F0999999 {' ' * 5}  Fecha: {datetime.datetime.now()}")
        
        gotoxy(72, 4);print("Subtotal:")
        gotoxy(72, 5);print("Descuento:")
        gotoxy(72, 6);print("Iva     :")
        gotoxy(72, 7);print("Total   :")
        gotoxy(1,6); print("Cedula :")
            
        dni = validar.solo_numeros("Error: Solo números", 10, 6)  # Solicita el número de cédula del cliente
            
        json_file = JsonFile(path +'/archivos/clients.json')
        client = json_file.find("dni", dni)  # Busca al cliente por su número de cédula
            
        if not client:
            gotoxy(1, 10);print("Cliente no existe")
            time.sleep(3)
            return
        client = client[0]

        cli = RegularClient(client["nombre"], client["apellido"], client["dni"],card=True)  # Crea un cliente RegularClient

        sale = Sale(cli)  # Crea una venta asociada al cliente

        gotoxy(30,6);print(cli.fullName())
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
                gotoxy(10, 15);print("Producto no existe")       
                time.sleep(3)
                break
            else:
                prods = prods[0]
                product = Product(prods["id"], prods["descripcion"], prods["precio"],prods["stock"])  # Crea un producto en la factura

                gotoxy(26,6);print(product.descrip)
                gotoxy(42,6); print(product.preci)
                qyt = int(validar.solo_numeros("Error: Solo números", 53, 6))  # Solicita la cantidad de producto

                if qyt > product.stock:
                    gotoxy(1, 15);print(f"El producto solo tiene un stock de {product.stock} ")
                    gotoxy(1, 15);respuesta = input('Desea llevar esa cantidad? (s/n): ').lower()
                    if respuesta == 's':
                        qyt = product.stock  # Actualiza la cantidad a la disponible en stock
                        new_subtotal = product.preci * qyt  # Calcula el nuevo subtotal
                        gotoxy(53, 4); print(qyt)  # Imprime la nueva cantidad
                        gotoxy(63, 4); print(new_subtotal)  # Imprime el nuevo subtotal
                        time.sleep(3)
                        
                        sale.add_detail(product, qyt)

                else:
                    subtotal = product.preci * qyt
                    gotoxy(63,6);print(subtotal)
                    sale.add_detail(product, qyt)

            if qyt != product.stock or respuesta == 's':
                gotoxy(1,18);follow = input('¿Desea agregar otro producto? (s/n): ').lower()
                if follow == "s":
                    gotoxy(78,9);print(green_color + "✔" + reset_color)
                    line += 1
                else:
                    gotoxy(80, 0);print(f"{round(sale.subtotal, 2)}")
                    gotoxy(80,5 );print(f"{round(sale.discount, 2)}")
                    gotoxy(80, -1);print(f"{round(sale.iva, 2)}")
                    gotoxy(80, 0);print(f"{round(sale.total, 2)}")

        gotoxy(1,78);print(red_color + "¿Está seguro de grabar la venta? (s/n): ", end='')
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
        file_json = JsonFile(path + '/archivos/invoices.json')
        product_json = JsonFile(path + '/archivos/products.json')
        invoice_number = int(input('Ingrese el numero de la factura: '))
        
    
        invoices = file_json.read()
        products = product_json.read()
        
        if invoices is None:
            print("No hay facturas para actualizar")
            time.sleep(2)
            return
        
        for invoice in invoices:
            if invoice['factura'] == invoice_number:
                print("Información de la factura:")
                for key, value in invoice.items():
                    if key != 'detalle':
                        print(f"{key}: {value}")
                print("Información del cliente: ")
                print(invoice['cliente'])
                print("Productos en la factura:")
                for product in invoice['detalle']:
                    product_info = ', '.join([f"{key}: {value}" for key, value in product.items()])
                    print(product_info)

                while True:
                    print("1. Añadir producto")
                    print("2. Eliminar producto")
                    print("3. Cambiar cantidad de producto")
                    
                    option = input("Seleccione una opción: ")
                    
                    if option == "1":
                        product_id = int(input("Ingrese el ID del producto que desea añadir: "))
                        product_to_add = next((prod for prod in products if prod['id'] == product_id), None)
                        if product_to_add is None:
                            print("Por favor, ingrese un ID de producto válido")
                            time.sleep(2)
                            continue
                            
                        product_quantity = int(input("Ingrese la cantidad del producto que desea añadir: "))
                        new_product = {
                            "producto": product_to_add['descripcion'],
                            "cantidad": product_quantity,
                            "precio": product_to_add['precio']
                        }
                        invoice['detalle'].append(new_product)
                        # Actualizar los totales de la factura
                        invoice['subtotal'] = sum([float(product['precio']) * int(product['cantidad']) for product in invoice['detalle']])
                        invoice['descuento'] = invoice['subtotal'] * 0.10  # Assuming a 10% discount
                        invoice['iva'] = invoice['subtotal'] * 0.12  # Assuming a 12% iva
                        invoice['total'] = invoice['subtotal'] - invoice['descuento'] + invoice['iva']
                        print("Se ha añadido el producto")
                        file_json.save(invoices)
                        
                    elif option == "2":
                        product_description = input("Ingrese la descripción del producto que desea eliminar: ")
                        for i, product in enumerate(invoice['detalle']):
                            if product['poducto'] == product_description:
                                del invoice['detalle'][i]
                                # Actualizar los totales de la factura
                                invoice['subtotal'] = sum([float(product['precio']) * int(product['cantidad']) for product in invoice['detalle']])
                                invoice['descuento'] = invoice['subtotal'] * 0.10  # Assuming a 10% discount
                                invoice['iva'] = invoice['subtotal'] * 0.15  # Assuming a 15% iva
                                invoice['total'] = invoice['subtotal'] - invoice['descuento'] + invoice['iva']
                                print("Se ha eliminado el producto")
                                file_json.save(invoices)
                                time.sleep(4)
                                break
                            else:
                                print("Producto no encontrado")
                        
                    elif option == "3":
                        product_description = input("Ingrese la descripción del producto cuya cantidad desea cambiar: ")
                        for product in invoice['detalle']:
                            if product['poducto'] == product_description:
                                new_quantity = int(input("Ingrese la nueva cantidad del producto: "))
                                product['cantidad'] = new_quantity
                                # Actualizar los totales de la factura
                                invoice['subtotal'] = sum([float(product['precio']) * int(product['cantidad']) for product in invoice['detalle']])
                                invoice['descuento'] = invoice['subtotal'] * 0.10  # Assuming a 10% discount
                                invoice['iva'] = invoice['subtotal'] * 0.12  # Assuming a 12% iva
                                invoice['total'] = invoice['subtotal'] - invoice['descuento'] + invoice['iva']
                                print("Se ha actualizado el producto")
                                file_json.save(invoices)
                                time.sleep(4)
                                break
                            else:
                                print("Producto no encontrado")
                            time.sleep(4)
                    else:
                        print("Opción no válida")
                        time.sleep(4)
            print("No se ha encontrado la factura")
            time.sleep(4)

    def delete(self):
        # Cargar datos de facturas desde el archivo JSON
        with open(path  + '/archivos/invoices.json', 'r') as json_file:
            invoices = json.load(json_file)

        # Mostrar las facturas disponibles
        opciones = [f"{factura['factura']}) Factura: #{factura['factura']}" for factura in invoices]
        menu_delete = Menu("Menu Eliminar", opciones, 20, 10)

        print("Seleccione la factura que desea eliminar:")
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
            for detalle in selected_invoice["detalle"]:
                print("\tProducto:", detalle["poducto"])
                print("\tprecio:", detalle["precio"])
                print("\tCantidad:", detalle["cantidad"])
            print()

            print("¿Está seguro de eliminar la venta? (s/n): ", end='')
            procesar = input().lower()  # Pregunta si se quiere grabar la venta
            if procesar == "s":
                # Eliminar la factura seleccionada de la lista
                del invoices[selected_invoice_index]

                #Actualizar los id de las facturas al eliminar
                for i, invoice in enumerate(invoices, start=1):
                    invoice['factura'] = i 
                
                
                print("-" * 90)
                gotoxy(15,9);print('Se actualizaron los ID de las facturas')
                time.sleep(3)

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
        print(green_color + "*" * 90)
        print("Consulta de Venta")
        invoice = input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path  + '/archivos/invoices.json')
            invoices = json_file.find("factura", invoice)
            print(f"Impresión de la Factura# {invoice} ")
            for invoice in invoices:
                for key, value in invoice.items():
                    if key == 'detalle':
                        print('Informacion de la factura:')
                        for item in value:
                            print(f'Producto:{item["poducto"]}')
                            print(f'Precio:{item["precio"]}')
                            print(f'Cantidad:{item["cantidad"]}')
                    else:
                        print(f'{key}:{value}')

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
