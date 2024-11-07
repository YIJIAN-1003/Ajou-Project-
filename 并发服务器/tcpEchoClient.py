import socket

# 서버의 IP 주소와 포트 설정
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12346
BUFFER_SIZE = 1024

# 클라이언트 소켓 생성 (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((SERVER_IP, SERVER_PORT))

while True:
    # 사용자로부터 입력 받기
    message = input("서버에 보낼 메시지를 입력하세요 ('exit' 입력 시 종료): ")

    if message.lower() == 'exit':
        print("클라이언트를 종료합니다.")
        break

    # 서버로 메시지 전송
    client_socket.sendall(message.encode())

    # 서버로부터 에코 메시지 수신
    data = client_socket.recv(BUFFER_SIZE)
    print(f"서버로부터 받은 에코 메시지: {data.decode()}")

# 소켓 닫기
client_socket.close()
