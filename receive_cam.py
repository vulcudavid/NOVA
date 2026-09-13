import socket
import struct
import time
import os

ESP32_MAC = "20:9B:A9:73:9C:F2"
PORT = 1

def connect_to_esp32():
    while True:
        try:
            print(f"[BT] Incerc conectarea la ESP32-CAM ({ESP32_MAC})...")
            sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            sock.connect((ESP32_MAC, PORT))
            print("[BT] Conectat cu succes!")
            return sock
        except Exception as e:
            print(f"[EROARE] Conectare esuata: {e}. Reincerc in 3 secunde...")
            time.sleep(3)

def recv_exact(sock, num_bytes):
    """Citeste exact numarul specificat de octeti din socket."""
    buf = bytearray()
    while len(buf) < num_bytes:
        chunk = sock.recv(num_bytes - len(buf))
        if not chunk:
            return None
        buf.extend(chunk)
    return bytes(buf)

def main():
    os.makedirs("capturi", exist_ok=True)
    sock = connect_to_esp32()
    img_index = 0

    try:
        while True:
            # 1. Citim lungimea imaginii (4 octeti, uint32 little-endian)
            raw_len = recv_exact(sock, 4)
            if raw_len is None:
                print("[WARN] Conexiunea s-a intrerupt. Reconectare...")
                sock.close()
                sock = connect_to_esp32()
                continue

            img_len = struct.unpack("<I", raw_len)[0]

            # 2. Citim imaginea JPEG completa
            img_bytes = recv_exact(sock, img_len)
            if img_bytes is None:
                print("[WARN] Date incomplete receptionate. Reconectare...")
                sock.close()
                sock = connect_to_esp32()
                continue

            img_index += 1
            filename = f"capturi/imagine_{img_index:04d}.jpg"
            
            # Salvam ultima poza
            with open(filename, "wb") as f:
                f.write(img_bytes)

            # Salvam si o copie ca 'latest.jpg' pentru acces facil
            with open("capturi/latest.jpg", "wb") as f:
                f.write(img_bytes)

            print(f"[OK] Primit cadru #{img_index:04d} - Dimensiune: {img_len} bytes -> {filename}")

    except KeyboardInterrupt:
        print("\n[INFO] Oprire la cererea utilizatorului...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
