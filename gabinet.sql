CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    visit_date TEXT NOT NULL,
    visit_time TEXT NOT NULL,
    reason TEXT,
    status TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
);

INSERT INTO patients (name, surname, phone)
VALUES
('Jan', 'Kowalski', '123456789'),
('Anna', 'Nowak', '987654321');

INSERT INTO appointments (
    patient_id,
    visit_date,
    visit_time,
    reason,
    status
)
VALUES
(1, '2026-05-20', '10:00', 'Kontrola', 'Zaplanowana'),
(2, '2026-05-21', '12:30', 'Badanie', 'Zaplanowana');