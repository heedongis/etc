import threading
import queue
import time

# 스레드 세이프한 큐 생성
data_queue = queue.Queue()

# 사용자 입력을 처리하는 함수
def input_thread_function():
    while True:
        try:
            if data_queue.empty():
                user_input = input("숫자를 입력하세요 : ")

                if user_input:
                    data_queue.put(user_input)  # 큐에 숫자 추가

        except ValueError:
            print("유효한 숫자를 입력해주세요.")

# 큐에서 데이터를 읽고 출력하는 함수
def output_thread_function():
    while True:
        try:
            # 큐에서 데이터 가져오기 (데이터가 없으면 여기서 블록됨)
            number = data_queue.get_nowait()
            print(f"큐에서 꺼낸 숫자: {number}")
        except queue.Empty:
            # 큐가 비어있으면 잠시 대기
            time.sleep(0.5)
            print(f"큐 대기중")

# 스레드 생성 및 시작
input_thread = threading.Thread(target=input_thread_function, )
output_thread = threading.Thread(target=output_thread_function)

input_thread.start()
output_thread.start()

# 메인 스레드가 종료되면 모든 스레드가 종료되도록 설정
input_thread.join()
output_thread.join()
