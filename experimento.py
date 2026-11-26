"""Compara 1.000 búsquedas en lista enlazada y tabla hash."""

import random
from time import perf_counter

from estructuras.lista_enlazada import ListaEnlazada
from estructuras.tabla_hash import TablaHash
from modelo.cliente import Cliente


def ejecutar_experimento() -> None:
    """Genera 10.000 clientes y mide ambos métodos con las mismas consultas."""
    cantidad_clientes = 10000
    cantidad_consultas = 1000
    generador = random.Random(2308)
    clientes_lista: ListaEnlazada[Cliente] = ListaEnlazada()
    clientes_hash: TablaHash[Cliente] = TablaHash(11)
    consultas: ListaEnlazada[int] = ListaEnlazada()

    print(f"Generando {cantidad_clientes} clientes...")
    indice = 0
    while indice < cantidad_clientes:
        codigo = generador.randint(100000, 999999999)
        while clientes_hash.buscar(codigo) is not None:
            codigo = generador.randint(100000, 999999999)
        cliente = Cliente(codigo, f"Cliente {indice}", "3000000000", "Manizales")
        clientes_lista.insertar_final(cliente)
        clientes_hash.insertar(codigo, cliente)
        if indice % (cantidad_clientes // cantidad_consultas) == 0:
            consultas.insertar_final(codigo)
        indice += 1

    inicio_lista = perf_counter()
    for codigo in consultas:
        clientes_lista.buscar(Cliente(codigo, "", "", ""))
    tiempo_lista = perf_counter() - inicio_lista

    inicio_hash = perf_counter()
    for codigo in consultas:
        clientes_hash.buscar(codigo)
    tiempo_hash = perf_counter() - inicio_hash

    print("\nRESULTADOS DEL EXPERIMENTO")
    print(f"Clientes cargados: {cantidad_clientes}")
    print(f"Búsquedas realizadas: {cantidad_consultas}")
    print(f"Capacidad final de la tabla hash: {clientes_hash.capacidad}")
    print(f"Factor de carga final: {clientes_hash.factor_carga():.4f}")
    print(f"Tiempo lista enlazada: {tiempo_lista:.6f} segundos")
    print(f"Tiempo tabla hash:     {tiempo_hash:.6f} segundos")
    if tiempo_hash > 0:
        print(f"Relación lista/hash:   {tiempo_lista / tiempo_hash:.2f} veces")


if __name__ == "__main__":
    ejecutar_experimento()
