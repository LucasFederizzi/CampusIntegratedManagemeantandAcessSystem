# ===== CONFIGURAÇÃO DO SISTEMA =====
# Edite este arquivo para configurar os IPs e portas

# IP ou hostname do Backend (onde app.py está rodando)
BACKEND_HOST = "192.168.1.100"
BACKEND_PORT = 5000
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/presenca"

# RabbitMQ (se usar fila de mensagens)
RABBITMQ_HOST = "192.168.1.100"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = "presencas"

# Conexão Serial (Arduino RFID)
SERIAL_PORT = "/dev/ttyUSB0"  # /dev/ttyACM0 no Linux, COM3 no Windows
SERIAL_BAUD_RATE = 9600
SERIAL_TIMEOUT = 1

# Timeouts
BACKEND_TIMEOUT = 5
SERIAL_READ_DELAY = 1  # segundos entre leituras
