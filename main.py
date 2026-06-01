import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gabinet"
        )

        self.cursor = self.conn.cursor()

    def fetch_patients(self):
        self.cursor.execute("SELECT * FROM patients")
        return self.cursor.fetchall()

    def fetch_appointments(self):
        self.cursor.execute("""
            SELECT appointments.id,
                   patients.name,
                   patients.surname,
                   appointments.visit_date,
                   appointments.visit_time,
                   appointments.reason,
                   appointments.status
            FROM appointments
            JOIN patients ON appointments.patient_id = patients.id
            ORDER BY appointments.visit_date, appointments.visit_time
        """)

        return self.cursor.fetchall()

    def add_patient(self, name, surname, phone):
        sql = """
            INSERT INTO patients(name, surname, phone)
            VALUES (%s, %s, %s)
        """

        self.cursor.execute(sql, (name, surname, phone))
        self.conn.commit()

    def add_appointment(self, patient_id, date, time, reason, status):
        sql = """
            INSERT INTO appointments(
                patient_id,
                visit_date,
                visit_time,
                reason,
                status
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        self.cursor.execute(
            sql,
            (patient_id, date, time, reason, status)
        )

        self.conn.commit()

    def delete_appointment(self, appointment_id):
        self.cursor.execute(
            "DELETE FROM appointments WHERE id=%s",
            (appointment_id,)
        )

        self.conn.commit()

    def update_appointment(
        self,
        appointment_id,
        date,
        time,
        reason,
        status
    ):

        sql = """
            UPDATE appointments
            SET visit_date=%s,
                visit_time=%s,
                reason=%s,
                status=%s
            WHERE id=%s
        """

        self.cursor.execute(
            sql,
            (
                date,
                time,
                reason,
                status,
                appointment_id
            )
        )

        self.conn.commit()


class MedicalApp:
    def __init__(self, root):
        self.db = Database()

        self.root = root
        self.root.title("Gabinet Lekarski")
        self.root.geometry("1100x650")

        title = tk.Label(
            root,
            text="System Rezerwacji Wizyt",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        self.create_patient_frame()
        self.create_appointment_frame()
        self.create_table()

        self.load_data()

    def create_patient_frame(self):
        frame = tk.LabelFrame(
            self.root,
            text="Dodaj Pacjenta",
            padx=10,
            pady=10
        )

        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Imię").grid(row=0, column=0)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(frame, text="Nazwisko").grid(row=0, column=2)
        self.surname_entry = tk.Entry(frame)
        self.surname_entry.grid(row=0, column=3)

        tk.Label(frame, text="Telefon").grid(row=0, column=4)
        self.phone_entry = tk.Entry(frame)
        self.phone_entry.grid(row=0, column=5)

        tk.Button(
            frame,
            text="Dodaj",
            bg="green",
            fg="white",
            command=self.add_patient
        ).grid(row=0, column=6, padx=10)

    def create_appointment_frame(self):
        frame = tk.LabelFrame(
            self.root,
            text="Rezerwacja Wizyty",
            padx=10,
            pady=10
        )

        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Pacjent").grid(row=0, column=0)

        self.patient_combo = ttk.Combobox(frame, width=30)
        self.patient_combo.grid(row=0, column=1)

        tk.Label(frame, text="Data").grid(row=0, column=2)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=3)

        tk.Label(frame, text="Godzina").grid(row=0, column=4)
        self.time_entry = tk.Entry(frame)
        self.time_entry.grid(row=0, column=5)

        tk.Label(frame, text="Powód").grid(row=1, column=0)
        self.reason_entry = tk.Entry(frame, width=40)
        self.reason_entry.grid(row=1, column=1, columnspan=2)

        tk.Label(frame, text="Status").grid(row=1, column=3)

        self.status_combo = ttk.Combobox(
            frame,
            values=[
                "Zaplanowana",
                "Zakończona",
                "Anulowana"
            ]
        )

        self.status_combo.grid(row=1, column=4)
        self.status_combo.current(0)

        tk.Button(
            frame,
            text="Dodaj Wizytę",
            bg="blue",
            fg="white",
            command=self.add_appointment
        ).grid(row=1, column=5)

        tk.Button(
            frame,
            text="Usuń",
            bg="red",
            fg="white",
            command=self.delete_appointment
        ).grid(row=1, column=6)

    def create_table(self):
        columns = (
            "ID",
            "Imię",
            "Nazwisko",
            "Data",
            "Godzina",
            "Powód",
            "Status"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=18
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        appointments = self.db.fetch_appointments()

        for row in appointments:
            self.tree.insert("", tk.END, values=row)

        self.load_patients()

    def load_patients(self):
        patients = self.db.fetch_patients()

        patient_list = []
        self.patient_map = {}

        for patient in patients:
            patient_id, name, surname, phone = patient

            text = f"{name} {surname}"

            patient_list.append(text)
            self.patient_map[text] = patient_id

        self.patient_combo["values"] = patient_list

    def add_patient(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        phone = self.phone_entry.get()

        if not name or not surname or not phone:
            messagebox.showerror(
                "Błąd",
                "Wypełnij wszystkie pola!"
            )

            return

        self.db.add_patient(name, surname, phone)

        messagebox.showinfo(
            "Sukces",
            "Pacjent dodany!"
        )

        self.load_patients()

    def add_appointment(self):
        try:
            patient_name = self.patient_combo.get()
            patient_id = self.patient_map[patient_name]

            visit_date = self.date_entry.get()
            visit_time = self.time_entry.get()

            datetime.strptime(visit_date, "%Y-%m-%d")

            reason = self.reason_entry.get()
            status = self.status_combo.get()

            self.db.add_appointment(
                patient_id,
                visit_date,
                visit_time,
                reason,
                status
            )

            messagebox.showinfo(
                "Sukces",
                "Wizyta dodana!"
            )

            self.load_data()

        except Exception as e:
            messagebox.showerror(
                "Błąd",
                str(e)
            )

    def delete_appointment(self):
        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected, "values")

        self.db.delete_appointment(values[0])

        self.load_data()


root = tk.Tk()
app = MedicalApp(root)
root.mainloop()