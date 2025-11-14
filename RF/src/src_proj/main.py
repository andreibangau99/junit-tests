import mysql.connector
from mysql.connector import Error
from random import randint, choice
from datetime import date, timedelta

class DatabaseConnection:
    """Clase pentru gestionarea conexiunii la baza de date MySQL."""

    def __init__(self, host="localhost", user="root", password=""):
        self.connection = self.create_connection(host, user, password)
        self.create_database("creatii_artistice")
        self.use_database("creatii_artistice")
        self.create_tables()

    def create_connection(self, host, user, password):
        """Inițializează conexiunea la MySQL."""
        try:
            connection = mysql.connector.connect(host=host, user=user, password=password)
            print("Conexiune MySQL reușită.")
            return connection
        except Error as e:
            print(f"Eroare la conectarea la MySQL: {e}")
            return None

    def create_database(self, db_name):
        """Creează baza de date dacă nu există."""
        cursor = self.connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Baza de date '{db_name}' a fost creată.")

    def use_database(self, db_name):
        """Selectează baza de date pentru a o utiliza."""
        cursor = self.connection.cursor()
        cursor.execute(f"USE {db_name}")
        print(f"Se folosește baza de date '{db_name}'.")

    def create_tables(self):
        """Creează tabelele necesare în baza de date."""
        tables = {
            "Scoala": """
                CREATE TABLE IF NOT EXISTS Scoala (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nume VARCHAR(255) NOT NULL
                )
            """,
            "Clasa": """
                CREATE TABLE IF NOT EXISTS Clasa (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nume VARCHAR(255) NOT NULL,
                    scoala_id INT,
                    FOREIGN KEY (scoala_id) REFERENCES Scoala(id)
                )
            """,
            "Elev": """
                CREATE TABLE IF NOT EXISTS Elev (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nume VARCHAR(255) NOT NULL,
                    clasa_id INT,
                    FOREIGN KEY (clasa_id) REFERENCES Clasa(id)
                )
            """,
            "Nota": """
                CREATE TABLE IF NOT EXISTS Nota (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    elev_id INT,
                    valoare FLOAT,
                    FOREIGN KEY (elev_id) REFERENCES Elev(id)
                )
            """,
            "Absenta": """
                CREATE TABLE IF NOT EXISTS Absenta (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    elev_id INT,
                    data DATE,
                    motiv VARCHAR(255),
                    FOREIGN KEY (elev_id) REFERENCES Elev(id)
                )
            """
        }
        cursor = self.connection.cursor()
        for table_name, create_statement in tables.items():
            cursor.execute(create_statement)
        print("Tabelele au fost create.")

class CreatiiArtisticeService:
    """Service pentru operațiuni CRUD și gestionare date pentru școala de arte 'Creații Artistice'."""

    def __init__(self, db_connection):
        self.connection = db_connection.connection

    def initializeaza_date(self):
        """Initializează baza de date cu date inițiale: două clase, zece elevi, note și absențe aleatorii."""
        scoala_id = self.insert_scoala("Scoala de Arte Creatii Artistice")
        
        # Creăm două clase
        clasa_a_id = self.insert_clasa("Clasa A", scoala_id)
        clasa_b_id = self.insert_clasa("Clasa B", scoala_id)
        
        # Creăm 10 elevi, 5 în fiecare clasă
        elev_ids = []
        for i in range(1, 6):
            elev_ids.append(self.insert_elev(f"Elev_A{i}", clasa_a_id))
            elev_ids.append(self.insert_elev(f"Elev_B{i}", clasa_b_id))

        # Adăugăm note și absențe pentru fiecare elev
        for elev_id in elev_ids:
            self.adauga_note_aleatoare(elev_id)
            self.adauga_absente_aleatoare(elev_id)
        
        print("Datele inițiale au fost inserate.")

    def insert_scoala(self, nume):
        """Inserează o școală și returnează ID-ul."""
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Scoala (nume) VALUES (%s)", (nume,))
        self.connection.commit()
        return cursor.lastrowid

    def insert_clasa(self, nume, scoala_id):
        """Inserează o clasă și returnează ID-ul."""
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Clasa (nume, scoala_id) VALUES (%s, %s)", (nume, scoala_id))
        self.connection.commit()
        return cursor.lastrowid

    def insert_elev(self, nume, clasa_id):
        """Inserează un elev într-o clasă și returnează ID-ul."""
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Elev (nume, clasa_id) VALUES (%s, %s)", (nume, clasa_id))
        self.connection.commit()
        return cursor.lastrowid

    def adauga_note_aleatoare(self, elev_id, numar_note=5):
        """Adaugă note aleatoare pentru un elev, între 1 și 10."""
        cursor = self.connection.cursor()
        for _ in range(numar_note):
            nota = round(randint(1, 10) + randint(0, 99) / 100, 2)  # Note între 1.00 și 10.00
            cursor.execute("INSERT INTO Nota (elev_id, valoare) VALUES (%s, %s)", (elev_id, nota))
        self.connection.commit()

    def adauga_absente_aleatoare(self, elev_id, numar_absente=3):
        """Adaugă absențe aleatoare pentru un elev."""
        cursor = self.connection.cursor()
        for _ in range(numar_absente):
            data_absenta = date.today() - timedelta(days=randint(0, 30))  # Date recente
            motiv = choice(["medical", "familie", "personale"])
            cursor.execute("INSERT INTO Absenta (elev_id, data, motiv) VALUES (%s, %s, %s)", (elev_id, data_absenta, motiv))
        self.connection.commit()

    def afiseaza_lista_elevi(self):
        """Afișează lista cu toți elevii din baza de date."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT nume FROM Elev")
        elevi = cursor.fetchall()
        print("Lista elevilor înregistrați:")
        for elev in elevi:
            print(f"- {elev[0]}")

    def cauta_elev_si_afiseaza_detalii(self, nume_elev):
        """Caută elevul după nume, afișează notele, absențele și media acestuia."""
        cursor = self.connection.cursor(dictionary=True)

        # Căutare elev după nume
        cursor.execute("SELECT * FROM Elev WHERE nume = %s", (nume_elev,))
        elev = cursor.fetchone()

        if elev is None:
            print(f"Elevul cu numele '{nume_elev}' nu a fost găsit.")
            return
        
        elev_id = elev["id"]
        print(f"Detalii pentru elevul: {nume_elev}")

        # Preluarea notelor elevului și calcularea mediei
        cursor.execute("SELECT valoare FROM Nota WHERE elev_id = %s", (elev_id,))
        note = [row["valoare"] for row in cursor.fetchall()]
        
        if note:
            media = sum(note) / len(note)
            print(f"Note: {note}")
            print(f"Media notelor: {media:.2f}")
        else:
            print("Elevul nu are note disponibile.")
        
        # Preluarea absențelor elevului
        cursor.execute("SELECT data, motiv FROM Absenta WHERE elev_id = %s", (elev_id,))
        absente = cursor.fetchall()
        
        if absente:
            print("Absențe:")
            for absenta in absente:
                print(f"- Data: {absenta['data']}, Motiv: {absenta['motiv']}")
        else:
            print("Elevul nu are absențe înregistrate.")

    def adauga_nota(self, elev_id, valoare_nota):
        """Adaugă o notă pentru un elev."""
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Nota (elev_id, valoare) VALUES (%s, %s)", (elev_id, valoare_nota))
        self.connection.commit()

    def adauga_absenta(self, elev_id, data_absenta, motiv):
        """Adaugă o absență pentru un elev."""
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Absenta (elev_id, data, motiv) VALUES (%s, %s, %s)", (elev_id, data_absenta, motiv))
        self.connection.commit()

def main():
    db_connection = DatabaseConnection(user="app", password="password")
    service = CreatiiArtisticeService(db_connection)
    service.initializeaza_date()
    
    # Afișăm lista de elevi după inițializarea datelor
    service.afiseaza_lista_elevi()
    
    while True:
        nume_elev = input("Introdu numele elevului (sau scrie 'exit' pentru a închide programul): ")
        if nume_elev.lower() == "exit":
            print("Programul se închide.")
            break
        
        service.cauta_elev_si_afiseaza_detalii(nume_elev)
        
        while True:
            print("\nOpțiuni:")
            print("1. Vizualizare note (+ medie)")
            print("2. Adăugare notă")
            print("3. Vizualizare absențe")
            print("4. Adăugare absență")
            print("5. Back")
            optiune = input("Alege opțiunea: ")

            if optiune == "1":
                service.cauta_elev_si_afiseaza_detalii(nume_elev)
            elif optiune == "2":
                try:
                    nota = float(input("Introduceti valoarea notei (1-10): "))
                    if 1 <= nota <= 10:
                        elev_id = service.cauta_elev_si_afiseaza_detalii(nume_elev)
                        service.adauga_nota(elev_id, nota)
                    else:
                        print("Nota trebuie să fie între 1 și 10.")
                except ValueError:
                    print("Valoare invalidă pentru nota.")
            elif optiune == "3":
                service.cauta_elev_si_afiseaza_detalii(nume_elev)
            elif optiune == "4":
                try:
                    data_absenta = input("Introduceti data absenței (YYYY-MM-DD): ")
                    motiv = input("Introduceti motivul absenței: ")
                    elev_id = service.cauta_elev_si_afiseaza_detalii(nume_elev)
                    service.adauga_absenta(elev_id, data_absenta, motiv)
                except ValueError:
                    print("Valoare invalidă pentru data absenței.")
            elif optiune == "5":
                break
            else:
                print("Opțiune invalidă.")

# Rularea programului
if __name__ == "__main__":
    main()
