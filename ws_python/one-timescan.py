import threading
import serial
import time
import queue
from pynput.keyboard import Controller
import tkinter as tk
from tkinter import simpledialog
from serial.tools import list_ports

# 데이터를 저장할 스레드 세이프한 큐 생성
data_queue = queue.Queue()

# 키보드 컨트롤러 초기화
keyboard = Controller()

# GUI를 사용하여 실제 포트와 가상 포트를 사용자에게 입력받는다
root = tk.Tk()
root.withdraw()  # 메인 창을 숨긴다

# 사용 가능한 COM 포트 목록을 가져온다
com_ports = list_ports.comports()

# "Barcode Scanner"가 포함된 포트를 검색한다
default_com_port = "COM1"  # 만약 찾지 못하면 기본값으로 사용될 포트
for port in com_ports:
    if "Barcode Scanner" in port.description:
        default_com_port = port.device
        break

# 실제 포트 설정
com_port = simpledialog.askstring("Input", "바코드 스캐너 포트를 입력하세요",
                                  initialvalue=default_com_port,
                                  parent=root)

# 시리얼 포트 설정
# ser = serial.Serial(com_port, 9600, timeout=1)  # 실제 포트, 9600 보레이트로 설정
ser = input("input barcode :")
# 가상 포트 설정
cnca_port = simpledialog.askstring("Input", "가상포트를 입력하세요",
                                   initialvalue="COM11",
                                   parent=root)

# CNCA0 포트로 연결
cnca = serial.Serial(cnca_port, 9600, timeout=1)

# 스레드에서 실행될 함수 정의 - 데이터 수신 및 처리
def serial_read_thread(ser):
    # global previous_data, start_time, last_send_time

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print("Received from COM5: ", line)
            previous_data = line

            keyboard.type(previous_data)
            keyboard.type('\n')
            print("Typed to keyboard and pressed Enter: ", previous_data)

            # 큐에 데이터 추가
            data_queue.put(previous_data)

        time.sleep(0.1)

# 스레드에서 실행될 함수 정의 - 데이터 전송
def serial_write_thread(cnca):
    while True:
        try:
            data_to_send = data_queue.get_nowait()
            cnca.write((data_to_send + '\r\n').encode('utf-8'))
            time.sleep(2.0)
            print("Sending barcode to center system: ", data_to_send)

        except queue.Empty:
            continue
        # 큐 작업 완료 표시
        data_queue.task_done()

        time.sleep(0.1)


# 스레드 생성 및 시작
read_thread = threading.Thread(target=serial_read_thread, args=(ser,))
write_thread = threading.Thread(target=serial_write_thread, args=(cnca,))

read_thread.start()
write_thread.start()


# 메인 스레드가 종료될 때 모든 스레드를 정상적으로 종료하기 위해 join을 호출
read_thread.join()
write_thread.join()
