# Dokumentacja projektu – System Rezerwacji Wizyt w Gabinecie Lekarskim

## 1. Cel projektu

Celem projektu było stworzenie aplikacji umożliwiającej zarządzanie pacjentami oraz rezerwacjami wizyt w gabinecie lekarskim. Program pozwala na dodawanie nowych pacjentów, planowanie wizyt, przeglądanie zapisanych terminów oraz usuwanie istniejących rezerwacji.

Aplikacja została napisana w języku Python z wykorzystaniem biblioteki Tkinter do stworzenia interfejsu graficznego oraz bazy danych MySQL do przechowywania informacji o pacjentach i wizytach.

---

## 2. Wykorzystane technologie

W projekcie wykorzystano następujące technologie:

* Python 3.x
* Tkinter – interfejs graficzny użytkownika
* MySQL – system zarządzania bazą danych
* mysql-connector-python – komunikacja aplikacji z bazą danych

---

## 3. Struktura bazy danych

Baza danych składa się z dwóch tabel:

### Tabela `patients`

Przechowuje dane pacjentów.

| Pole    | Typ danych | Opis              |
| ------- | ---------- | ----------------- |
| id      | INTEGER    | Klucz główny      |
| name    | TEXT       | Imię pacjenta     |
| surname | TEXT       | Nazwisko pacjenta |
| phone   | TEXT       | Numer telefonu    |

### Tabela `appointments`

Przechowuje informacje o wizytach.

| Pole       | Typ danych | Opis                   |
| ---------- | ---------- | ---------------------- |
| id         | INTEGER    | Klucz główny           |
| patient_id | INTEGER    | Identyfikator pacjenta |
| visit_date | TEXT       | Data wizyty            |
| visit_time | TEXT       | Godzina wizyty         |
| reason     | TEXT       | Powód wizyty           |
| status     | TEXT       | Status wizyty          |

Tabela `appointments` jest połączona z tabelą `patients` za pomocą klucza obcego `patient_id`.

---

## 4. Opis działania programu

Po uruchomieniu aplikacji użytkownik widzi główne okno programu zawierające formularze do zarządzania pacjentami i wizytami oraz tabelę z zapisanymi terminami.

Program składa się z dwóch głównych klas:

### Klasa Database

Odpowiada za komunikację z bazą danych. Zawiera metody umożliwiające:

* pobieranie listy pacjentów,
* pobieranie listy wizyt,
* dodawanie nowych pacjentów,
* dodawanie wizyt,
* aktualizowanie danych wizyty,
* usuwanie wizyt.

Każda operacja zapisu kończy się zatwierdzeniem zmian przy pomocy metody `commit()`.

### Klasa MedicalApp

Odpowiada za obsługę interfejsu graficznego użytkownika.

Najważniejsze funkcje klasy:

* tworzenie formularza dodawania pacjentów,
* tworzenie formularza rezerwacji wizyt,
* wyświetlanie danych w tabeli,
* odświeżanie danych pobieranych z bazy,
* walidacja wprowadzonych danych,
* obsługa przycisków aplikacji.

---

## 5. Funkcjonalności aplikacji

### Dodawanie pacjenta

Użytkownik może wprowadzić:

* imię,
* nazwisko,
* numer telefonu.

Po poprawnym wypełnieniu pól dane zostają zapisane w bazie danych.

### Rezerwacja wizyty

Podczas dodawania wizyty użytkownik wybiera pacjenta z listy rozwijanej i podaje:

* datę wizyty,
* godzinę wizyty,
* powód wizyty,
* status wizyty.

Program sprawdza poprawność formatu daty przed zapisaniem danych.

### Przegląd wizyt

Wszystkie zapisane wizyty wyświetlane są w tabeli zawierającej:

* identyfikator wizyty,
* imię pacjenta,
* nazwisko pacjenta,
* datę wizyty,
* godzinę wizyty,
* powód wizyty,
* status wizyty.

### Usuwanie wizyty

Po zaznaczeniu wybranej pozycji w tabeli użytkownik może usunąć wizytę z bazy danych.

---

## 6. Instalacja projektu

### Instalacja wymaganych bibliotek

W katalogu projektu należy wykonać polecenie:

```bash
pip install -r requirements.txt
```

Zawartość pliku `requirements.txt`:

```text
tk
mysql-connector-python
```

### Utworzenie bazy danych

Należy utworzyć bazę danych o nazwie:

```sql
CREATE DATABASE gabinet;
```

Następnie wykonać skrypt tworzący tabele `patients` oraz `appointments` i dodać przykładowe rekordy.

### Konfiguracja połączenia

W klasie `Database` należy ustawić parametry połączenia:

```python
host="localhost"
user="root"
password=""
database="gabinet"
```

W przypadku innej konfiguracji serwera MySQL dane należy odpowiednio zmienić.

---

## 7. Uruchomienie programu

Program uruchamia się za pomocą polecenia:

```bash
python main.py
```

Po uruchomieniu zostanie wyświetlone główne okno aplikacji umożliwiające zarządzanie pacjentami oraz wizytami.

---

## 8. Możliwości rozwoju projektu

Projekt można rozbudować o dodatkowe funkcjonalności, takie jak:

* edycja danych pacjenta,
* edycja istniejących wizyt,
* wyszukiwanie pacjentów,
* filtrowanie wizyt według daty lub statusu,
* logowanie użytkowników,
* automatyczne przypomnienia o wizytach,
* eksport danych do plików PDF lub Excel.

---

## 9. Podsumowanie

Stworzona aplikacja umożliwia podstawową obsługę gabinetu lekarskiego w zakresie zarządzania pacjentami i wizytami. Zastosowanie bazy danych MySQL pozwala na trwałe przechowywanie informacji, natomiast interfejs graficzny wykonany w bibliotece Tkinter zapewnia prostą i wygodną obsługę programu. Projekt spełnia założone wymagania i może stanowić podstawę do dalszego rozwoju systemu.
