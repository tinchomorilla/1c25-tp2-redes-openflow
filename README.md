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

### Instalación de Dependencias del Sistema (Ubuntu/Debian)

```bash
# Actualizar repositorios
sudo apt-get update

# Instalar dependencias básicas
sudo apt-get install python3 python3-pip python3-venv git

# Instalar Python 2.7 (recomendado para POX)
sudo apt-get install python2.7 python2.7-dev

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
chmod +x setup_sudoers.sh
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

### 4. [OPCIONAL] Configurar sudoers para evitar prompts de password:
```bash
./setup_sudoers.sh
```

## Cómo ejecutar

### 1. Configuración inicial del entorno

```bash
# Hacer ejecutables los scripts de configuración
chmod +x setup_environment.sh
chmod +x setup_sudoers.sh

# Ejecutar configuración (solo la primera vez)
./setup_environment.sh

# [OPCIONAL] Configurar sudoers para evitar password prompts
./setup_sudoers.sh
```

### 2. Ejecución del proyecto

#### Opción A: Ejecutar todo automáticamente (RECOMENDADO)
```bash
# Ejecutar controlador y topología juntos CON CLEANUP AUTOMÁTICO
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

# Para matar procesos POX si quedan colgados
pkill -f "pox.py"

# Para liberar el puerto 6633 si está ocupado
sudo fuser -k 6633/tcp
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
├── setup_sudoers.sh      # Script para configurar sudoers (opcional)
└── README.md
```

## Mejoras Incluidas

### ✅ Cleanup Automático
- **Scripts individuales**: Cada script (run_pox.sh, run_mininet.sh) hace su propio cleanup
- **Eliminación de procesos**: Mata procesos POX y Mininet existentes
- **Liberación de puertos**: Libera el puerto 6633 (OpenFlow) automáticamente
- **Limpieza de redes**: Elimina interfaces y bridges de Mininet previos

### ✅ Compatibilidad de Python
- **POX**: Detecta y usa Python 2.7 automáticamente (evita warnings)
- **Mininet**: Usa Python 3 con PYTHONPATH configurado correctamente
- **Fallback**: Si no hay Python 2.7, usa Python 3 con advertencia

### ✅ Gestión de Permisos
- **Script sudoers**: setup_sudoers.sh configura permisos automáticamente
- **Sin password prompts**: Una vez configurado, no pide contraseñas
- **Seguridad**: Solo permite comandos específicos de red sin password

## Notas Importantes

- **Primera ejecución**: Siempre ejecutar `./setup_environment.sh` antes del primer uso
- **Permisos**: Los scripts necesitan permisos de ejecución (`chmod +x`)
- **Sudo**: Mininet requiere permisos de administrador para crear interfaces de red
- **Limpieza**: Los scripts incluyen cleanup automático, pero puedes usar `sudo mn -c` manualmente
- **Entorno virtual**: Las dependencias Python se instalan en `venv/` y no afectan el sistema
- **Actualización importante**: Si actualizas los archivos del controlador, re-ejecuta `./setup_environment.sh` para actualizar los archivos en POX
- **Python 2.7**: Altamente recomendado para POX - elimina warnings de versión
- **Password prompts**: Ejecuta `./setup_sudoers.sh` una vez para evitar prompts repetitivos

## Resolución de Problemas

### Error: "Address already in use" (Puerto 6633)

Los scripts ahora incluyen cleanup automático, pero si persiste:

```bash
# Liberar puerto manualmente
sudo fuser -k 6633/tcp

# O reiniciar completamente
./src/scripts/run_all.sh
```

### Error: "ModuleNotFoundError: No module named 'src'"

Los scripts configuran PYTHONPATH automáticamente, pero si persiste:

```bash
# Re-ejecutar setup
./setup_environment.sh

# Verificar PYTHONPATH manualmente
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### Warnings de versión de Python en POX

```bash
# Instalar Python 2.7
sudo apt-get install python2.7 python2.7-dev

# Re-ejecutar setup
./setup_environment.sh
```

### Prompts de password constantes

```bash
# Configurar sudoers una sola vez
chmod +x setup_sudoers.sh
./setup_sudoers.sh
```



