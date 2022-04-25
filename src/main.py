from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="prak_dpbo_3"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)

    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(
        row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label3 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input3 = OptionMenu(dframe, input_jurusan, *options)
    input3.grid(row=2, column=1, padx=20, pady=10, sticky='w')

    # label jenis kelamin and new frame input
    label4 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    genderFrame = LabelFrame(dframe, text="", borderwidth=0)
    genderFrame.grid(row=3, column=1, padx=20, pady=10, sticky='w')

    # input jenis kelamin ~ radio button
    gender = StringVar()
    gender.set("Laki-laki")
    Radiobutton(genderFrame, text="Laki-laki", variable=gender, value="Laki-laki").grid(row=0, column=0, sticky="w")
    Radiobutton(genderFrame, text="Perempuan", variable=gender, value="Perempuan").grid(row=0, column=1, sticky="w")

    # combobox hobi
    label5= Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    # hobi_input = StringVar()
    optionHobi = ["Main Game", "Ngoding", "Sholawatan", "Nyanyi", "Joget"]
    comboHobi = ttk.Combobox(dframe, value=optionHobi)
    comboHobi.grid(row=4, column=1, padx=20, pady=10, sticky='w')
    comboHobi.current(0)

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit", anchor="s", command=lambda: [insertData(top, input_nama, input_nim, input_jurusan, gender, comboHobi), top.withdraw()])
    btn_submit.grid(row=4, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Back", anchor="s",
                        command=lambda: [top.destroy(), root.deiconify()])
    btn_cancel.grid(row=4, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, gender, hobi):
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    gender = gender.get()
    hobi = hobi.get()

    # check empty input
    if nama == "" or nim == "" or jurusan == "" or gender == "" or hobi == "":
        notification(parent, "Ada Data Yang Kosong")
        return

    # insert data to database
    query = "INSERT INTO mahasiswa VALUES (NULL, %s, %s, %s, %s, %s)"
    val = (nim, nama, jurusan, gender, hobi)
    dbcursor.execute(query, val)
    mydb.commit()

    notification(parent, "Data Berhasil Diinput")

def notification(parent, message):
    top = Toplevel()
    top.title("Notification")
    dframe = LabelFrame(top, text="")
    dframe.pack(padx=10, pady=10)

    labelNotif= Label(dframe, text=message).grid(row=0, column=0, padx=20, pady=10)
    btn_ok = Button(dframe, text="OK", anchor="s", command=lambda: [top.destroy(), parent.deiconify()]).grid(row=1, column=0, padx=20, pady=10)

# Window Semua Mahasiswa


def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Back", anchor="w",
                        command=lambda: [top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column=0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="jenis_kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data


def clearAll(parent):
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)

    # Yes
    btn_yes = Button(btnframe, text="Yes", bg="green", fg="white", command=lambda: [top.destroy(), delAll(parent)])
    btn_yes.grid(row=0, column=0, padx=10)

    # No
    btn_no = Button(btnframe, text="No", bg="red", fg="white", command=lambda: [top.destroy(), parent.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI


def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Yes", bg="green", fg="white",
                     command=lambda: [top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="No", bg="red", fg="white",
                    command=lambda: [top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)


def delAll(parent):
    # Delete data disini
    query = "DELETE FROM mahasiswa"
    dbcursor.execute(query)
    mydb.commit()

    notification(parent, "Semua Data Berhasil Dihapus")

# Window Input Data
def imageSlider():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas Kampus")
    dframe = LabelFrame(top, text="Image Slider", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)

    img1 = ImageTk.PhotoImage(Image.open('project/bioskop.jpeg'))
    img2 = ImageTk.PhotoImage(Image.open('project/gameCenter.jpg'))
    image_list = [img1, img2]
    image_name = ["Bioskop", "Game Center"]
    number = 0

    # show image name
    imageName = Label(dframe, text=image_name[0])
    imageName.grid(row=0, column=0)

    # show image label
    imageLabel = Label(dframe, image=img1)
    imageLabel.image = img1
    imageLabel.grid(row=1, column=0)

    # Button Frame
    buttonFrame = LabelFrame(dframe, text="", borderwidth=0)
    buttonFrame.grid(row=2, column=0, pady=10)

    # prev Button
    btn_prev = Button(buttonFrame, text="<<", anchor="s", command=lambda: [prevImage(number-1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next)], state=DISABLED)
    btn_prev.grid(row=0, column=0)

    # Cancel Button
    btn_cancel = Button(buttonFrame, text="Back", anchor="s", command=lambda: [top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=1, padx=20)

    # next Button
    if len(image_list) == 1 :
        btn_next = Button(buttonFrame, text=">>", anchor="s", command=lambda: nextImage(number+1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next), state=DISABLED)
    else :
        btn_next = Button(buttonFrame, text=">>", anchor="s", command=lambda: nextImage(number+1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next))
    btn_next.grid(row=0, column=2)

def prevImage(number, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next):
    imageName.grid_forget()
    imageLabel.grid_forget()
    btn_prev.grid_forget()
    btn_next.grid_forget()

    imageName = Label(dframe, text=image_name[number])
    imageLabel = Label(dframe, image=image_list[number])
    imageLabel.image = image_list[number]
    btn_next = Button(buttonFrame, text=">>", command=lambda: nextImage(number+1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next))

    if number == 0:
        btn_prev = Button(buttonFrame, text="<<", command=lambda: prevImage(number-1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next), state=DISABLED)
    else :
        btn_prev = Button(buttonFrame, text="<<", command=lambda: prevImage(number-1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next))

    imageName.grid(row=0, column=0)
    imageLabel.grid(row=1, column=0)
    btn_prev.grid(row=0, column=0)
    btn_next.grid(row=0, column=2)

def nextImage(number, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next):
    imageName.grid_forget()
    imageLabel.grid_forget()
    btn_prev.grid_forget()
    btn_next.grid_forget()

    imageName = Label(dframe, text=image_name[number])
    imageLabel = Label(dframe, image=image_list[number])
    imageLabel.image = image_list[number]
    btn_prev = Button(buttonFrame, text="<<", command=lambda: prevImage(number-1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next))

    if number == len(image_list)-1:
        btn_next = Button(buttonFrame, text=">>", command=lambda: nextImage(number+1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next), state=DISABLED)
    else :
        btn_next = Button(buttonFrame, text=">>", command=lambda: nextImage(number+1, imageName, image_name, image_list, imageLabel, dframe, buttonFrame, btn_prev, btn_next))

    imageName.grid(row=0, column=0)
    imageLabel.grid(row=1, column=0)
    btn_prev.grid(row=0, column=0)
    btn_next.grid(row=0, column=2)


# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=lambda: [clearAll(root), root.withdraw()], width=30)
b_clear.grid(row=2, column=0, pady=5)

# image slider
b_image = Button(buttonGroup, text="Daftar Fasilitas Kampus", command=imageSlider, width=30)
b_image.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=5, column=0, pady=5)

root.mainloop()
