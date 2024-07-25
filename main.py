import pyaudio
import wave
import threading
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk

recording = False
frames = []
stream = None

def file_path():
    global add
    add = askdirectory()
    print(add)

def save_audio(filename):
    global frames
    p = pyaudio.PyAudio()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    p.terminate()

def record_audio():
    global recording, frames
    recording = True
    frames = []
    p = pyaudio.PyAudio()
    global stream
    stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)

    def record():
        if recording:
            data = stream.read(1024)
            frames.append(data)
            root.after(10, record)

    record()

def start_recording():
    global recording
    if not recording:
        threading.Thread(target=record_audio).start()
        showinfo(title="Recording", message="Recording Started")

def stop_recording():
    global recording
    if recording:
        recording = False
        stream.stop_stream()
        stream.close()
        p.terminate()
        filename = add + "/output.wav"
        save_audio(filename)
        showinfo(title="Recording", message="Recording Stopped")

def main_window():
    global root
    root = Tk()
    root.title("Audio Recorder")
    root.geometry("390x390")
    root.resizable(False, False)
    root.config(bg="lightblue")

    # Open and resize the image
    img1 = Image.open("music.png")
    img1 = img1.resize((310, 100))
    img1 = ImageTk.PhotoImage(img1)

    l1 = Label(root, image=img1, bg="lightblue")
    l1.place(x=45, y=20, height=100, width=310)

    b1 = Button(root, text="Path", font=("Time New Roman", 15), command=file_path, bg="gray", fg="black")
    b1.place(x=120, y=130, height=30, width=150)

    img2 = Image.open("record.png")
    img2 = img2.resize((70, 70))
    img2 = ImageTk.PhotoImage(img2)
    start = Button(root, image=img2, command=start_recording, bg="white", fg="red")
    start.place(x=50, y=180, height=80, width=130)

    stop = Button(root, text="Stop", font=("Time New Roman", 15), command=stop_recording, bg="red", fg="white")
    stop.place(x=210, y=180, height=80, width=130)

    root.mainloop()

main_window()
