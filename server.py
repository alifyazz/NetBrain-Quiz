import socket
import threading
import random

HOST = '127.0.0.1'
PORT = 5555

clients = {}
scores = {}

questions = [
    {
        "question": "Apa kepanjangan dari TCP?",
        "answer": "transmission control protocol"
    },
    {
        "question": "Port default HTTP adalah?",
        "answer": "80"
    },
    {
        "question": "Layer OSI ke-3 adalah?",
        "answer": "network"
    },
    {
        "question": "Protokol untuk transfer file adalah?",
        "answer": "ftp"
    },
    {
        "question": "Perintah ping menggunakan protokol?",
        "answer": "icmp"
    }
]

lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    # LOGIN USERNAME
    while True:
        conn.sendall(b"Masukkan username: ")
        username = conn.recv(1024).decode().strip()

        with lock:
            if username not in clients:
                clients[username] = conn
                scores[username] = 0
                conn.sendall(b"LOGIN_BERHASIL\n")
                break
            else:
                conn.sendall(b"USERNAME_SUDAH_DIGUNAKAN\n")

    # QUIZ
    # Buat salinan pertanyaan dan acak
    client_questions = questions[:]
    random.shuffle(client_questions)
    
    for q in client_questions:
        conn.sendall(q["question"].encode())
        answer = conn.recv(1024).decode().lower().strip()

        if answer == q["answer"]:
            scores[username] += 10
            conn.sendall(b"Jawaban benar!\n")
        else:
            conn.sendall(b"Jawaban salah!\n")

    result = f"Skor akhir kamu: {scores[username]}"
    conn.sendall(result.encode())

    # CLEAN UP
    with lock:
        del clients[username]

    conn.close()
    print(f"[DISCONNECTED] {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER RUNNING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start_server()
