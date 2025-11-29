import tkinter as tk
from tkinter import ttk, messagebox
from ui.styles import Styles
from ui.pos_frame import POSFrame
from ui.menu_frame import MenuFrame
from ui.history_frame import HistoryFrame

class PupuseriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Sistema de Ventas - Pupusería "El Sabor de Casa"')
        self.root.geometry("1200x800")
        
        self.dark_mode = False
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        self.header_frame = tk.Frame(self.root, bg=Styles.PRIMARY, height=80)
        self.header_frame.pack(fill="x")
        
        self.title_label = tk.Label(
            self.header_frame, 
            text='Pupusería "El Sabor de Casa"',
            font=Styles.HEADER_FONT,
            bg=Styles.PRIMARY,
            fg=Styles.WHITE
        )
        self.title_label.pack(side="left", padx=20, pady=20)
        
        self.theme_btn = tk.Button(
            self.header_frame,
            text="Modo Oscuro",
            command=self.toggle_theme,
            font=Styles.BOLD_FONT
        )
        self.theme_btn.pack(side="right", padx=20)
        
        # Navigation
        self.nav_frame = tk.Frame(self.root, bg=Styles.DARK_BG)
        self.nav_frame.pack(fill="x")
        
        self.btn_pos = tk.Button(self.nav_frame, text="Ventas", command=lambda: self.show_frame("pos"))
        self.btn_pos.pack(side="left", padx=10, pady=10)
        
        self.btn_menu = tk.Button(self.nav_frame, text="Menú", command=lambda: self.show_frame("menu"))
        self.btn_menu.pack(side="left", padx=10, pady=10)
        
        self.btn_history = tk.Button(self.nav_frame, text="Historial", command=lambda: self.show_frame("history"))
        self.btn_history.pack(side="left", padx=10, pady=10)
        
        # Content Area
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Placeholder for frames
        self.current_frame = None
        self.show_frame("pos")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        Styles.apply_theme(self.root, self.dark_mode)
        # Update button text
        self.theme_btn.config(text="Modo Claro" if self.dark_mode else "Modo Oscuro")

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
            
        if frame_name == "pos":
            self.current_frame = POSFrame(self.content_frame)
            self.current_frame.pack(fill="both", expand=True)
        elif frame_name == "menu":
            self.current_frame = MenuFrame(self.content_frame)
            self.current_frame.pack(fill="both", expand=True)
        elif frame_name == "history":
            self.current_frame = HistoryFrame(self.content_frame)
            self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = PupuseriaApp(root)
    root.mainloop()
