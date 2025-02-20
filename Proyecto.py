import re
from datetime import datetime

def Com_placa(placa):
    patron = r'^[A-Z]{3}-[0-9]{4}$'
    return re.match(patron, placa)

class NodoMantenimiento:
    def __init__(self, fecha, descripcion, costo):
        self.fecha = self.validar_fecha(fecha)
        self.descripcion = descripcion
        self.costo = self.validar_costo(costo)
        self.siguiente = None

    def validar_fecha(self, fecha):
        try:
            return datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido, debe ser YYYY-MM-DD")

    def validar_costo(self, costo):
        if costo < 0:
            raise ValueError("El costo no puede ser negativo")
        return costo

class ListaMantenimientos:
    def __init__(self):
        self.primero = None

    def agregar_mantenimiento(self, fecha, descripcion, costo):
        nuevo = NodoMantenimiento(fecha, descripcion, costo)
        if not self.primero:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def listar_mantenimientos(self):
        mantenimientos = []
        actual = self.primero
        while actual:
            mantenimientos.append(f"{actual.fecha} - {actual.descripcion} (${actual.costo})")
            actual = actual.siguiente
        return mantenimientos if mantenimientos else ["Sin mantenimientos"]

    def calcular_costo_total(self):
        total = 0
        actual = self.primero
        while actual:
            total += actual.costo
            actual = actual.siguiente
        return total

class NodoVehiculo:
    def __init__(self, placa, marca, modelo, año, kilometraje):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.kilometraje = kilometraje
        self.mantenimientos = ListaMantenimientos()
        self.siguiente = None
        self.anterior = None

class ListaVehiculos:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def registrar_vehiculo(self, placa, marca, modelo, año, kilometraje):
        nuevo = NodoVehiculo(placa, marca, modelo, año, kilometraje)
        if not self.primero:
            self.primero = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo

    def buscar_vehiculo(self, placa):
        actual = self.primero
        while actual:
            if actual.placa == placa:
                return actual
            actual = actual.siguiente
        return None

    def eliminar_vehiculo(self, placa):
        actual = self.primero
        while actual:
            if actual.placa == placa:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.primero = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.ultimo = actual.anterior
                print("Vehículo eliminado correctamente.")
                return
            actual = actual.siguiente
        print("Vehículo no encontrado.")

    def mostrar_vehiculos(self):
        actual = self.primero
        while actual:
            print(f"Placa: {actual.placa}, Marca: {actual.marca}, Modelo: {actual.modelo}, Año: {actual.año}, Kilometraje: {actual.kilometraje}")
            print("Mantenimientos:", actual.mantenimientos.listar_mantenimientos())
            print(f"Costo total de mantenimientos: ${actual.mantenimientos.calcular_costo_total()}")
            actual = actual.siguiente

def menu():
    flota = ListaVehiculos()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar vehículo")
        print("2. Mostrar vehículos")
        print("3. Buscar vehículo")
        print("4. Agregar mantenimiento")
        print("5. Calcular costo total de mantenimientos")
        print("6. Eliminar vehículo")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                placa = input("Ingrese la placa (AAA-1234): ")
                if not Com_placa(placa):
                    print("Placa inválida.")
                    input("Presione Enter para continuar...")
                    continue
                marca = input("Ingrese la marca: ")
                modelo = input("Ingrese el modelo: ")
                x = int(input("Ingrese el año: "))
                if x < 1900 or x > 2023:
                    print("Año inválido.")
                    input("Presione Enter para continuar...")
                    continue
                else:
                    año = x
                kilometraje = int(input("Ingrese el kilometraje: "))
                flota.registrar_vehiculo(placa, marca, modelo, año, kilometraje)
                print("Vehículo registrado con éxito.")

            case "2":
                flota.mostrar_vehiculos()
                input("Presione Enter para continuar...")

            case "3":
                placa = input("Ingrese la placa a buscar: ")
                vehiculo = flota.buscar_vehiculo(placa)
                if vehiculo:
                    print(f"Placa: {vehiculo.placa}, Marca: {vehiculo.marca}, Modelo: {vehiculo.modelo}, Año: {vehiculo.año}, Kilometraje: {vehiculo.kilometraje}")
                else:
                    print("Vehículo no encontrado.")
                input("Presione Enter para continuar...")

            case "4":
                placa = input("Ingrese la placa del vehículo: ")
                vehiculo = flota.buscar_vehiculo(placa)
                if vehiculo:
                    fecha = input("Ingrese la fecha del mantenimiento (YYYY-MM-DD): ")
                    descripcion = input("Ingrese la descripción: ")
                    costo = float(input("Ingrese el costo: "))
                    vehiculo.mantenimientos.agregar_mantenimiento(fecha, descripcion, costo)
                    print("Mantenimiento agregado con éxito.")
                else:
                    print("Vehículo no encontrado.")
                input("Presione Enter para continuar...")

            case "5":
                placa = input("Ingrese la placa del vehículo: ")
                vehiculo = flota.buscar_vehiculo(placa)
                if vehiculo:
                    print(f"Costo total de mantenimientos: ${vehiculo.mantenimientos.calcular_costo_total()}")
                else:
                    print("Vehículo no encontrado.")
                input("Presione Enter para continuar...")

            case "6":
                placa = input("Ingrese la placa a eliminar: ")
                flota.eliminar_vehiculo(placa)
                input("Presione Enter para continuar...")

            case "7":
                print("Saliendo...")
                break

            case _:
                print("Opción no válida. Intente de nuevo.")
                input("Presione Enter para continuar...")

menu()