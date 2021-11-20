
import tkinter as tk                
from tkinter import font as tkfont  
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os
from chat import get_response, bot_name
import speech_recognition as sr



LARGE_FONT= ("Verdana", 12)
gray = "#ABB2B9"
bg_color = "#17202A"
color_texto = "#EAECEE"

font = "Helvetica 10"
font_bold = "Helvetica 11 bold"



class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        verif(globals())

        # New loop
        for F in CLASSES:
            frame = CLASSES[F](container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageStart")

    # Now everytime you use this method you need to pass
    # the class name in string format ("" or '').
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


# New name, instead of StartPage.
class PageStart(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg = "#2C3E50")
        #Head
        head_label = tk.Label(self, bg = bg_color, fg = color_texto, text="Chat Bot", 
                            font=font_bold)
        head_label.pack(fill = "x")

        #Line
        line = tk.Label(self, width=58, bg=gray)
        line.pack(fill = "x")

        #Texto
        self.text_widget = tk.Text(self, bg = "#2C3E50", fg = color_texto,font = font)
        self.text_widget.pack(fill="x")
        self.text_widget.configure(cursor = "arrow", state = tk.DISABLED, height=30, width=50)

        #ventana baja
        botton_label = tk.Label(self, bg =gray)
        botton_label.pack(fill ="x")

        #entrada de texto
        self.msg_entry = tk.Entry(botton_label, bg ="#2C3E50", fg = color_texto, font = font )
        self.msg_entry.focus()
        self.msg_entry.pack(fill = "x")
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        self.msg_entry.bind("<Return>", self.speech)

        #Button send 
        button_send = tk.Button(self.msg_entry, text = "SEND", command= lambda: self._on_enter_pressed(None))
        button_send.pack(side = "right")

        # Change in show_frame parameter
        button = tk.Button(self, text="Face Scanner",
                            command=lambda: controller.show_frame("PageOne"))
        button.pack()
        
    
    def speech(self, event):
        mic = sr.Microphone()

        recog = sr.Recognizer()

        with mic as audio_file:
            print("Speak Please")

            recog.adjust_for_ambient_noise(audio_file)
            audio = recog.listen(audio_file)
            msg = recog.recognize_google(audio, language='es-PER')
        self._insert_message(msg, "TU")
        


    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get() 
        self._insert_message(msg, "TU") 
    
    def _insert_message(self, msg, sender):
        if not msg:
            return
        self.msg_entry.delete(0, tk.END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg1)
        self.text_widget.configure(state=tk.DISABLED)

        self.msg_entry.delete(0, tk.END)
        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg2)
        self.text_widget.configure(state=tk.DISABLED)

        self.text_widget.see(tk.END)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #Leer el clasificador de rostros
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        def video_de_entrada():
            global cap, path_video
            if selected.get() == 1:
                path_video = filedialog.askopenfilename(filetypes = [
                    ("all video format", ".mp4"),
                    ("all video format", ".avi")])
                if len(path_video) > 0:
                    btnEnd.configure(state="active")
                    rad1.configure(state="disabled")
                    rad2.configure(state="disabled")
                    pathInputVideo = "..." + path_video[-20:]
                    lblInfoVideoPath.configure(text=pathInputVideo)
                    cap = cv2.VideoCapture(path_video)
                    visualizar()
            if selected.get() == 2:
                btnEnd.configure(state="active")
                rad1.configure(state="disabled")
                rad2.configure(state="disabled")
                lblInfoVideoPath.configure(text="")
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                visualizar()
        
       

        def visualizar():
            global cap
            ret, frame = cap.read()
            if ret == True:
                frame = imutils.resize(frame, width=640)
                frame = deteccion_facilal(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                lblVideo.configure(image=img)
                lblVideo.image = img
                lblVideo.after(10, visualizar)
            else:
                lblVideo.image = ""
                lblInfoVideoPath.configure(text="")
                rad1.configure(state="active")
                rad2.configure(state="active")
                selected.set(0)
                btnEnd.configure(state="disabled")
                cap.release()

        def deteccion_facilal(frame):
            '''import Final2 as fn
            fn.inicio(path_video, cap)'''

            import Final2 as fn
            
            
           
            '''method = 'LBPH'

            if method == 'LBPH': emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

            emotion_recognizer.read('modelo'+method+'.xml')
            # --------------------------------------------------------------------------------

            dataPath = 'D:\DEV\Hackaton_GUI\Data' 
            imagePath = os.listdir(dataPath)
            print('imagePaths=',imagePath)

            cap = cv2.VideoCapture(path_video)
            #cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

            while True:

                ret,frame = cap.read()
                if ret == False: break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                auxFrame = gray.copy()

                faces = faceClassif.detectMultiScale(gray,1.3,5)

                for (x,y,w,h) in faces:
                    rostro = auxFrame[y:y+h,x:x+w]
                    rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
                    result = emotion_recognizer.predict(rostro)
                    cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
                    # LBPHFace
                    if method == 'LBPH':
                        if result[1] < 60:
                            cv2.putText(frame,'{}'.format(imagePath[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)

                        else:
                            cv2.putText(frame,'No identificado',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
            return frame
            #cap.release()
            #cv2.destroyAllWindows()'''
                    
            

            

        def finalizar_limpiar():
            lblVideo.image = ""
            lblInfoVideoPath.configure(text="")
            rad1.configure(state="active")
            rad2.configure(state="active")
            selected.set(0)
            cap.release()
        
        self.configure(bg = "#2C3E50")
        #Head
        head_label = tk.Label(self, fg = color_texto,bg = "#2C3E50", text="Face Scanner", 
                            font=font_bold)
        head_label.grid(column=0, row=0, columnspan = 2)
        #head_label.pack(fill = "x")

        #Line
        line = tk.Label(self, width=58, bg=gray)
        line.grid(column=0, row=1, columnspan = 2)
        #line.pack(fill = "x")

        selected = tk.IntVar()
        rad1 = tk.Radiobutton(self, text="Elegir video", width=20, value=1, variable=selected, command=video_de_entrada, bg = "#2C3E50",fg = color_texto)
        rad2 = tk.Radiobutton(self, text="Video en directo", width=20, value=2, variable=selected, command=video_de_entrada, bg = "#2C3E50",fg = color_texto)
        rad1.grid(column=0, row=2)
        rad2.grid(column=1, row=2)
        #rad1.pack(fill = "x")
        #rad2.pack(fill = "x")

        lblInfoVideoPath = tk.Label(self, text="", width=20, bg = "#2C3E50")
        lblInfoVideoPath.grid(column=0, row=3)
        #lblInfoVideoPath.pack()

        lblVideo = tk.Label(self, bg = "#2C3E50")
        lblVideo.grid(column=0, row=4, columnspan=2)
        #lblVideo.pack()
        
        btnEnd = tk.Button(self, text="Finalizar visualización y limpiar", state="disabled", command=finalizar_limpiar)
        btnEnd.grid(column=0, row=5, columnspan=2, pady=10)
        #btnEnd.pack()

        # Change in show_frame parameter
        button1 = tk.Button(self, text="Back to ChatBot",
                            command=lambda: controller.show_frame("PageStart"))
        #button1.pack()
        button1.grid(column=0, row=6, columnspan = 2)
        
        

def verif(param):
    global CLASSES   

    # Empty dic of classes
    CLASSES = {}
    # We need to declarate aClass before iterating throught globals()
    aClass = ""
    for aClass in param:
        # You need to use a pattern in your classes names. In this
        # example, they start with "Page".

        if aClass.startswith("Page"):
            CLASSES[aClass] = param[aClass]










