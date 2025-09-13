import customtkinter as ctk
from ui_components import create_widgets
from canvas_utils import load_and_display_tee, redraw_all
from data_management import generate_configs, export_points, import_points
from utils import set_window_icon

class main(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ACG | by lapuhhh")
        self.geometry("1200x800")
        set_window_icon(self, "assets/icon.ico")
        
        # переменные для хранения данных
        self.points = []
        self.point_counter = 1
        self.scale_factor = 1.0
        
        # настройки конфигурации по умолчанию
        self.bind_key = ctk.StringVar(value="o")
        self.folder_name = ctk.StringVar(value="i_like_furries")
        self.default_commands = "rcon tele\nrcon move_raw %coord%\ntoggle cl_dummy 0 1\nrcon tele\nrcon move_raw %opposite%\ntoggle cl_dummy 0 1"
        
        # пер-точечные команды
        self.per_point_commands = {}
        
        # настройки изображения (тии)
        self.tee_filename = "assets/tee.png"
        self.tee_id = None
        
        # создаем интерфейс
        create_widgets(self)
        load_and_display_tee(self)
        redraw_all(self)  # Исправлено: вызов функции из canvas_utils.py

if __name__ == "__main__":
    app = main()
    app.mainloop()