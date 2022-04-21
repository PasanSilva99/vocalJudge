import os.path
import threading
import time
from pathlib import Path
from threading import Thread

from tkinter import *
from tkinter import filedialog as fd

import Seperator
import PitchDetection
# Explicit imports to satisfy Flake8
# from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Show the gui
def start_gui():
    window = Tk()

    window.geometry("740x315")
    window.configure(bg="#000000")

    # Base Canvas
    canvas = Canvas(
        window,
        bg="#000000",
        height=315,
        width=740,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    # base Canvas Image
    canvas.place(x=0, y=0)
    bg_mic = PhotoImage(
        file=relative_to_assets("mic.png"))
    image_1 = canvas.create_image(
        167.0,
        157.00000000000006,
        image=bg_mic
    )

    # About App Background
    bg_mic_blur = PhotoImage(
        file=relative_to_assets("BlurMic.png"))
    image_3 = canvas.create_image(
        160.0,
        103.0,
        image=bg_mic_blur
    )

    # About App Description
    canvas.create_text(
        26.0,
        28.03,
        anchor="nw",
        text="Vocal Judge 1.0",
        fill="#FFFFFF",
        font=("Roboto", 18 * -1)
    )

    canvas.create_text(
        33.0,
        64.0,
        anchor="nw",
        text="This tool will help you to get an AI based",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    canvas.create_text(
        33.0,
        78.0,
        anchor="nw",
        text="analysis for your song.",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    canvas.create_text(
        33.0,
        98.0,
        anchor="nw",
        text="To get better results, use seperated Vocal",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    canvas.create_text(
        33.0,
        112.0,
        anchor="nw",
        text="and instrumental tracks.",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    canvas.create_text(
        33.0,
        135.0,
        anchor="nw",
        text="If you only have the song recording as a 1 file,",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    canvas.create_text(
        33.0,
        149.0,
        anchor="nw",
        text="Select it in the Vocal/ Complete Song and Leave",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    canvas.create_text(
        33.0,
        163.0,
        anchor="nw",
        text="Instrumental Track Blank.",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    # Background Gradient
    bg_color = PhotoImage(
        file=relative_to_assets("BackgroundImage.png"))
    image_2 = canvas.create_image(
        528.0,
        157.00000000000006,
        image=bg_color
    )
    # Inputs
    canvas.create_text(
        334.0,
        31.03,
        anchor="nw",
        text="Select Audio Files",
        fill="#FFFFFF",
        font=("Roboto", 14 * -1)
    )

    canvas.create_text(
        359.0,
        66.0,
        anchor="nw",
        text="Vocal Track/ Complete Song",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    img_entry_vocal_file = PhotoImage(
        file=relative_to_assets("textbox_bg.png"))
    entry_bg_1 = canvas.create_image(
        535.0,
        100.0,
        image=img_entry_vocal_file
    )
    entry_vocal_file = Entry(
        bd=0,
        bg="#1E1E1E",
        fg="#ffffff",
        highlightthickness=0
    )
    entry_vocal_file.place(
        x=369.0,
        y=85.0,
        width=332.0,
        height=28.0
    )

    img_btn_vocal = PhotoImage(
        file=relative_to_assets("ButtonFolder.png"))
    btn_vocal_track = Button(
        image=img_btn_vocal,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: open_vocal_track(entry_vocal_file),
        relief="flat"
    )
    btn_vocal_track.place(
        x=682.0,
        y=90.0,
        width=22.0,
        height=20.0
    )

    canvas.create_text(
        359.0,
        125.0,
        anchor="nw",
        text="Instrumental Track",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    img_instrumental_file_entry = PhotoImage(
        file=relative_to_assets("textbox_bg2.png"))
    entry_bg_2 = canvas.create_image(
        535.0,
        159.0,
        image=img_instrumental_file_entry
    )
    entry_instrumental = Entry(
        bd=0,
        bg="#1E1E1E",
        fg="#ffffff",
        highlightthickness=0
    )
    entry_instrumental.place(
        x=369.0,
        y=144.0,
        width=332.0,
        height=28.0
    )

    img_btn_instrumental_file = PhotoImage(
        file=relative_to_assets("ButtonFolder2.png"))
    btn_instrumental_file = Button(
        image=img_btn_instrumental_file,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: open_instrumental_track(entry_instrumental),
        relief="flat"
    )
    btn_instrumental_file.place(
        x=682.0,
        y=149.0,
        width=22.0,
        height=20.0
    )

    # show analysis
    canvas.create_text(
        340.0,
        275.0,
        anchor="nw",
        text="Progress",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1)
    )

    progress = canvas.create_text(
        401.0,
        273.0,
        anchor="nw",
        text="The Application GUI may freeze during the analysis",
        fill="#FFFFFF",
        font=("Roboto", 12 * -1))

    img_analyze_button = PhotoImage(
        file=relative_to_assets("btn_analyze.png"))
    btn_analyze = Button(
        image=img_analyze_button,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: start_analysis(entry_vocal_file.get(), entry_instrumental.get(), progress, canvas),
        relief="flat"
    )
    btn_analyze.place(
        x=632.0,
        y=208.0,
        width=77.0,
        height=28.0
    )

    window.resizable(False, False)
    window.mainloop()


def open_vocal_track(entry_1):
    # file type
    filetypes = (
        ('Wav Files', '*.wav'),
    )

    f = fd.askopenfile(filetypes=filetypes)
    entry_1.delete(0, END)
    entry_1.insert(0, os.path.abspath(f.name))


def open_instrumental_track(entry_2):
    # file type
    filetypes = (
        ('Wav Files', '*.wav'),
    )

    f = fd.askopenfile(filetypes=filetypes)
    entry_2.delete(0, END)
    entry_2.insert(0, os.path.abspath(f.name))


def start_analysis(vocal_track, instrumental_track, progress, canvas):

    if not len(vocal_track) == 0 and not len(instrumental_track) == 0:
        print("Starting Analysis")
        # 344919-b89c3977-6450-44a0-9475-8b8a9148443f
        # https://www.figma.com/file/Ee6eGOauQZJZi7LuuoIRep/Untitled?node-id=1%3A2
        print("Vocal Track = " + vocal_track)
        print("Instrumental Track = " + instrumental_track)
        print("Progress : 0%")

        canvas.itemconfig(progress, text="Starting Analysis")
    elif not len(vocal_track) == 0:
        print("==============================================")
        print("Starting Separation")
        canvas.itemconfig(progress, text="Separation Started")
        time.sleep(5)
        Seperator.Seperate(vocal_track)
        canvas.itemconfig(progress, text="Separation Completed")
        print("Separation Completed")
        print("===============================================")

        time.sleep(5)

        print("\n\n=============================================")
        print("Detecting pitch form vocal track")
        canvas.itemconfig(progress, text="Detecting pitch for vocal track")
        vocal_time, vocal_frequency, vocal_confidence, vocal_activation = PitchDetection.GetPitch("VocalsSeperated.wav")
        print("Successfully Detected the pitch")
        canvas.itemconfig(progress, text="Successfully Detected the pitch")
        print("===============================================")

        time.sleep(5)

        print("\n\n=============================================")
        print("Detecting pitch form vocal track")
        canvas.itemconfig(progress, text="Detecting pitch for vocal track")
        ins_time, ins_frequency, ins_confidence, ins_activation = PitchDetection.GetPitch("Instruments.wav")
        print("Successfully Detected the pitch")
        canvas.itemconfig(progress, text="Successfully Detected the pitch")
        print("===============================================")

        time.sleep(5)

        print("\n\n=============================================")
        print("Saving Graphs")
        PitchDetection.SavePlots(ins_time, ins_frequency, vocal_time, vocal_frequency)
        print("Successfully Saved Graphs")
        canvas.itemconfig(progress, text="Successfully Saved Graphs")
        print("===============================================")

        time.sleep(5)

        print("\n\n=============================================")
        print("Detecting Tempo")

    else:
        print("Input Error : No files detected")


if __name__ == "__main__":
    start_gui()
