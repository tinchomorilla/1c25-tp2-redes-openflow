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

## Configuración del Entorno

### Prerrequisitos

Este proyecto requiere las siguientes dependencias del sistema:

1. **Python 3** (3.8 o superior) - para Mininet y entorno virtual
2. **Python 2.7** (recomendado) - para POX controller (evita warnings)
3. **pip3** para gestión de paquetes Python
4. **Mininet** para emulación de redes
5. **Open vSwitch** para switches virtuales
6. **git** para clonar dependencias


## Comandos para crear el Virtual Environment apropiadamente

### 1. Hacer ejecutables los scripts:
```bash
chmod +x setup_environment.sh
chmod +x setup_sudoers.sh
chmod +x src/scripts/run_all.sh
chmod +x src/scripts/run_pox.sh
chmod +x src/scripts/run_mininet.sh
```


## Cómo ejecutar

### 1. Configuración inicial del entorno

```bash
# Ejecutar configuración (solo la primera vez)
sudo ./setup_environment.sh

# [RECOMENDADO] Configurar sudoers para evitar password prompts
sudo ./setup_sudoers.sh
```

### 2. Ejecución del proyecto

**IMPORTANTE**: Ejecutar cada script en una terminal separada:

#### Terminal 1: Controlador POX
```bash
./src/scripts/run_pox.sh
```

#### Terminal 2: Mininet (después de que el controlador esté corriendo)
```bash
./src/scripts/run_mininet.sh
```




