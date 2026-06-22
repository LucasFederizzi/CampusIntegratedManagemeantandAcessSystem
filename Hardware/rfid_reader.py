"""
Raspberry Pi + Arduino + RFID - Setup Completo
Lê RFID via Serial (Arduino) e envia ao Backend
"""

import serial
import time
from datetime import datetime
import requests
import json
from config import BACKEND_URL, BACKEND_TIMEOUT, SERIAL_PORT, SERIAL_BAUD_RATE, SERIAL_TIMEOUT, SERIAL_READ_DELAY

# ===== CLASSE PARA GERENCIAR RFID =====
class RFIDReader:
    def __init__(self, port, baud_rate, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial = None
        self.running = False
    
    def connect(self):
        """Conecta ao Arduino via Serial"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=self.timeout
            )
            self.running = True
            print(f"✓ Conectado em {self.port} @ {self.baud_rate} baud")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar em {self.port}: {e}")
            return False
    
    def read_rfid(self):
        """Lê ID do cartão RFID do Arduino"""
        if not self.serial or not self.serial.is_open:
            return None
        
        try:
            if self.serial.in_waiting > 0:
                data = self.serial.readline().decode('utf-8').strip()
                return data if data else None
        except Exception as e:
            print(f"✗ Erro ao ler: {e}")
        
        return None
    
    def close(self):
        """Fecha conexão serial"""
        if self.serial:
            self.serial.close()
            self.running = False
            print("Conexão serial fechada")

# ===== CLASSE PARA ENVIAR AO BACKEND =====
class BackendSender:
    def __init__(self, url, timeout=5):
        self.url = url
        self.timeout = timeout
    
    def send_attendance(self, card_id, nome=None):
        """Envia presença para o backend"""
        payload = {
            "id": str(card_id),
            "nome": str(nome) if nome else "Usuário RFID",
            "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            response = requests.post(self.url, json=payload, timeout=self.timeout)
            
            if response.status_code == 201:
                data = response.json()
                print(f"✓ {card_id} registrado (PK: {data.get('pk')})")
                return True
            else:
                print(f"✗ Erro {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"✗ Não conseguiu conectar ao backend")
            return False
        except Exception as e:
            print(f"✗ Erro: {e}")
            return False

# ===== MAIN =====
def main():
    print("=== Campus Attendance System - RFID Reader ===\n")
    
    # Inicializar RFID
    rfid = RFIDReader(SERIAL_PORT, SERIAL_BAUD_RATE, SERIAL_TIMEOUT)
    if not rfid.connect():
        print("Abortando...")
        return
    
    # Inicializar Backend
    backend = BackendSender(BACKEND_URL, BACKEND_TIMEOUT)
    
    print(f"Aguardando leitura de cartões RFID...")
    print("(Pressione Ctrl+C para sair)\n")
    
    try:
        while rfid.running:
            card_id = rfid.read_rfid()
            
            if card_id:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Cartão lido: {card_id}")
                
                # Tentar enviar para backend
                backend.send_attendance(card_id)
                
                # Aguardar antes de ler próximo (evitar duplicata rápida)
                time.sleep(SERIAL_READ_DELAY)
            
            time.sleep(0.1)  # CPU cool-down
    
    except KeyboardInterrupt:
        print("\n\nEncerrando...")
    finally:
        rfid.close()
        print("Programa finalizado")

if __name__ == "__main__":
    main()
