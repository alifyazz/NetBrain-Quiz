import socket

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    message = client.recv(1024).decode()
    print(message)

    if "Masukkan username" in message:
        username = input("> ")
        client.sendall(username.encode())

    elif "USERNAME_SUDAH_DIGUNAKAN" in message:
        print("Username sudah dipakai, coba yang lain.")

    elif "LOGIN_BERHASIL" in message:
        print("Login berhasil!\n")
        break

# QUIZ LOOP
try:
    while True:
        message = client.recv(1024).decode()
        print(message)

        if "?" in message:
            answer = input("Jawaban: ")
            client.sendall(answer.encode())
        else:
            break
except:
    pass

client.close()
