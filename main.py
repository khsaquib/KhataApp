import flet as ft
import sqlite3
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('khata_mobile.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS len_den
                      (id INTEGER PRIMARY KEY, tareekh TEXT, naam TEXT, raqam REAL, qism TEXT, zariya TEXT, tafseel TEXT)''')
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

def main(page: ft.Page):
    page.title = "Khata App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 700

    # UI Inputs
    naam_input = ft.TextField(label="Party Name", width=300)
    raqam_input = ft.TextField(label="Amount (Rs)", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    zariya_dropdown = ft.Dropdown(
        label="Method", 
        options=[ft.dropdown.Option("Cash"), ft.dropdown.Option("Bank Transfer")], 
        width=300
    )
    qism_dropdown = ft.Dropdown(
        label="Type", 
        options=[ft.dropdown.Option("Given"), ft.dropdown.Option("Taken")], 
        width=300
    )
    
    # Ledger List
    ledger_list = ft.ListView(expand=True, spacing=10)

    def load_data():
        ledger_list.controls.clear()
        cursor.execute("SELECT tareekh, naam, raqam, qism FROM len_den ORDER BY id DESC")
        rows = cursor.fetchall()
        for row in rows:
            color = ft.colors.GREEN if row[3] == "Given" else ft.colors.RED
            ledger_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{row[1]} - Rs {row[2]}", color=color, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"{row[0]} | Type: {row[3]}")
                )
            )
        page.update()

    def save_record(e):
        if naam_input.value and raqam_input.value and qism_dropdown.value:
            tareekh = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute("INSERT INTO len_den (tareekh, naam, raqam, qism, zariya, tafseel) VALUES (?, ?, ?, ?, ?, ?)",
                           (tareekh, naam_input.value, float(raqam_input.value), qism_dropdown.value, zariya_dropdown.value, ""))
            conn.commit()
            
            # Clear inputs
            naam_input.value = ""
            raqam_input.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("Record Saved!"))
            page.snack_bar.open = True
            load_data()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Please fill all fields!"))
            page.snack_bar.open = True
            page.update()

    save_btn = ft.ElevatedButton("Save Record", on_click=save_record, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE)

    # Page Layout
    page.add(
        ft.Text("📖 Main Khata", size=24, weight=ft.FontWeight.BOLD),
        naam_input,
        raqam_input,
        zariya_dropdown,
        qism_dropdown,
        save_btn,
        ft.Divider(),
        ft.Text("Ledger History", size=20, weight=ft.FontWeight.BOLD),
        ledger_list
    )
    
    load_data()

ft.app(target=main)