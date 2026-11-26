# DomiRuta Manizales

Sistema de gestión de domicilios desarrollado en Python 3.10 o superior para el proyecto final de Estructuras de Datos Aplicadas (230G8F), Universidad de Caldas.

## Requisitos

- Python 3.10 o superior.
- No requiere instalar paquetes externos.
- Ejecutar los comandos desde esta carpeta, donde se encuentra `main.py`.

## Ejecutar el programa

```bash
python main.py
```

El menú permite registrar y buscar clientes, consultar historiales, crear pedidos, asignar pedidos por prioridad, cancelar pedidos, deshacer operaciones, consultar la cola y generar reportes de clientes.

## Ejecutar las pruebas

```bash
python pruebas.py
```

Se implementan los ocho casos mínimos indicados en el enunciado. La salida muestra cuáles pasan y cuáles fallan.

## Ejecutar el experimento de rendimiento

```bash
python experimento.py
```

El programa genera 10.000 clientes con códigos aleatorios y mide 1.000 búsquedas sobre la lista enlazada y la tabla hash. Los tiempos se imprimen en segundos. Registra los valores obtenidos en `ANALISIS.md`; los resultados dependen del equipo donde se ejecute el experimento.

## Organización del código

```text
DomiRuta/
├── estructuras/
│   ├── __init__.py
│   ├── nodo.py
│   ├── lista_enlazada.py
│   ├── pila.py
│   ├── cola.py
│   ├── cola_prioridad.py
│   ├── tabla_hash.py
│   └── arbol_bst.py
├── modelo/
│   ├── __init__.py
│   ├── cliente.py
│   ├── pedido.py
│   └── operacion.py
├── servicios/
│   ├── __init__.py
│   ├── gestor_pedidos.py
│   └── directorio_clientes.py
├── util/
│   ├── __init__.py
│   └── recursion.py
├── docs/
│   └── diagrama_clases.md
├── main.py
├── pruebas.py
├── experimento.py
└── ANALISIS.md
```

## Decisiones de implementación

- La lista, la pila y las colas se construyen con nodos enlazados.
- La cola de prioridad usa dos colas: una para urgentes y otra para normales. Así, los urgentes se atienden primero y se conserva el orden de llegada dentro de cada grupo.
- La tabla hash inicia con capacidad 11, usa `clave % capacidad`, resuelve colisiones por encadenamiento y crece cuando el factor de carga supera 0.75. El nuevo tamaño es el siguiente número primo después de duplicar la capacidad.
- El árbol binario de búsqueda compara clientes por código. Su recorrido inorden produce el reporte ascendente.
- Los recorridos del árbol devuelven una `ListaEnlazada`, no una colección incorporada de Python.
- La única lista de Python utilizada como estructura es el arreglo fijo de cubetas de la tabla hash, permitido expresamente por el enunciado.

## Git y entregas parciales

El enunciado solicita un repositorio compartido, aportes de todos los integrantes y al menos un commit por día de trabajo. No se debe crear un historial ficticio: cada integrante debe registrar sus propios cambios. Después de validar cada fase, se pueden crear las etiquetas solicitadas:

```bash
git tag v1-listas
git tag v2-lineales
git tag v3-arboles
```

Antes de crear cada etiqueta, ejecutar las pruebas y confirmar los cambios de la fase correspondiente.
