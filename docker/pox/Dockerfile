# Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Dependencias base
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Cloná POX
RUN git clone https://github.com/noxrepo/pox.git /app/src/pox

# Copiá los archivos del controlador al lugar correcto dentro de POX
COPY src/controller/main.py /app/src/pox/pox/main.py
COPY src/controller/switch_controller.py /app/src/pox/pox/switch_controller.py
COPY src/controller/firewall.py /app/src/pox/pox/firewall.py

# También copiá el rules.json a una ruta accesible dentro del container
COPY src/controller/rules.json /app/src/pox/pox/rules.json

ENV PYTHONPATH=/app/src/pox

# Ejecutar POX con tu controlador
CMD ["python3", "src/pox/pox.py", "log.level", "--DEBUG", "main", "--rules_path=/app/src/pox/pox/rules.json"]
