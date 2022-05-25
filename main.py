import pandas as pd
import pymysql
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

class Main:
    def __init__(self, file):
        self.file = file
        
    def get_file(self):
        data = pd.read_csv(self.file,
                usecols=["is_compat_interior_wall",
                        "mesh_width","mesh_height","mass_surf","mass_comb",
                        "trame","roll_pallet","color_names"],
                delimiter=";",
                )
        df = pd.DataFrame(data)
        df['mesh_width'] = df['mesh_width'].fillna(0.0)
        df['mesh_height'] = df['mesh_height'].fillna(0.0)
        df['mass_surf'] = df['mass_surf'].fillna(0.0)
        df['mass_comb'] = df['mass_comb'].fillna(0.0)
        df['roll_pallet'] = df['roll_pallet'].fillna(0)
        return (df)
                
    def connection_sql(self, connection):
        if (connection == "new"):
            mydb = pymysql.connect(
                host="localhost",
                user="test",
                password="######",
                )
            return mydb
        else:
            mydb = pymysql.connect(
                host="localhost",
                user="test",
                password="######",
                database="mydatabase",
                )
            return mydb
    
    def create_database(self):
        mydb = self.connection_sql(connection="new")
        mycursor = mydb.cursor()
        mycursor.execute("SHOW DATABASES")
        mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
        mycursor.fetchall()
        self.create_table()

    def create_table(self):
        mydb = self.connection_sql(connection="")
        query = """CREATE TABLE IF NOT EXISTS Mesh (id INT AUTO_INCREMENT PRIMARY KEY, 
                trame VARCHAR(255), 
                mass_surf FLOAT DEFAULT 0.0, 
                is_compat_interior_wall BOOL, 
                mesh_height FLOAT DEFAULT 0.0, 
                mesh_width FLOAT DEFAULT 0.0, 
                mass_comb FLOAT DEFAULT 0.0, 
                roll_pallet INT, 
                color_names VARCHAR(255))"""
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mycursor.execute("SHOW TABLES")
        self.insert_data(mycursor, mydb)

    def insert_data(self, mycursor, mydb):
        sql = "INSERT INTO `Mesh` (`trame`, `mass_surf`, `is_compat_interior_wall`, `mesh_height`, `mesh_width`, `mass_comb`, `roll_pallet`, `color_names`) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', %s)"
        df = self.get_file()
        for row in df.itertuples():
            mycursor.execute(sql, (row.trame, row.mass_surf, row.is_compat_interior_wall, row.mesh_height, row.mesh_width, row.mass_comb, row.roll_pallet, row.color_names))
        mydb.commit()
        self.close_connection(mycursor)

    def close_connection(self, mydb):
        print("Data correctly store")
        mydb.close()

class Mesh:
    @property
    def trame(self):
        return(self._trame)
    @trame.setter
    def trame(self, value):
        self._trame = value

    def __init__(self):
        self._trame = ""
        self._mass_surf = 0
        self._is_compat_interior_wall = False
        self._mesh_height = 0.0
        self._mesh_width= 0.0
        self._mass_comb= 0.0
        self._roll_pallet = 0
        self._color_names = [""]

    def modif_data(self):
        return {"trame": self.trame, "mass_surf": self.mass_surf, "is_compat_interior_wall": self.is_compat_interior_wall,
                "mesh_height": self.mesh_height, "mesh_width": self.mesh_width, "mass_comb": self.mass_comb, 
                "roll_pallet:": self.roll_pallet, "color_names": self.color_names}


def select_files():
    filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*'),
        ('text files', '*.txt')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/home/',
        filetypes=filetypes)
    Main(filename).create_table()
    exit(0)


def main():
    window = tk.Tk()
    window.title('Upload CSV File')
    window.geometry('300x200+50+50')
    window.resizable(False, False)
    window.configure(bg='black')
    label = tk.Label(
                text="Please select your csv file",
                foreground="white",
                background="black" 
            )
    label.pack()
    open_button = tk.Button(
                window,
                text='Open Files',
                command=select_files
            )
    open_button.pack(expand=True)
    window.mainloop()

if __name__ == '__main__':
    filepath = main()