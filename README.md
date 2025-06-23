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

1. **Python 3** (3.8 o superior)
2. **pip3** para gestión de paquetes Python
3. **Mininet** para emulación de redes
4. **Open vSwitch** para switches virtuales
5. **git** para clonar dependencias

### Instalación de Dependencias del Sistema (Ubuntu/Debian)

```bash
# Actualizar repositorios
sudo apt-get update

# Instalar dependencias básicas
sudo apt-get install python3 python3-pip python3-venv git

# Instalar Mininet
sudo apt-get install mininet

# Instalar Open vSwitch
sudo apt-get install openvswitch-switch

# Alternativamente, para instalación completa de Mininet:
# git clone https://github.com/mininet/mininet.git
# cd mininet && sudo ./util/install.sh -a
```

## Comandos para Migración de Docker a Virtual Environment

### 1. Hacer ejecutables los scripts:
```bash
chmod +x setup_environment.sh
chmod +x src/scripts/run_all.sh
chmod +x src/scripts/run_pox.sh
chmod +x src/scripts/run_mininet.sh
```

### 2. Eliminar archivos de Docker (si migras desde versión Docker):
```bash
# Eliminar docker-compose.yml
rm docker-compose.yml

# Eliminar toda la carpeta docker y su contenido
rm -rf docker/
```

### 3. Ejecutar la configuración inicial (solo la primera vez):
```bash
./setup_environment.sh
```

## Cómo ejecutar

### 1. Configuración inicial del entorno

```bash
# Hacer ejecutable el script de configuración
chmod +x setup_environment.sh

# Ejecutar configuración (solo la primera vez)
./setup_environment.sh
```

Este script:
- Crea un entorno virtual Python
- Instala las dependencias Python necesarias
- Clona el controlador POX
- Configura los archivos del controlador

### 2. Ejecución del proyecto

#### Opción A: Ejecutar todo automáticamente
```bash
# Ejecutar controlador y topología juntos
chmod +x src/scripts/run_all.sh
./src/scripts/run_all.sh
```

#### Opción B: Ejecutar por separado

1. **Ejecutar el controlador POX**:
```bash
chmod +x src/scripts/run_pox.sh
./src/scripts/run_pox.sh
```

2. **En una nueva terminal, ejecutar Mininet**:
```bash
chmod +x src/scripts/run_mininet.sh
./src/scripts/run_mininet.sh
```

### 3. Comandos adicionales útiles

```bash
# Para limpiar Mininet si hay problemas
sudo mn -c

# Para reiniciar Open vSwitch si es necesario
sudo service openvswitch-switch restart

# Para activar manualmente el entorno virtual
source venv/bin/activate
```

### 4. Limpieza (si es necesario)

```bash
# Limpiar interfaces de red de Mininet
sudo mn -c

# Reiniciar Open vSwitch si hay problemas
sudo service openvswitch-switch restart
```

## Estructura del Proyecto

```
├── src/
│   ├── controller/        # Código del controlador POX
│   ├── topologies/        # Topologías de red para Mininet  
│   └── scripts/          # Scripts de ejecución
├── venv/                 # Entorno virtual (generado automáticamente)
├── pox/                  # Controlador POX (clonado automáticamente)
├── requirements.txt      # Dependencias Python
├── setup_environment.sh  # Script de configuración inicial
└── README.md
```

## Notas Importantes

- **Primera ejecución**: Siempre ejecutar `./setup_environment.sh` antes del primer uso
- **Permisos**: Los scripts necesitan permisos de ejecución (`chmod +x`)
- **Sudo**: Mininet requiere permisos de administrador para crear interfaces de red
- **Limpieza**: Usar `sudo mn -c` para limpiar interfaces de Mininet entre ejecuciones
- **Entorno virtual**: Las dependencias Python se instalan en `venv/` y no afectan el sistema
- **Actualización importante**: Si actualizas los archivos del controlador, re-ejecuta `./setup_environment.sh` para actualizar los archivos en POX

## Resolución de Problemas

### Error: "ModuleNotFoundError: No module named 'pox.switch_controller'"

Este error indica que los archivos del controlador no están correctamente copiados a POX. Para solucionarlo:

```bash
# Re-ejecutar el script de configuración
./setup_environment.sh
```

### Error: "No module named 'pox.custom.firewall'"

Similar al anterior, ejecutar:

```bash
# Asegurar que todos los archivos estén actualizados
./setup_environment.sh
```



