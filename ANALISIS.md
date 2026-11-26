# Análisis de DomiRuta

## 1. Experimento: lista enlazada frente a tabla hash

El experimento de `experimento.py` genera 10.000 clientes con códigos enteros aleatorios y realiza 1.000 búsquedas de clientes existentes. Se consultan los mismos códigos en las dos estructuras y se mide el tiempo con `time.perf_counter()`.

Para obtener los datos en el equipo del grupo, ejecutar:

```bash
python experimento.py
```

Registrar la salida en esta tabla. No se dejan tiempos inventados porque el resultado depende del procesador, la memoria y el estado del equipo donde se ejecute.

| Medición | Resultado obtenido |
|---|---:|
| Clientes cargados | 10.000 |
| Búsquedas realizadas | 1.000 |
| Capacidad final de la tabla hash | 25.717 |
| Factor de carga final | 0,3888 |
| Tiempo de búsqueda en lista enlazada (s) | 0,607958 |
| Tiempo de búsqueda en tabla hash (s) | 0,000751 |
| Relación entre ambos tiempos | 809,46 veces |

Medición de referencia obtenida al ejecutar el experimento durante la preparación de este proyecto. Los tiempos son orientativos y pueden cambiar según el computador donde se vuelva a ejecutar. Para el informe de entrega, conviene reemplazarlos por la medición del equipo del grupo.

### Interpretación esperada

La búsqueda en la lista enlazada es secuencial: en el peor caso debe revisar los 10.000 nodos. Su complejidad es O(n). La tabla hash calcula una posición usando el código del cliente y busca dentro de la cubeta correspondiente. Con una buena distribución de llaves, la búsqueda promedio se aproxima a O(1); si muchas llaves colisionan, el costo aumenta y depende de la longitud de la cadena.

La comparación debe basarse en los tiempos que muestre el experimento ejecutado por el grupo. La tabla hash no garantiza que todas las búsquedas tarden lo mismo: las colisiones pueden afectar el resultado.

## 2. Tipo de recursión en las funciones de la lista

| Función | Tipo | Motivo |
|---|---|---|
| `sumar_valores` | Lineal no terminal | Después de regresar de la llamada recursiva, todavía suma el valor del nodo actual. |
| `contar_urgentes` | Lineal no terminal | Después de regresar de la llamada recursiva, suma el indicador del nodo actual. |
| `buscar_recursivo` | Lineal de cola | Cuando el dato no coincide, retorna directamente el resultado de la llamada al siguiente nodo. |
| `invertir_lista` | Lineal de cola | La función auxiliar invierte el enlace y llama al siguiente nodo como última operación. |

## 3. Límite de recursión de Python

Las funciones recursivas de la lista enlazada y algunos métodos del árbol consumen una llamada de función por nivel de recursión. Python limita la profundidad de llamadas para evitar que una recursión descontrolada agote la pila de ejecución. El valor habitual inicial es cercano a 1.000, pero se puede consultar en la instalación utilizada con:

```python
import sys
print(sys.getrecursionlimit())
```

En una lista muy larga, `sumar_valores`, `contar_urgentes`, `buscar_recursivo` o `invertir_lista` podrían superar ese límite. El mismo riesgo aparece en operaciones recursivas de un árbol muy desbalanceado. El límite no significa que todas las listas deban tener exactamente 1.000 elementos: la profundidad real disponible depende también de las llamadas que ya estén activas.

## 4. Decisiones de diseño

### Lista enlazada

Se mantienen referencias a la cabeza y a la cola. Por eso insertar al final cuesta O(1). Buscar, obtener por posición y eliminar requieren recorrer nodos y cuestan O(n) en el peor caso.

### Pila y colas

La pila trabaja con el criterio LIFO: el último registro agregado es el primero que se retira. Se utiliza para deshacer operaciones. La cola normal funciona con FIFO. La cola de prioridad contiene dos colas enlazadas: los urgentes se atienden antes, manteniendo FIFO entre urgentes y FIFO entre normales.

### Tabla hash

La tabla inicia con 11 cubetas. Las colisiones se resuelven mediante encadenamiento con la lista enlazada de la Fase 1. Cuando el factor de carga supera 0.75, se crea un arreglo con el siguiente primo después de duplicar la capacidad y se reubican las entradas.

### Árbol binario de búsqueda

Los clientes se comparan por código. El recorrido inorden produce el directorio ascendente. El reporte por rango evita recorrer ramas que no pueden contener códigos dentro de los límites solicitados.

## 5. Cobertura de pruebas

El archivo `pruebas.py` ejecuta los ocho casos mínimos del documento del proyecto y una prueba adicional para las demás funciones recursivas: eliminación en lista vacía, inversión recursiva, cancelar y deshacer, prioridad estable, colisiones hash, redimensionamiento, recorrido inorden y eliminación de la raíz del BST con dos hijos.
