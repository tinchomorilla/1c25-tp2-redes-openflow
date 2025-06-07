# TP2 - Redes - OpenFlow

## Teoría

### ¿Por qué es necesario un controlador?

En una red tradicional, cada switch o router decide por sí solo qué hacer con cada paquete. En cambio, en SDN (Software-Defined Networking), el controlador centraliza la lógica: los switches se vuelven "tontos" y delegan la decisión al controlador.

Entonces:
- El switch solo reenvía paquetes y obedece reglas.
- El controlador decide esas reglas (por ejemplo, "si viene de X, mandalo a Y").
- En este TP, se programa el controlador para decirle a los switches qué hacer.

### ¿Qué es POX?

POX es un framework en Python 2 para desarrollar controladores SDN.

- Permite escribir aplicaciones propias (como firewalls, switches, balanceadores) en Python.
- Utiliza su API para manejar eventos como conexiones de switches, paquetes entrantes, etc.
- Se utiliza POX para implementar el comportamiento deseado en la red.

### ¿Qué es OpenFlow?

OpenFlow es el protocolo de comunicación entre los switches y el controlador.

- Es lo que permite al controlador hablar con los switches.
- Permite decir: "Si ves un paquete con destino a IP X, mandalo por el puerto Y".
- Los switches avisan al controlador: "Recibí un paquete y no sé qué hacer con él, ¿me das instrucciones?"
