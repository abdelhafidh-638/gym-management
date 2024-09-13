import time
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, Frame, Label, Button, Menu, Toplevel, Entry, filedialog, messagebox
from cryptography.fernet import Fernet
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import csv
import os
import uuid
import matplotlib.pyplot as plt
import qrcode
import cv2
import threading
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import winsound

class Dashboard(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Dashboard ")

        # Load background images
        self.header_bg_image = PhotoImage(file="images/header.png")
        self.body_bg_image = PhotoImage(file="images/body.png")
        self.settings_bg = PhotoImage(file="images/settings.png")
        self.lock_bg = PhotoImage(file="images/lock.png")
        self.unlock_bg = PhotoImage(file="images/unlock.png")

        # Show header background using label
        self.header_label = Label(self.master, image=self.header_bg_image)
        self.header_label.place(x=0, y=0, relwidth=1, relheight=0.25)

        # Create the settings button
        self.settings_button = Button(self.master, image=self.settings_bg, command=self.show_settings_menu)
        self.settings_button.place(x=10, y=10)

        self.lock_button = tk.Button(self.master, image=self.unlock_bg, command=self.toggle_image)
        self.lock_button.place(x=730, y=10)

        self.is_locked = False

        self.write = False

        # Create buttons in their defined positions
        self.inscription_button = Button(self.master, text="inscription", command=self.show_inscription_window)
        self.inscription_button.place(x=90, y=20)

        self.recherche_button = Button(self.master, text="recherche", command=self.show_recherche_window)
        self.recherche_button.place(x=170, y=20)

        self.edit_button = Button(self.master, text="Scanner", command=self.start_scanning)
        self.edit_button.place(x=250, y=20)

        self.list_button = Button(self.master, text="List", command=self.show_list)
        self.list_button.place(x=320, y=20)

        # Create the settings menu
        self.settings_menu = Menu(self.master, tearoff=0)
        self.settings_menu.add_command(label="Set New Password", command=self.set_new_password)
        self.settings_menu.add_command(label="Option 2", command=self.option2_function)
        self.settings_menu.add_command(label="Option 3", command=self.option3_function)
        # Create body frame for main content
        self.body_frame = Frame(self.master)
        self.body_frame.place(x=0, y=150, relwidth=1, relheight=0.75)

        # Show body background using label
        self.body_label = Label(self.body_frame, image=self.body_bg_image)
        self.body_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Initialize inscription data list
        self.inscriptions_data = []
        self.photo_label = None  # Initialize photo_label to None
        self.disable_main_buttons()

        self.combo_var='TOUT'


        self.label = Label(self, text="Main Window")

        self.label.pack()
        self.running = True

        #self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def show_settings_menu(self):
        self.settings_menu.post(self.settings_button.winfo_rootx(),
                                self.settings_button.winfo_rooty() + self.settings_button.winfo_height())

    def set_new_password(self):
        password_window = Toplevel(self.master)
        password_window.title("Set New Password")
        password_window.geometry("300x200")

        tk.Label(password_window, text="Enter a new password:").pack(pady=5)
        password_entry = tk.Entry(password_window, show="*")
        password_entry.pack(padx=10, pady=5)

        tk.Label(password_window, text="Confirm password:").pack(pady=5)
        confirm_entry = tk.Entry(password_window, show="*")
        confirm_entry.pack(padx=10, pady=5)

        def submit_password():
            password = password_entry.get()
            confirm_password = confirm_entry.get()

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match. Please try again.")
                return

            try:
                # Generate Fernet key
                key = Fernet.generate_key()
                cipher_suite = Fernet(key)

                # Encrypt password
                encrypted_password = cipher_suite.encrypt(password.encode())

                # Write encrypted password to file
                with open("password.enc", "wb") as password_file:
                    password_file.write(encrypted_password)

                # Write key to file
                with open("key.key", "wb") as key_file:
                    key_file.write(key)

                messagebox.showinfo("Success", "Password and key set successfully.")
                password_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(password_window, text="Set Password", command=submit_password).pack(pady=10)


    def toggle_image(self):
        if not self.is_locked==False:
            self.lock_button.config(image=self.unlock_bg)
            self.disable_main_buttons()
            self.is_locked = False

        else:
            password_window = Toplevel(self.master)
            password_window.title("Password Required")
            password_window.geometry("300x150")

            tk.Label(password_window, text="Enter password:").pack(pady=10)
            password_entry = tk.Entry(password_window, show="*")
            password_entry.pack(padx=10, pady=10)

            def check_password():
                password = password_entry.get()
                try:
                    # Load Fernet key
                    with open('key.key', 'rb') as key_file:
                        key = key_file.read()
                    cipher_suite = Fernet(key)

                    # Decrypt password
                    with open('password.enc', 'rb') as password_file:
                        encrypted_password = password_file.read()
                    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

                    if password == decrypted_password:
                        self.lock_button.config(image=self.lock_bg)
                        self.enable_main_buttons()
                        self.is_locked = True
                        password_window.destroy()

                    else:
                        messagebox.showerror("Error", "Incorrect password")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(password_window, text="Submit", command=check_password).pack(pady=10)


    def disable_main_buttons(self):
        self.inscription_button.config(state="disabled")
        self.recherche_button.config(state="disabled")
        self.edit_button.config(state="disabled")
        self.settings_button.config(state="disabled")
        self.list_button.config(state="disabled")
    def enable_main_buttons(self):
        self.inscription_button.config(state="normal")
        self.recherche_button.config(state="normal")
        self.edit_button.config(state="normal")
        self.settings_button.config(state="normal")
        self.list_button.config(state="normal")

    def show_inscription_window(self):
        self.inscription_window = Toplevel(self.master)
        self.inscription_window.title("Inscription")

        self.labels = ["Nom", "Prenom", "Date de naissance", "Date de début", "Date de fin", "Upload Photo"]
        self.entries = []
        self.photo_path = ""  # Initialize photo_path

        for i, label in enumerate(self.labels):
            lbl = Label(self.inscription_window, text=label)
            lbl.grid(row=i, column=0, padx=10, pady=5)

            if "Date" in label:
                entry = DateEntry(self.inscription_window, date_pattern='yyyy-mm-dd')
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entries.append(entry)
            elif "Upload Photo" in label:
                select_button = Button(self.inscription_window, text="Upload Photo", command=self.open_camera_window)
                select_button.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = Entry(self.inscription_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entries.append(entry)

        add_button = Button(self.inscription_window, text="Add", command=self.add_inscription)
        add_button.grid(row=len(self.labels), columnspan=2, pady=10)

    def open_camera_window(self):
        self.camera_window = Toplevel(self.master)
        self.camera_window.title("Capture Photo")

        self.video_frame = Label(self.camera_window)
        self.video_frame.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.show_fram()

        capture_button = Button(self.camera_window, text="Capture", command=self.capture_image)
        capture_button.pack(pady=10)

    def show_fram(self):
        ret, frame = self.cap.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image)
            image_tk = ImageTk.PhotoImage(image_pil)

            self.video_frame.imgtk = image_tk
            self.video_frame.configure(image=image_tk)

        self.video_frame.after(10, self.show_fram)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image)

            image_pil.thumbnail((100, 100))

            photo_folder = 'photo'
            if not os.path.exists(photo_folder):
                os.makedirs(photo_folder)

            timestamp = time.strftime("%Y%m%d_%H%M%S")

            self.photo_path = os.path.join(photo_folder, f"captured_image_{timestamp}.jpg")
            image_pil.save(self.photo_path)

            self.show_selected_photo(self.photo_path)

            messagebox.showinfo("تم الالتقاط", "تم حفظ الصورة بنجاح في مجلد photo")
            self.camera_window.destroy()
            self.cap.release()
            self.camera_window.destroy()

    def select_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.photo_path = file_path  # Save the photo path
            self.show_selected_photo(file_path)

    def show_selected_photo(self, file_path):
        # Open and resize the selected photo
        image = Image.open(file_path)
        image = image.resize((100, 100), Image.LANCZOS)  # Resize image to 100x100

        photo = ImageTk.PhotoImage(image)

        # Update or create label to show the selected photo
        if self.photo_label:
            self.photo_label.configure(image=photo)
            self.photo_label.image = photo  # Keep reference to the image to prevent garbage collection
        else:
            self.photo_label = Label(self.inscription_window, image=photo, borderwidth=2, relief="solid")
            self.photo_label.image = photo  # Keep reference to the image to prevent garbage collection
            self.photo_label.grid(row=len(self.labels), column=2, padx=10, pady=5)  # Show photo in a new column

    def add_inscription(self):
        data = [entry.get() for entry in self.entries]
        data.append(self.photo_path)  # Add the photo path to the data
        unique_code = str(uuid.uuid4())  # Generate a unique code
        data.append(unique_code)  # Add the unique code to the data

        file_exists = os.path.isfile('inscriptions.csv')

        # Save data to a CSV file
        with open('inscriptions.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(self.labels + ["Photo Path", "Unique Code"])  # Write headers if file does not exist
            writer.writerow(data)

        messagebox.showinfo("Info", "Inscription added successfully")
        self.inscription_window.destroy()  # Close the Inscription window
        self.refresh_table()
        self.photo_label = None  # Reset the photo_label for the next inscription

    def show_recherche_window(self):
        self.recherche_window = Toplevel(self.master)
        self.recherche_window.title("Recherche")

        labels = ["Nom", "Prenom", "Date de naissance"]
        entries = []

        for i, label in enumerate(labels):
            lbl = Label(self.recherche_window, text=label)
            lbl.grid(row=i, column=0, padx=10, pady=5)

            if "Date" in label:
                entry = DateEntry(self.recherche_window, date_pattern='yyyy-mm-dd')
                entry.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = Entry(self.recherche_window)
                entry.grid(row=i, column=1, padx=10, pady=5)

            entries.append(entry)

        recherche_button = Button(self.recherche_window, text="Rechercher", command=lambda: self.recherche(entries))
        recherche_button.grid(row=len(labels), columnspan=2, pady=10)

        self.result_frame = Frame(self.recherche_window, borderwidth=2, relief="solid")
        self.result_frame.grid(row=len(labels) + 1, columnspan=2, pady=10, padx=10, sticky="nsew")

    def recherche(self, entries):
        nom = entries[0].get()
        prenom = entries[1].get()
        date_naissance = entries[2].get()

        with open('inscriptions.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            found = False
            for row in reader:
                if (row[0] == nom and row[1] == prenom and row[2] == date_naissance):
                    self.show_result_in_new_window(row)
                    found = True
                    break

            if not found:
                messagebox.showinfo("Information", "Aucun résultat trouvé.")

    def show_result_in_new_window(self, row):
        result_window = Toplevel(self.master)
        result_window.title("Résultat de recherche")
        result_window.geometry("545x375")  # تعيين حجم النافذة إلى 545x375
        result_window.resizable(False, False)  # منع تغيير حجم النافذة

        result_frame = Frame(result_window, borderwidth=2, relief="solid", bg="#000080")
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load logo image
        logo_image = Image.open("images/logo.png")
        logo_image = logo_image.resize((250, 150), Image.LANCZOS)  # Resize image to 250x150
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = Label(result_frame, image=logo_photo, bg="#000080")
        logo_label.image = logo_photo  # Keep reference to the image to prevent garbage collection
        logo_label.grid(row=0, column=1, padx=10, pady=5, rowspan=2)  # Span 2 rows for logo

        # Show photo if available
        if row[5]:  # Check if photo path exists in the row data
            image = Image.open(row[5])
            image = image.resize((100, 130), Image.LANCZOS)  # Resize image to 100x100
            photo = ImageTk.PhotoImage(image)
            photo_label = Label(result_frame, image=photo, bg="#000080")
            photo_label.image = photo  # Keep reference to the image to prevent garbage collection
            photo_label.grid(row=0, column=0, padx=10, pady=5, rowspan=4)  # Span 4 rows for photo
        else:
            photo_label = Label(result_frame, text="No photo available", bg="#000080", fg='yellow',
                                font=('Arial', 12, 'bold'), padx=10, pady=5)
            photo_label.grid(row=2, column=0, padx=10, pady=5, rowspan=4)  # Span 4 rows for no photo label

        # Display details
        labels = ["Nom", "Prenom", "Date de naissance", "Date de début", "Date de fin", "Photo Path", "Unique Code"]
        for i, label in enumerate(labels):
            if label in ["Date de début", "Date de fin", "Photo Path", "Unique Code"]:
                continue
            lbl = Label(result_frame, text=f"{label}: {row[i]}", bg="#000080", fg='white', font=('Arial', 12, 'bold'),
                        padx=10, pady=5)
            lbl.grid(row=i + 2, column=1, sticky="w")

        # Show date range in one line
        date_debut = row[3]
        date_fin = row[4]
        date_range = f"{date_debut}  →  {date_fin}"
        date_range_label = Label(result_frame, text=date_range, bg="#000080", fg='white', font=('Arial', 12, 'bold'),
                                 padx=10, pady=5)
        date_range_label.grid(row=len(labels) - 1, column=1, sticky="W")

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(row[6])
        qr.make(fit=True)

        img = qr.make_image(fill='red', back_color='green')
        img = img.resize((100, 100), Image.LANCZOS)

        # Convert the image to a format supported by Tkinter
        phot = ImageTk.PhotoImage(img)

        # Create and display the image inside a Label in the result frame
        qr_label = Label(result_frame, image=phot, bg='#000080')
        qr_label.img = phot  # Keep reference to the image to prevent garbage collection
        qr_label.grid(row=4, column=2, padx=5, pady=5, rowspan=4)

    def read_barcodes(self, frame):
        detector = cv2.QRCodeDetector()
        data, vertices_array, _ = detector.detectAndDecode(frame)

        if vertices_array is not None and data:
            vertices_array = vertices_array.astype(int)
            for i in range(len(vertices_array)):
                next_point_index = (i + 1) % len(vertices_array)
                cv2.line(frame, tuple(vertices_array[i][0]), tuple(vertices_array[next_point_index][0]), (0, 255, 0), 3)

            print(f"QR Code Data: {data}")
            winsound.Beep(1000, 500)  # Frequency=1000Hz, Duration=500ms

            file_path = 'inscriptions.csv'
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip the header row
                code_found = False

                for row in reader:
                    if row[6] == data:
                        print(
                            f"Name: {row[0]}\nSurname: {row[1]}\nBirth Date: {row[2]}\nStart Date: {row[3]}\nEnd Date: {row[4]}\nCode: {row[6]}")
                        self.show_result_in_new_window(row)
                        code_found = True
                        break  # Exit the loop if code is found

                if not code_found:
                    print("Code not found")

        return frame

    def show_frame(self):
        if not self.running:
            return

        # Create a new window for video display
        video_window = Toplevel(self)
        video_window.title("Barcode/QR Code Reader")
        video_window.geometry("320x240+600+50")
        video_window.resizable(False,False)
        label = Label(video_window)
        label.pack(fill="both", expand=True)

        def update_frame():
            ret, frame = self.cap.read()
            if ret:
                frame = self.read_barcodes(frame)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                label.imgtk = imgtk
                label.configure(image=imgtk)
            if self.running:
                video_window.after(10, update_frame)

        update_frame()

    def barcode_scanner(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend
        if not self.cap.isOpened():
            print("Cannot open camera")
            return

        # Set the resolution to a lower value for faster processing
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        self.show_frame()

    def start_scanning(self):
        self.running = True
        threading.Thread(target=self.barcode_scanner).start()

    def on_closing(self):
        self.running = False
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()



    def show_result(self, row):
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Set background color to sky blue
        self.result_frame.config(bg="#000080")

        # Show photo if available
        if row[5]:  # Check if photo path exists in the row data
            image = Image.open(row[5])
            image = image.resize((100, 100), Image.LANCZOS)  # Resize image to 100x100
            photo = ImageTk.PhotoImage(image)
            photo_label = Label(self.result_frame, image=photo, bg="#000080")
            photo_label.image = photo  # Keep reference to the image to prevent garbage collection
            photo_label.grid(row=0, column=0, padx=10, pady=5, rowspan=4)  # Span 4 rows for photo
        else:
            photo_label = Label(self.result_frame, text="No photo available", bg="#000080", padx=10, pady=5)
            photo_label.grid(row=0, column=0, padx=10, pady=5, rowspan=4)  # Span 4 rows for no photo label

        # Display details
        labels = ["Nom", "Prenom", "Date de naissance", "Date de début", "Date de fin", "Photo Path", "Unique Code"]
        for i, label in enumerate(labels):
            if label == "Date de début" or label == "Date de fin":
                # Skip displaying these labels individually, show them as a range instead
                continue
            if label == "Unique Code":
                # lbl = Label(self.result_frame, text=f" {row[-1]}", bg="sky blue", padx=10, pady=5)
                continue
            elif label == "Photo Path":
                # Skip displaying the photo path
                continue
            else:
                lbl = Label(self.result_frame, text=f"{label}: {row[i]}", bg="#000080", padx=10, pady=5)
            lbl.grid(row=i, column=1, sticky="w")

        # Show date range in one line
        date_debut = row[3]
        date_fin = row[4]
        date_range = f"{date_debut}  →  {date_fin}"
        date_range_label = Label(self.result_frame, text=date_range, bg="#000080", padx=10, pady=5)
        date_range_label.grid(row=len(labels), column=1, sticky="W")

        # lbl = Label(self.result_frame, text=f" {row[6]}", bg="sky blue", padx=10, pady=5)
        # lbl.grid(row=len(labels)+1, column=1, sticky="w")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data({row[6]})
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # عرض الصورة في نافذة جديدة
        plt.imshow(img)
        plt.axis('off')
        # plt.show()

        img = img.resize((100, 100), Image.LANCZOS)

        # تحويل الصورة إلى صيغة تدعمها Tkinter
        phot = ImageTk.PhotoImage(img)

        # إنشاء وعرض الصورة داخل Label في الإطار النتيجي (self.result_frame
        photo_label = Label(self.result_frame, image=phot)
        photo_label.img = phot  # الاحتفاظ بالمرجع على الصورة لتجنب جمع النفايات
        photo_label.grid(row=4, column=5, padx=5, pady=5, rowspan=4)



    def show_list(self):
        # قراءة البيانات من ملف CSV
        with open('inscriptions.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.data = list(reader)  # حفظ البيانات الأصلية

        # إنشاء نافذة جديدة لعرض الجدول
        self.list_window = tk.Toplevel(self.master)
        self.list_window.title("List")

        self.search_entry = tk.Entry(self.list_window, width=40)
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_key_release)

        options = ["TOUT", "Ils n'ont pas payé"]


        self.combo_var = tk.StringVar()

        # إنشاء قائمة منسدلة
        self.combo = ttk.Combobox(self.list_window, textvariable=self.combo_var, values=options, state="readonly")
        self.combo.bind("<<ComboboxSelected>>", self.on_select)
        self.combo.current(0)  # تعيين الخيار الافتراضي
        self.combo.pack(padx=10, pady=10)

        # إنشاء جدول باستخدام ttk.Treeview
        columns_to_show = self.data[0][:-2]  # استبعاد العمودين قبل الأخيرين
        columns_to_show.append("modification")
        columns_to_show.append("Suprition")  # إضافة عمود الحذف
        self.tree = ttk.Treeview(self.list_window, columns=columns_to_show, show='headings')

        # تعيين رؤوس الأعمدة
        for col in columns_to_show:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        # إضافة الصفوف إلى الجدول
        for row in self.data[1:]:
            row_to_show = row[:-2]  # استبعاد العمودين قبل الأخيرين
            row_to_show.append("modifie")
            row_to_show.append("suprimie")  # إضافة النص "delet" إلى عمود الحذف
            self.tree.insert('', 'end', values=row_to_show)

        # تعيين حجم الجدول ليمتلئ داخل النافذة
        self.tree.pack(fill='both', expand=True)

        # ربط حدث النقر على الخلية
        self.tree.bind("<ButtonRelease-1>", self.on_click)

    def on_click(self, event):
        # الحصول على العنصر المحدد
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        # التحقق مما إذا كان العمود هو عمود الإجراءات أو عمود الحذف
        if column != f"#{len(self.tree['columns'])}" and column != f"#{len(self.tree['columns']) - 1}":
            # العثور على الصف الأصلي في البيانات
            index = self.tree.index(item)
            original_values = self.data[index + 1]  # +1 لأننا استبعدنا الرأس
            self.show_result_in_new_window(original_values)
        elif column == f"#{len(self.tree['columns'])}":
            # إذا كان العمود هو عمود الحذف
            index = self.tree.index(item)
            target_code = self.data[index + 1][6]  # الحصول على الكود المستهدف
            self.delet(target_code)
            self.refresh_table()
        if column == f"#{len(self.tree['columns'])-1}":
            index = self.tree.index(item)
            target_code = self.data[index + 1][6]  # الحصول على الكود المستهدف
            self.display_row_data(self.tree, item,target_code)
            self.refresh_table()

    def on_select(self, event):
        selected_option = self.combo_var.get()
        if selected_option=='TOUT':
            self.refresh_table()
        else:

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in self.data[1:]:
                if  datetime.strptime(row[4], '%Y-%m-%d') < datetime.now():
                    row_to_show = row[:-2]
                    row_to_show.append("modifie")
                    row_to_show.append("suprimie")
                    self.tree.insert('', 'end', values=row_to_show)



    def on_key_release(self, event):
        if self.search_entry.get():
            self.write = True
            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in self.data[1:]:
                if self.search_entry.get() in row[1] or  self.search_entry.get() in row[0]:
                    row_to_show = row[:-2]
                    row_to_show.append("modifie")
                    row_to_show.append("suprimie")
                    self.tree.insert('', 'end', values=row_to_show)
            print("بحث: ", self.search_entry.get())
        elif self.write:
            self.refresh_table()
            self.write = False


    def display_row_data(self, tree, selected_item,N):
        item = tree.item(selected_item)
        row_data = item["values"]
        F = N
        self.row_window = Toplevel(self.master)
        self.row_window.title("Edit Row Data")

        labels = ["Nom", "Prenom", "Date de naissance", "Date de début", "Date de fin"]
        self.entries = []

        for i, label in enumerate(labels):
            lbl = Label(self.row_window, text=label)
            lbl.grid(row=i, column=0, padx=10, pady=5)

            if i < len(row_data):
                value = row_data[i]
            else:
                value = ""  # Default to empty string if row_data is missing values

            if "date" in label.lower():
                entry = DateEntry(self.row_window, date_pattern="yyyy-mm-dd")
                try:
                    date_value = datetime.strptime(value, "%Y-%m-%d").date()
                    entry.set_date(date_value)
                except ValueError:
                    entry.set_date(datetime.today())  # Default to today if parsing fails
            else:
                entry = Entry(self.row_window)
                entry.insert(0, value)

            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        save_button = Button(self.row_window, text="Save Changes", command=lambda: self.save_changes(row_data,F))
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def save_changes(self, original_row_data,A):
        new_data = [entry.get() for entry in self.entries]
        print("New data:", new_data)  # طباعة للتحقق من البيانات الجديدة

        # قراءة البيانات من ملف CSV الحالي
        try:
            with open('inscriptions.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = list(reader)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return

        # تحديث البيانات في قائمة البيانات
        updated = False
        for i, row in enumerate(data):
            if row[6] ==A:  # Match using the unique code
                new_row = new_data + row[-2:]  # Keep the last two columns unchanged
                data[i] = new_row
                updated = True
                break

        if not updated:
            print("No matching row found.")
            return

        # كتابة البيانات المحدثة إلى ملف CSV
        try:
            with open('inscriptions.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            print("Data saved successfully to CSV.")  # طباعة للتحقق من حفظ البيانات
            messagebox.showinfo("Info", "Changes saved successfully")
            self.row_window.destroy()
            self.refresh_table()
        except Exception as e:
            print(f"Error writing to CSV file: {e}")

    def delet(self, target_code):
        # عرض نافذة تنبيه بسيطة
        confirm = messagebox.askokcancel("تأكيد الحذف", "هل تريد حقاً حذف هذا السجل؟")

        if confirm:
            file_path = 'inscriptions.csv'
            df = pd.read_csv(file_path)
            df_filtered = df[df.iloc[:, 6] != target_code]
            df_filtered.to_csv(file_path, index=False)
            messagebox.showinfo("تم الحذف", "تم حذف السجل بنجاح!")

    def refresh_table(self):
        # حذف جميع الصفوف من الجدول الحالي
        for row in self.tree.get_children():
            self.tree.delete(row)

        # إعادة قراءة البيانات وتحديث الجدول
        with open('inscriptions.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.data = list(reader)

        for row in self.data[1:]:
            row_to_show = row[:-2]
            row_to_show.append("modifie")
            row_to_show.append("suprimie")
            self.tree.insert('', 'end', values=row_to_show)

    def option2_function(self):
        print("Option 2 selected")

    def option3_function(self):
        print("Option 3 selected")


def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.resizable(False,False)
    app = Dashboard(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
