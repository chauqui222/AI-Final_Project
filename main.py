import numpy as np
import cv2
import tensorflow as tf
from tkinter.ttk import *
from tkinter import *
from tkinter.filedialog import Open, SaveAs
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)
from PIL import Image, ImageTk
import PIL

app = Tk()
app.title("Tomato Disease")
scrW = app.winfo_screenwidth()
scrH = app.winfo_screenheight()
app.geometry('1380x750+%d+%d' %(scrW/2-625, 70))
app.configure(bg= "#e5e7e9")
app.resizable(width= False, height= False) #cố định kích thước của cửa sổ

can1 = Canvas(app, bg= 'blue', bd=0)
can1.place(x=0, y= 0,width= 900, height= 675)

solution_img_list = ["Bacterial_spot.jpg", "Early_blight.jpg", "Late_blight.jpg", "Leaf_Mold.jpg",
                     "Septoria_leaf_spot.jpg", "Spider_mites_Two-spotted_spider_mite.jpg","Target_Spot.jpg",
                    "Yellow_Leaf_Curl_Virus.jpg", "healthy.jpg", "mosaic_virus.jpg"]
solution_img= ImageTk.PhotoImage(file= "Solution_Images/Late_blight.jpg")

solution_label = Label(app, image=solution_img, text= "Qui")
solution_label.place(x= 900, y= 0)

global mode
mode = 1
cap_object = 0
cap_object_pr = 0
fl = ''
def getImage():
    global fl, cap_object, mode
    mode = 0
    ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png *.mp4')]
    dlg = Open(filetypes = ftypes)
    fl = dlg.show()
    cap_object = fl
    print("Qui:::",fl)
def getVideo():
    global cap_object, mode
    mode= 1
    ftypes = [('Images', '*.jpg *.tif *.bmp *.gif *.png *.mp4')]
    dlg = Open(filetypes = ftypes)
    fl = dlg.show()
    cap_object = fl

def getCam():
    global cap_object, mode
    mode = 1
    cap_object = 0

getImage_Btn = Button(app, bg= "green", text= "Get Image", font= ("Arial 14 bold"), command= getImage)
getImage_Btn.place(x= 150, y= 685)

getVideo_Btn = Button(app, bg= "green", text= "Get Video", font= ("Arial 14 bold"), command= getVideo)
getVideo_Btn.place(x= 350, y= 685)

getCam_Btn = Button(app, bg= "green", text= "Get Camera", font= ("Arial 14 bold"),command= getCam)
getCam_Btn.place(x= 550, y= 685)


model = tf.keras.models.load_model('Model_Final.h5')



Mydict = ["Bacterial_spot", "Early_blight", "Late_blight", "Leaf_Mold", "Septoria_leaf_spot",
        "Spider_mites Two-spotted_spider_mite","Target_Spot", "Yellow_Leaf_Curl_Virus", "healthy", "mosaic_virus"]


frameWidth = 900
frameHeight = 675
cap = cv2.VideoCapture(cap_object) 
cap.set(3, frameWidth) 
cap.set(4, frameHeight)

while True:   
    if mode ==1:
        if cap_object != cap_object_pr:
            cap_object_pr = cap_object
            cap = cv2.VideoCapture(cap_object)
        success, img = cap.read()
    else:
        img = cv2.imread(fl,cv2.IMREAD_COLOR)
    img_goc = img
    img_goc = cv2.resize(img_goc, (frameWidth,frameHeight))
    img_goc = cv2.cvtColor(img_goc, cv2.COLOR_BGR2RGB)
    # Nhan dang anh
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256,256))
    img_array = np.array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    print("Predictions:",predictions)
    predicted_class = np.argmax(predictions[0])
    confidence = round(100 * (np.max(predictions[0])), 2)
    print(predicted_class)
    print(confidence)
    print(fl)

    # Hien thi 
    solution_img= ImageTk.PhotoImage(file= "Solution_Images/"+solution_img_list[predicted_class])
    solution_label.configure(image=solution_img)

    
    cv2.putText(img_goc, f'Disease Name: {Mydict[predicted_class]}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 80), 2)
    cv2.putText(img_goc, f'Confidence: {confidence}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 80), 2)
    img_goc = ImageTk.PhotoImage(Image.fromarray(img_goc))
    can1.create_image(0,0, image= img_goc, anchor=NW)
    can1.update()
app.mainloop()

