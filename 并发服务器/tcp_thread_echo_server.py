import socket
import threading

# 클라이언트 처리를 위한 파생 클래스 스레드
class ClientThread(threading.Thread):
    def __init__(self, clntSock, clntAddr):
        super().__init__()
        self.clntSock = clntSock
        self.clntAddr = clntAddr
        print(f"New connection from {self.clntAddr}")

    # 스레드가 실행될 때 호출되는 메소드
    def run(self):
        while True:
            try:
                # 클라이언트로부터 메시지 수신
                message = self.clntSock.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received from {self.clntAddr}: {message}")
                
                # 클라이언트에게 메시지 다시 전송 (Echo server)
                self.clntSock.send(f"Echo: {message}".encode('utf-8'))
            except ConnectionResetError:
                print(f"Connection lost with {self.clntAddr}")
                break

        # 연결 종료
        print(f"Connection closed with {self.clntAddr}")
        self.clntSock.close()

# 서버 소켓 설정
def tcp_thread_server(host='127.0.0.1', port=9999):
    # 소켓 생성 (IPv4, TCP 사용)
    servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSock.bind((host, port))

    # 클라이언트 접속을 대기 (최대 5개 동시 연결 대기)
    servSock.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # 클라이언트의 연결 요청을 수락
        clntSock, clntAddr = servSock.accept()

        # ClientThread 파생 클래스 인스턴스 생성 및 스레드 시작
        tclnt = ClientThread(clntSock, clntAddr)
        tclnt.start()

if __name__ == "__main__":
    # 서버 시작
    tcp_thread_server()
