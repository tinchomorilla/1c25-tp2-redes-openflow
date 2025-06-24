# TP2 - Redes - OpenFlow

## Resumen Ejecutivo

Este proyecto implementa una red definida por software (SDN) utilizando OpenFlow como protocolo de comunicación entre switches y controlador. Se desarrolló un controlador personalizado con funcionalidades de switch learning y firewall para demostrar el control centralizado de flujos de red en una topología lineal virtualizada con Mininet.

## Marco Teórico

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

## Arquitectura del Sistema

### Estructura del Proyecto

```
src/
├── controller/               # Módulo del controlador SDN
│   ├── main.py              # Punto de entrada del controlador POX
│   ├── switch_controller.py # Implementación del switch learning
│   ├── firewall.py         # Implementación del firewall
│   └── rules.json          # Configuración de reglas de firewall
├── topologies/             # Configuración de topologías de red
│   ├── main.py            # Ejecutor principal de topologías
│   ├── linear_topology.py # Implementación de topología lineal
│   └── rule_tester.py     # Suite de pruebas para reglas de firewall
├── utils/                 # Utilidades y configuración
│   ├── constants.py      # Constantes del sistema (DEFAULT_SWITCHES, DEFAULT_RULE)
│   └── logger.py         # Sistema de logging
└── scripts/              # Scripts de ejecución
    ├── run_pox.sh       # Lanzador del controlador POX
    └── run_mininet.sh   # Lanzador de Mininet
```

### Componentes Principales

#### 1. Controlador SDN (`src/controller/`)

- **`main.py`**: Punto de entrada para POX que inicializa el controlador con las reglas especificadas
- **`switch_controller.py`**: Implementa funcionalidad de switch learning con aprendizaje automático de MACs
- **`firewall.py`**: Implementa reglas de filtrado de tráfico basadas en IPs, puertos y protocolos
- **`rules.json`**: Configuración de reglas de firewall que incluye:
  - Bloqueo de tráfico HTTP (puerto 80) para TCP y UDP
  - Bloqueo de tráfico UDP desde h1 al puerto 5001
  - Bloqueo total de comunicación entre h2 y h3

#### 2. Archivo de Configuración (`src/utils/constants.py`)

Define parámetros globales del sistema:
- `DEFAULT_SWITCHES = 3`: Número por defecto de switches en la topología
- `DEFAULT_RULE = "R2"`: Regla por defecto para pruebas automáticas

#### 3. Topologías de Red (`src/topologies/`)

- **`linear_topology.py`**: Crea una topología lineal con n switches interconectados
- **`main.py`**: Orquesta la creación de la red y permite especificar número de switches y reglas a probar
- **`rule_tester.py`**: Ejecuta pruebas automáticas para verificar el funcionamiento de las reglas de firewall

## Configuración del Entorno

### Prerrequisitos del Sistema

Este proyecto requiere las siguientes dependencias:

1. **Python 3** (3.8 o superior) - para Mininet y entorno virtual
2. **Python 2.7** (recomendado) - para POX controller (evita warnings)
3. **pip3** para gestión de paquetes Python
4. **Mininet** para emulación de redes
5. **Open vSwitch** para switches virtuales
6. **git** para clonar dependencias

### Instalación y Configuración

#### 1. Configuración Inicial del Entorno

```bash
# Hacer ejecutables los scripts
chmod +x setup_environment.sh setup_sudoers.sh src/scripts/*.sh

# Ejecutar configuración (solo la primera vez)
sudo ./setup_environment.sh

# [RECOMENDADO] Configurar sudoers para evitar prompts de contraseña
sudo ./setup_sudoers.sh
```

#### 2. Verificación del Entorno

El script `test_environment.sh` verifica que todos los componentes estén correctamente instalados:

```bash
# Ejecutar pruebas de verificación
./test_environment.sh
```

Este script verifica:
- Existencia del entorno virtual Python
- Disponibilidad de Python 2.7 y Python 3
- Instalación de Mininet y Open vSwitch
- Configuración correcta de POX
- Permisos de ejecución de scripts
- Configuración de sudoers

## Procedimientos de Ejecución

### Método 1: Ejecución Manual (Recomendado para Desarrollo)

**IMPORTANTE**: Ejecutar cada script en una terminal separada para monitoreo independiente.

#### Terminal 1: Controlador POX
```bash
./src/scripts/run_pox.sh
```

**Funcionalidad del script `run_pox.sh`:**
- Verifica la existencia del entorno virtual y POX
- Limpia procesos previos de POX y libera el puerto 6633
- Detecta automáticamente la versión de Python más adecuada (prioriza Python 2.7)
- Carga las reglas desde `src/controller/rules.json`
- Lanza POX en una nueva terminal con logging detallado

#### Terminal 2: Mininet (después de que el controlador esté activo)
```bash
./src/scripts/run_mininet.sh
```

**Funcionalidad del script `run_mininet.sh`:**
- Verifica la conexión con el controlador POX en puerto 6633
- Limpia configuraciones previas de Mininet
- Lanza la topología con parámetros configurables

### Método 2: Ejecución con Parámetros Personalizados

#### Especificar Número de Switches
```bash
# Crear topología con 5 switches
python3 -m src.topologies.main 5
```

#### Ejecutar Pruebas Específicas de Reglas
```bash
# Probar regla R1 (bloqueo HTTP)
python3 -m src.topologies.main 3 --rule R1

# Probar regla R2 (bloqueo UDP específico)
python3 -m src.topologies.main 3 --rule R2

# Probar regla R3 (bloqueo h2-h3)
python3 -m src.topologies.main 3 --rule R3
```

## Escenarios de Prueba y Validación

### Configuración de Red por Defecto

- **h1**: 10.0.0.1
- **h2**: 10.0.0.2  
- **h3**: 10.0.0.3
- **h4**: 10.0.0.4
- **Switch de Firewall**: s2 (configurado en `rules.json`)

### Reglas de Firewall Implementadas

#### Regla R1: Bloqueo de Tráfico HTTP
**Descripción**: Bloquea todo el tráfico TCP y UDP al puerto 80
**Comando de prueba desde Mininet CLI**:
```bash
# Debe fallar
h1 wget -T 5 -t 1 h2:80
h1 nc -u h2 80
```

#### Regla R2: Bloqueo UDP Específico desde h1
**Descripción**: Bloquea tráfico UDP desde 10.0.0.1 al puerto 5001
**Comando de prueba desde Mininet CLI**:
```bash
# En h2, escuchar en puerto 5001
h2 nc -ul 5001 &

# Desde h1, debe fallar
h1 echo "test" | nc -u 10.0.0.2 5001

# Desde h3, debe funcionar
h3 echo "test" | nc -u 10.0.0.2 5001
```

#### Regla R3: Bloqueo Total h2-h3
**Descripción**: Impide toda comunicación entre h2 (10.0.0.2) y h3 (10.0.0.3)
**Comando de prueba desde Mininet CLI**:
```bash
# Todas estas comunicaciones deben fallar
h2 ping -c 3 h3
h3 ping -c 3 h2
h2 nc h3 22
```

### Pruebas Automáticas

El sistema incluye un conjunto de pruebas automáticas en `src/topologies/rule_tester.py` que se ejecutan al especificar el parámetro `--rule`:

```bash
# Ejecutar pruebas automáticas
python3 -m src.topologies.main 3 --rule R1  # Prueba automática de HTTP
python3 -m src.topologies.main 3 --rule R2  # Prueba automática de UDP
python3 -m src.topologies.main 3 --rule R3  # Prueba automática de bloqueo h2-h3
```

### Comandos de Verificación Manual en Mininet CLI

#### Verificar Conectividad General
```bash
# Probar conectividad básica (debe funcionar excepto donde hay reglas)
pingall

# Probar conectividad específica
h1 ping -c 3 h4
h4 ping -c 3 h1
```

#### Verificar Switch Learning
```bash
# El controlador debe aprender las MACs automáticamente
h1 ping h2
h2 ping h3
h3 ping h4
```

#### Verificar Funcionamiento del Firewall
```bash
# Comprobar que el switch s2 aplica las reglas correctamente
dpctl dump-flows tcp:127.0.0.1:6634
```

## Estructura de Archivos de Configuración

### `src/controller/rules.json`
Archivo principal de configuración del firewall que define:
- `firewall_switch`: Switch donde se aplican las reglas (ej: "s2")
- `rules`: Array de reglas con campos:
  - `rule`: Identificador único
  - `src_ip`, `dst_ip`: IPs origen y destino (opcional)
  - `dst_port`: Puerto destino (opcional)
  - `protocol`: "TCP" o "UDP" (opcional)
  - `description`: Descripción de la regla

### `src/utils/constants.py`
Define constantes del sistema:
- `DEFAULT_SWITCHES`: Número por defecto de switches (3)
- `DEFAULT_RULE`: Regla por defecto para pruebas ("R2")

## Solución de Problemas

### Problemas Comunes

#### Error: "Virtual environment not found"
```bash
sudo ./setup_environment.sh
```

#### Error: "Connection refused to 127.0.0.1:6633"
```bash
# Verificar que POX esté ejecutándose
./src/scripts/run_pox.sh
# Esperar a ver "Controller started" antes de ejecutar Mininet
```

#### Error: "POX warnings about Python version"
```bash
# Instalar Python 2.7
sudo apt-get install python2.7 python2.7-dev
```

#### Problemas de permisos con Mininet
```bash
sudo ./setup_sudoers.sh
```

### Limpieza del Sistema

```bash
# Limpiar configuraciones de Mininet
sudo mn -c

# Matar procesos de POX
pkill -f "pox.py"

# Liberar puerto 6633
sudo fuser -k 6633/tcp
```

## Logs y Depuración

- **Logs del Controlador**: Se muestran en la terminal donde se ejecuta POX
- **Logs de Mininet**: Se muestran en la terminal de Mininet
- **Logs Detallados**: El sistema utiliza el módulo `src/utils/logger.py` para logging estructurado

Para depuración avanzada, modificar el nivel de log en `run_pox.sh`:
```bash
# Cambiar --DEBUG por --INFO o --WARNING según necesidad
$PYTHON_CMD pox/pox.py log.level --DEBUG custom.main --rules_path=$RULES_PATH
```

## Consideraciones de Implementación

### Tecnologías Utilizadas
- **POX Framework**: Controlador SDN en Python
- **OpenFlow 1.0**: Protocolo de comunicación switch-controlador
- **Mininet**: Emulador de redes
- **Open vSwitch**: Implementación de switches virtuales

### Características del Sistema
- **Switch Learning**: Aprendizaje automático de direcciones MAC
- **Firewall Centralizado**: Reglas aplicadas desde el controlador
- **Topología Escalable**: Número configurable de switches
- **Pruebas Automatizadas**: Suite de testing integrada

Este proyecto demuestra los principios fundamentales de SDN y proporciona una base sólida para comprender la separación entre el plano de control y el plano de datos en redes modernas.




