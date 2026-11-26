"""Menú principal de la aplicación DomiRuta Manizales."""

from modelo.cliente import Cliente
from modelo.pedido import EstadoPedido, Pedido
from servicios.gestor_pedidos import GestorPedidos
from util.recursion import contar_urgentes, sumar_valores


def _leer_entero(mensaje: str) -> int:
    """Solicita un entero y repite la pregunta cuando la entrada no es válida."""
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Escribe un número entero válido.")


def _leer_decimal(mensaje: str) -> float:
    """Solicita un valor decimal; acepta punto o coma como separador."""
    while True:
        try:
            return float(input(mensaje).strip().replace(",", "."))
        except ValueError:
            print("Escribe un valor numérico válido.")


def _registrar_cliente(gestor: GestorPedidos) -> None:
    """Lee los datos y registra un cliente."""
    print("\nREGISTRAR CLIENTE")
    codigo = _leer_entero("Código: ")
    nombre = input("Nombre: ").strip()
    telefono = input("Teléfono: ").strip()
    barrio = input("Barrio: ").strip()
    if not nombre or not telefono or not barrio:
        print("No se registró: todos los campos son obligatorios.")
        return
    cliente = Cliente(codigo, nombre, telefono, barrio)
    if gestor.registrar_cliente(cliente):
        print("Cliente registrado correctamente.")
    else:
        print("Ya existe un cliente con ese código.")


def _buscar_cliente(gestor: GestorPedidos) -> None:
    """Busca un cliente por código y muestra su historial."""
    codigo = _leer_entero("Código del cliente: ")
    cliente = gestor.buscar_cliente(codigo)
    if cliente is None:
        print("No se encontró el cliente.")
        return
    print(cliente)
    print("Historial de pedidos:")
    if cliente.historial_pedidos.esta_vacia():
        print("  Sin pedidos registrados.")
    else:
        for pedido in cliente.historial_pedidos:
            print(f"  {pedido}")
    total = sumar_valores(cliente.historial_pedidos.cabeza)
    urgentes = contar_urgentes(cliente.historial_pedidos.cabeza)
    print(f"Total recursivo de pedidos: ${total:.2f}")
    print(f"Pedidos urgentes: {urgentes}")


def _crear_pedido(gestor: GestorPedidos) -> None:
    """Lee los datos y crea un pedido para un cliente registrado."""
    print("\nCREAR PEDIDO")
    identificador = _leer_entero("ID del pedido: ")
    codigo_cliente = _leer_entero("Código del cliente: ")
    if gestor.buscar_cliente(codigo_cliente) is None:
        print("Primero debes registrar al cliente.")
        return
    descripcion = input("Descripción: ").strip()
    valor = _leer_decimal("Valor: $")
    barrio = input("Barrio de destino: ").strip()
    respuesta = input("¿Es urgente? (s/n): ").strip().lower()
    urgente = respuesta == "s"
    if not descripcion or not barrio or valor < 0:
        print("No se creó: revisa la descripción, el barrio y el valor.")
        return
    pedido = Pedido(identificador, codigo_cliente, descripcion, valor, barrio, urgente)
    if gestor.crear_pedido(pedido):
        print("Pedido creado y agregado a la cola de espera.")
    else:
        print("No se pudo crear. Revisa el ID del pedido.")


def _asignar_pedido(gestor: GestorPedidos) -> None:
    """Asigna y muestra el pedido con mayor prioridad."""
    pedido = gestor.asignar_siguiente()
    if pedido is None:
        print("No hay pedidos en espera.")
    else:
        print("Pedido asignado:")
        print(pedido)


def _cancelar_pedido(gestor: GestorPedidos) -> None:
    """Cancela un pedido por su identificador."""
    identificador = _leer_entero("ID del pedido que deseas cancelar: ")
    if gestor.cancelar_pedido(identificador):
        print("Pedido cancelado. Puedes usar Deshacer para revertir la acción.")
    else:
        print("No se pudo cancelar. Comprueba el ID y el estado del pedido.")


def _mostrar_cola(gestor: GestorPedidos) -> None:
    """Muestra los pedidos según el orden en que serán atendidos."""
    cola = gestor.ver_cola_espera()
    if cola.esta_vacia():
        print("No hay pedidos en espera.")
        return
    print("\nPEDIDOS EN ORDEN DE ATENCIÓN")
    for pedido in cola:
        print(pedido)


def _mostrar_clientes_ordenados(gestor: GestorPedidos) -> None:
    """Imprime el reporte ascendente generado mediante recorrido inorden."""
    clientes = gestor.clientes_ordenados()
    if clientes.esta_vacia():
        print("No hay clientes registrados.")
        return
    print("\nCLIENTES ORDENADOS POR CÓDIGO")
    for cliente in clientes:
        print(cliente)


def _mostrar_clientes_rango(gestor: GestorPedidos) -> None:
    """Imprime clientes dentro de un rango de códigos."""
    desde = _leer_entero("Código inicial: ")
    hasta = _leer_entero("Código final: ")
    clientes = gestor.clientes_en_rango(desde, hasta)
    if clientes.esta_vacia():
        print("No se encontraron clientes en ese rango.")
        return
    for cliente in clientes:
        print(cliente)


def _cambiar_estado(gestor: GestorPedidos) -> None:
    """Permite marcar un pedido como entregado y registra la operación."""
    identificador = _leer_entero("ID del pedido: ")
    pedido = gestor.buscar_pedido(identificador)
    if pedido is None:
        print("No existe ese pedido.")
        return
    print("1. Asignado")
    print("2. Entregado")
    opcion = input("Nuevo estado: ").strip()
    if opcion == "1":
        nuevo_estado = EstadoPedido.ASIGNADO
    elif opcion == "2":
        nuevo_estado = EstadoPedido.ENTREGADO
    else:
        print("Opción no válida.")
        return
    if gestor.cambiar_estado(identificador, nuevo_estado):
        print("Estado actualizado. La operación se puede deshacer.")
    else:
        print("No se pudo cambiar el estado.")


def mostrar_menu() -> None:
    """Muestra las opciones disponibles en consola."""
    print("\n========== DOMIRUTA MANIZALES ==========")
    print("1. Registrar cliente")
    print("2. Buscar cliente e historial")
    print("3. Crear pedido")
    print("4. Asignar siguiente pedido")
    print("5. Cancelar pedido")
    print("6. Ver cola de espera")
    print("7. Deshacer última operación")
    print("8. Reporte de clientes ordenados")
    print("9. Reporte de clientes por rango")
    print("10. Cambiar estado de pedido")
    print("11. Ejecutar pruebas")
    print("0. Salir")
    print("========================================")


def main() -> None:
    """Inicia la aplicación y mantiene activo el menú principal."""
    gestor = GestorPedidos()
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            _registrar_cliente(gestor)
        elif opcion == "2":
            _buscar_cliente(gestor)
        elif opcion == "3":
            _crear_pedido(gestor)
        elif opcion == "4":
            _asignar_pedido(gestor)
        elif opcion == "5":
            _cancelar_pedido(gestor)
        elif opcion == "6":
            _mostrar_cola(gestor)
        elif opcion == "7":
            print("Operación deshecha." if gestor.deshacer() else "No hay operaciones para deshacer.")
        elif opcion == "8":
            _mostrar_clientes_ordenados(gestor)
        elif opcion == "9":
            _mostrar_clientes_rango(gestor)
        elif opcion == "10":
            _cambiar_estado(gestor)
        elif opcion == "11":
            from pruebas import ejecutar_pruebas
            ejecutar_pruebas()
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
