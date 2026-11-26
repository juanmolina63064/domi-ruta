"""Ocho pruebas mínimas exigidas en el proyecto final."""

from estructuras.arbol_bst import ArbolBST
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.lista_enlazada import ListaEnlazada
from estructuras.tabla_hash import TablaHash
from modelo.cliente import Cliente
from modelo.pedido import EstadoPedido, Pedido
from servicios.gestor_pedidos import GestorPedidos
from util.recursion import contar_urgentes, buscar_recursivo, sumar_valores


class _ContadorPruebas:
    """Acumula resultados sin utilizar colecciones del lenguaje."""

    def __init__(self) -> None:
        self.aprobadas = 0
        self.fallidas = 0

    def aprobar(self) -> None:
        """Registra una prueba aprobada."""
        self.aprobadas += 1

    def fallar(self) -> None:
        """Registra una prueba fallida."""
        self.fallidas += 1


def _ejecutar(nombre: str, prueba, contador: _ContadorPruebas) -> None:
    """Ejecuta una prueba e informa su resultado sin detener las demás."""
    try:
        prueba()
        print(f"[OK] {nombre}")
        contador.aprobar()
    except Exception as error:
        print(f"[ERROR] {nombre}: {error}")
        contador.fallar()


def _prueba_1_eliminar_lista_vacia() -> None:
    """Caso 1: eliminar en una lista vacía devuelve False."""
    lista: ListaEnlazada[int] = ListaEnlazada()
    assert lista.eliminar(10) is False
    assert len(lista) == 0


def _prueba_2_invertir_lista() -> None:
    """Caso 2: invierte físicamente una lista mediante recursión."""
    lista: ListaEnlazada[int] = ListaEnlazada()
    lista.insertar_final(1)
    lista.insertar_final(2)
    lista.insertar_final(3)
    lista.insertar_final(4)
    lista.invertir_recursivamente()
    assert str(lista) == "4 -> 3 -> 2 -> 1"


def _prueba_3_cancelar_y_deshacer() -> None:
    """Caso 3: al deshacer una cancelación, el pedido vuelve a EN_ESPERA."""
    gestor = GestorPedidos()
    cliente = Cliente(1, "Laura", "3001112233", "Centro")
    assert gestor.registrar_cliente(cliente)
    pedido = Pedido(15, 1, "Mercado", 25000.0, "Centro", False)
    assert gestor.crear_pedido(pedido)
    assert gestor.cancelar_pedido(15)
    assert pedido.estado == EstadoPedido.CANCELADO
    assert gestor.deshacer()
    assert pedido.estado == EstadoPedido.EN_ESPERA
    assert len(gestor.ver_cola_espera()) == 1


def _prueba_4_prioridad_estable() -> None:
    """Caso 4: urgentes primero y FIFO dentro de cada prioridad."""
    cola: ColaPrioridad[Pedido] = ColaPrioridad()
    cola.encolar(Pedido(1, 1, "Normal A", 1.0, "Centro", False))
    cola.encolar(Pedido(2, 1, "Urgente B", 1.0, "Centro", True))
    cola.encolar(Pedido(3, 1, "Normal C", 1.0, "Centro", False))
    cola.encolar(Pedido(4, 1, "Urgente D", 1.0, "Centro", True))
    assert cola.desencolar().id == 2
    assert cola.desencolar().id == 4
    assert cola.desencolar().id == 1
    assert cola.desencolar().id == 3


def _prueba_5_colisiones_hash() -> None:
    """Caso 5: las llaves 3, 14 y 25 colisionan en el índice 3."""
    tabla: TablaHash[str] = TablaHash(11)
    tabla.insertar(3, "A")
    tabla.insertar(14, "B")
    tabla.insertar(25, "C")
    assert tabla.capacidad == 11
    assert tabla.funcion_hash(3) == 3
    assert tabla.funcion_hash(14) == 3
    assert tabla.funcion_hash(25) == 3
    assert tabla.buscar(3) == "A"
    assert tabla.buscar(14) == "B"
    assert tabla.buscar(25) == "C"


def _prueba_6_redimension_hash() -> None:
    """Caso 6: al superar el factor 0.75, la tabla crece y conserva los datos."""
    tabla: TablaHash[str] = TablaHash(11)
    indice = 0
    while indice < 12:
        tabla.insertar(indice, f"Cliente {indice}")
        indice += 1
    assert tabla.capacidad > 11
    assert len(tabla) == 12
    indice = 0
    while indice < 12:
        assert tabla.buscar(indice) == f"Cliente {indice}"
        indice += 1


def _prueba_7_recorrido_inorden() -> None:
    """Caso 7: el inorden devuelve los siete códigos en orden ascendente."""
    arbol: ArbolBST[int] = ArbolBST()
    arbol.insertar(50)
    arbol.insertar(30)
    arbol.insertar(70)
    arbol.insertar(20)
    arbol.insertar(40)
    arbol.insertar(60)
    arbol.insertar(80)
    assert str(arbol.inorden()) == "20 -> 30 -> 40 -> 50 -> 60 -> 70 -> 80"


def _prueba_8_eliminar_raiz_dos_hijos() -> None:
    """Caso 8: eliminar la raíz con dos hijos conserva el orden del BST."""
    arbol: ArbolBST[int] = ArbolBST()
    arbol.insertar(50)
    arbol.insertar(30)
    arbol.insertar(70)
    arbol.insertar(20)
    arbol.insertar(40)
    arbol.insertar(60)
    arbol.insertar(80)
    assert arbol.eliminar(50)
    assert str(arbol.inorden()) == "20 -> 30 -> 40 -> 60 -> 70 -> 80"
    assert len(arbol) == 6



def _prueba_9_funciones_recursivas() -> None:
    """Comprueba suma, conteo de urgentes y búsqueda recursiva."""
    historial: ListaEnlazada[Pedido] = ListaEnlazada()
    pedido_a = Pedido(21, 1, "A", 1000.0, "Centro", True)
    pedido_b = Pedido(22, 1, "B", 2500.0, "Palermo", False)
    historial.insertar_final(pedido_a)
    historial.insertar_final(pedido_b)
    assert sumar_valores(historial.cabeza) == 3500.0
    assert contar_urgentes(historial.cabeza) == 1
    assert buscar_recursivo(historial.cabeza, pedido_b)
    assert not buscar_recursivo(historial.cabeza, Pedido(23, 1, "C", 50.0, "Centro", False))


def ejecutar_pruebas() -> bool:
    """Ejecuta los ocho casos mínimos y devuelve True si todos pasan."""
    print("\nPRUEBAS DE DOMIRUTA")
    print("-" * 45)
    contador = _ContadorPruebas()
    _ejecutar("1. Eliminar de una lista vacía", _prueba_1_eliminar_lista_vacia, contador)
    _ejecutar("2. Invertir recursivamente 1 -> 2 -> 3 -> 4", _prueba_2_invertir_lista, contador)
    _ejecutar("3. Crear, cancelar y deshacer un pedido", _prueba_3_cancelar_y_deshacer, contador)
    _ejecutar("4. Prioridad urgente y orden de llegada", _prueba_4_prioridad_estable, contador)
    _ejecutar("5. Colisiones de la tabla hash", _prueba_5_colisiones_hash, contador)
    _ejecutar("6. Redimensionamiento de la tabla hash", _prueba_6_redimension_hash, contador)
    _ejecutar("7. Recorrido inorden del árbol", _prueba_7_recorrido_inorden, contador)
    _ejecutar("8. Eliminar raíz del BST con dos hijos", _prueba_8_eliminar_raiz_dos_hijos, contador)
    _ejecutar("9. Funciones recursivas de historial", _prueba_9_funciones_recursivas, contador)
    print("-" * 45)
    print(f"Resultado: {contador.aprobadas} aprobadas, {contador.fallidas} fallidas")
    return contador.fallidas == 0


if __name__ == "__main__":
    ejecutar_pruebas()
