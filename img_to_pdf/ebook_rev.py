import sys
import os
import pyautogui
import time
from pynput import mouse
from PIL import Image

picture_size = []  # 왼쪽 상단 좌표 , 오른쪽 하단 좌표
next_page = []  # 다음 페이지의 좌표


def get_mouse_point(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        # print('입력받은 좌표: ', (x, y))
        picture_size.append(x)
        picture_size.append(y)
    return False


def get_next_page(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        # print('입력받은 좌표 : ', (x, y))
        next_page.append(x)
        next_page.append(y)
    return False


def page_input():
    page = int(input("페이지 수를 입력하세요 : "))
    return page


def start_point_input():
    print("좌측 상단 좌표를 클릭하세요.")
    with mouse.Listener(on_click=get_mouse_point) as listener:
        listener.join()
        msg = "좌측 상단 좌표 : (%s, %s)" % (picture_size[0], picture_size[1])
        print(msg)
    return


def end_point_input():
    print("우측 하단 좌표를 클릭하세요")
    with mouse.Listener(on_click=get_mouse_point) as listener:
        listener.join()
        msg = "우측 하단 좌표 : (%s, %s)" % (picture_size[2], picture_size[3])
        print(msg)


def next_page_input():
    print("다음페이지 버튼을 클릭하세요")
    with mouse.Listener(on_click=get_next_page) as listener:
        listener.join()
        msg = "다음페이지 좌표 : (%s, %s)" % (next_page[0], next_page[1])
        print(msg)


def get_picture(path, page):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError:
        print("Error: Failed to create the directory.")
    for i in range(page):
        if len(picture_size) >= 4:
            pyautogui.screenshot(path + "/%s.png" % i, region=(picture_size[0], picture_size[1],
                                                               picture_size[2] - picture_size[0],
                                                               picture_size[3] - picture_size[1]))
        pyautogui.click(*next_page)
        time.sleep(0.8)


def png_to_pdf(input_path, page, dir_name):

    file_list = os.listdir(input_path)
    png_files = [file for file in file_list if file.lower().endswith('.png')]

    png_files = sorted(png_files)
    png_files.sort(key=lambda x: int(x.split('.')[0]))
    print(png_files)

    img_list = []
    img_path = input_path + '/' + png_files[0]
    # print(img_path)

    im_buf = Image.open(img_path)
    cvt_rgb_0 = im_buf.convert('RGB')

    for i in png_files:
        img_path = input_path + '/' + i
        # print(img_path)
        im_buf = Image.open(img_path)
        cvt_rgb = im_buf.convert('RGB')
        img_list.append(cvt_rgb)
    pdf_path = input_path + '/' + dir_name + '.pdf'
    del img_list[0]
    cvt_rgb_0.save(pdf_path, save_all=True, append_images=img_list)


def main():
    page = 0  # 찍을 페이지 수
    dir_name = str(input('디렉토리명을 입력해주세요.(현재 디렉토리에 생성 됩니다 - 영문 or 숫자 추천) : '))
    curr_path = os.getcwd()
    input_path = os.path.join(curr_path, dir_name)

    page = page_input()

    start_point_input()
    time.sleep(0.5)
    end_point_input()
    time.sleep(0.5)
    next_page_input()
    # print(dir_name)

    get_picture(input_path, page)
    pdf_choice = input("이미지를 PDF로 저장하시겠습니까? (yes/no) : ")
    if pdf_choice.lower() == 'yes':
        png_to_pdf(input_path, page, dir_name)
        print('pdf파일이 ', input_path, "에 저장되었습니다.")
    elif pdf_choice.lower() == 'no':
        print("감사합니다.")
    else:
        exit()


if __name__ == '__main__':
    sys.exit(main() or 0)
