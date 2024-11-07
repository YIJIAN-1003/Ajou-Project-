import socket
import select

# 클라이언트 소켓을 처리할 파생 클래스
class ClientHandler:
    def __init__(self, clntSock, clntAddr):
        self.clntSock = clntSock
        self.clntAddr = clntAddr
        print(f"New connection from {clntAddr}")

    def handle_read(self):
        """클라이언트로부터 메시지를 읽고 즉시 처리"""
        try:
            data = self.clntSock.recv(1024)
            if data: # 클라이언트로 부터 메시지 수신
                print(f"Received '{data.decode()}' from {self.clntAddr}")
                self.clntSock.send(data)           # 받은 데이터 클라이언트에게 전송 (에코)
            else: # 클라이언트가 연결을 끊은 경우
                print(f"Closing connection to {self.clntAddr}")
                return False
        except ConnectionResetError:
            print(f"Connection reset by {self.clntAddr}")
            return False
        return True

    def close(self): # 클라이언트 연결 종료
        print(f"Connection closed with {self.clntAddr}")
        self.clntSock.close()

# select 서버 실행 함수
def tcp_select_server(host='127.0.0.1', port=9999, timeout=5):
    # 서버 소켓 생성
    servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servSock.bind((host, port))
    servSock.listen(5)
    print(f"Server listening on {host}:{port}")

    # select용 소켓 목록
    inputs = [servSock]  # 읽기 가능한 소켓 리스트
    client_handlers = {}      # 클라이언트 소켓과 ClientHandler 매핑

    while inputs:
        # select로 소켓 상태 모니터링
        readable, _, exceptional = select.select(inputs, [], inputs, timeout)

        if not (readable or exceptional):
            # 타임아웃 발생 시 처리 (필요 시 로그 등 추가 가능)
            print("Select timed out, continuing...")
            continue
        
        # 읽을 준비가 된 소켓 처리
        for s in readable:
            if s is servSock:
                # 새로운 클라이언트 연결 수락
                clntSock, clntAddr = servSock.accept()
                handler = ClientHandler(clntSock, clntAddr)
                client_handlers[clntSock] = handler
                inputs.append(clntSock)
            else:
                # 기존 클라이언트 데이터 처리
                handler = client_handlers[s]
                if not handler.handle_read():
                    close_client(s, inputs, client_handlers)

        # 예외 소켓 처리
        for s in exceptional:
            close_client(s, inputs, client_handlers)

# 클라이언트 연결을 닫는 함수
def close_client(clntSock, inputs, client_handlers):
    """클라이언트 소켓을 닫고 리스트에서 제거"""
    handler = client_handlers.pop(clntSock, None)
    if handler:
        handler.close()
    if clntSock in inputs:
        inputs.remove(clntSock)

if __name__ == "__main__":
    tcp_select_server()
