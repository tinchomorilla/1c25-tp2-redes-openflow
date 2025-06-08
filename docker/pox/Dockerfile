FROM sdn-project-base:latest

# Install POX with retry logic
RUN for i in {1..3}; do \
    git clone https://github.com/noxrepo/pox.git && \
    cd pox && \
    git checkout eel && \
    break || sleep 5; \
    done

# Copy the entire project
COPY . /app

# Set the working directory
WORKDIR /app

# Set the command to run POX directly
CMD ["python3", "src/pox/pox.py", "log.level", "--DEBUG", "controller.learning_switch"] 