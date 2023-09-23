import tkinter as tk
import random
import cv2
from tkinter import messagebox
import os, shutil
import ultralytics
from ultralytics import YOLO
import pathlib
import csv
import datetime
def start_program():
    exel=[]
    filename = "Данные.csv"
    f = open(filename, "w+")
    f.close()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    my_folder = (str(current_dir) + '/video')
    isExist = os.path.exists(my_folder)
    if isExist == False:
        os.mkdir("video")
    files = os.listdir(my_folder)
    video_files = (list(pathlib.Path(my_folder).glob('*.mp4'))) or (list(pathlib.Path(my_folder).glob('*.AVI')))
    k=0
    if len(video_files)<1:
        messagebox.showinfo('Контроль Внимания', 'В папке нет видео.')
    else:
        messagebox.showinfo('Контроль Внимания', 'Процесс пошел, после его окончания данные выгрузятся в "Данные.csv"')
        exit_program()
        for file in range(len(video_files)):
            namef = []
            kol = []
            timecode = []
            path = video_files[file]
            name = os.path.basename(path)
            cap = cv2.VideoCapture('video/'+name)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames == 0:
                messagebox.showinfo('Контроль Внимания', 'Программе не удалось открыть видео ' + str(name))
                exit_program()
            fps = cap.get(cv2.CAP_PROP_FPS)
            my_file = open("coco.txt", "r")
            data = my_file.read()
            class_list = data.split("\n")
            my_file.close()
            detection_colors = []
            for i in range(len(class_list)):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                detection_colors.append((b, g, r))
            model = YOLO("yolov8x.pt")
            oldtime = -9
            k = 0
            tot = []
            final = []
            frame_pos = 0
            while frame_pos < total_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
                ret, frame = cap.read()
                if ret:
                    if not ret:
                        break
                    if not cap.isOpened():
                        exit()
                    while True:
                        detect_params = model.predict(source=[frame], conf=0.45, save=False)
                        DP = detect_params[0].numpy()
                        if len(DP) != 0:
                            for i in range(len(detect_params[0])):
                                boxes = detect_params[0].boxes
                                box = boxes[i]
                                clsID = box.cls.numpy()[0]
                                conf = box.conf.numpy()[0]
                                bb = box.xyxy.numpy()[0]
                                cv2.rectangle(
                                    frame,
                                    (int(bb[0]), int(bb[1])),
                                    (int(bb[2]), int(bb[3])),
                                    detection_colors[int(clsID)],
                                    3,
                                )
                                font = cv2.FONT_HERSHEY_COMPLEX
                                if 'cell phone' in class_list[int(clsID)]:
                                    cv2.imwrite("amg/frame" + str(frame_pos) + ".jpg", frame)
                                    cv2.putText(
                                        frame,
                                        class_list[int(clsID)] + " " + str(round(conf, 2)) + "%",
                                        (int(bb[0]), int(bb[1]) - 10),
                                        font,
                                        1,
                                        (255, 255, 255),
                                        2,
                                    )
                                    time = int(frame_pos) / int(fps)
                                    if int(time) - int(oldtime) > 15:
                                        tot.append(str(datetime.timedelta(seconds=time)))
                                    oldtime = time
                        break
                frame_pos += 60

            final = {'filename': name, 'cases_count': len(tot), 'timestamps': tot}
            exel.append(final)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            my_folder = (str(current_dir) + '/amg')
            for filename in os.listdir(my_folder):
                file_path = os.path.join(my_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print()
        csv_file = 'Данные.csv'
        with open(csv_file, 'a', newline='') as csvfile:
            fieldnames = ['filename', 'cases_count', 'timestamps']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for log in range(len(exel)):
                kot=exel[log]
                writer.writerow(kot)
    cap.release()
    messagebox.showinfo('Контроль Внимания', 'Программа завершила поиск' + str(name))
    exit_program()
k=0
def start():

    start_program()
def openp():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    my_folder = (str(current_dir) + '/video')
    isExist = os.path.exists(my_folder)
    if isExist == True:
        os.startfile(my_folder)
    else:
        os.mkdir("video")
        os.startfile(my_folder)
def exit_program():
    window.destroy()
def clicked():
    messagebox.showinfo('Контроль Внимания', 'Убедитесь что вы переместили файлы в папку video. Если не переместили, можете нажать кнопку "Путь к папке"')
window = tk.Tk()
window.title("Контроль Внимания")
window.geometry('1024x512')
window.resizable(width=False, height=False)

window.image = tk.PhotoImage(file='fon.png')
window.iconphoto(False, tk.PhotoImage(file='ico.png'))
bg_logo = tk.Label(window, image=window.image)
bg_logo.grid(row=0, column=0)

clicked()

label = tk.Label(window, text="Vigilance Control")
label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

start_button = tk.Button(window, text="Путь к папке", bg='dark grey', fg='red', font=('Segoe UI Light', 20, 'bold'),
                             command=openp)
start_button.place(anchor=tk.CENTER, y=-100, relx=0.5, rely=0.5)

start_button = tk.Button(window, text="Начать поиск телефонов", bg='dark grey', fg='red', font=('Segoe UI Light', 20, 'bold'),
                             command=start)
start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create the Exit program button
exit_button = tk.Button(window, text="Выход",  bg='dark grey', fg='red', font=('Segoe UI Light', 20, 'bold'), command=exit_program)
exit_button.place(anchor=tk.CENTER, y=100, relx=0.5, rely=0.5)

# Start the main loop
window.mainloop()