import sqlite3

class Student:
    def __init__(self, student_id, name, address):
        self.student_id = student_id
        self.name = name
        self.address = address

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Address: {self.address}"

class UniversityClass:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()
        self.load_data()

    #creates a simple database with student id, name and address as the columns
    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS students (
                            student_id TEXT PRIMARY KEY,
                            name TEXT,
                            address TEXT)''')
        self.conn.commit()

    #populates the empty database using student data from a text file
    def load_data(self):
        with open('student_data.txt', 'r') as file:
            for line in file:
                parts = line.strip().split()
                student_id = parts[0]
                name = ' '.join(parts[1:-4])
                address = ' '.join(parts[-4:])
                self.cur.execute("INSERT INTO students VALUES (?, ?, ?)", (student_id, name, address))
                self.conn.commit()

    def read_student_data(self):
        student_id = input("Enter student ID: ")
        self.cur.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        row = self.cur.fetchone()
        if row:
            print(Student(row[0], row[1], row[2]))
        else:
            print("Student not found.")

    def add_student(self, student_id, name, address):
        self.cur.execute("INSERT INTO students VALUES (?, ?, ?)", (student_id, name, address))
        self.conn.commit()
        print("Student added successfully.")

    def remove_student(self, student_id):
        self.cur.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        self.conn.commit()
        print("Student removed successfully.")

    def modify_student_data(self, student_id, new_name, new_address):
        self.cur.execute("UPDATE students SET name=?, address=? WHERE student_id=?", (new_name, new_address, student_id))
        self.conn.commit()
        print("Student data modified successfully.")

    def __del__(self):
        self.conn.close()

def main():
    university_class = UniversityClass('student_data.db')

    #simple menu for the user to be able to access and modify the database
    while True:
        print("\nMenu:")
        print("1. View student data by ID")
        print("2. Add a new student")
        print("3. Remove a student")
        print("4. Modify student data")
        print("5. Exit")

        choice = input("Enter your choice: ")

        #this choice allows the user to view the data of a student by entering their id
        if choice == '1':
            university_class.read_student_data()
        #this choice allows the user to create a new student in the database
        elif choice == '2':
            student_id = input("Enter student ID: ")
            name = input("Enter student name: ")
            address = input("Enter student address: ")
            university_class.add_student(student_id, name, address)
        #this choice allows the user to remove the student from the database by entering their id
        elif choice == '3':
            student_id = input("Enter student ID to remove: ")
            university_class.remove_student(student_id)
        #lets the user modify the data of an existing student by entering their id
        elif choice == '4':
            student_id = input("Enter student ID to modify: ")
            new_name = input("Enter new name: ")
            new_address = input("Enter new address: ")
            university_class.modify_student_data(student_id, new_name, new_address)
        #lets the user exit the program
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
