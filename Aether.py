import customtkinter as ctk
from tkinter import messagebox, filedialog, Toplevel, Canvas
import os
from pathlib import Path
from PIL import Image, ImageTk
import base64
import json

# стиль
ctk.set_appearance_mode("Dark")

class main(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ACG | by lapuhhh")
        self.geometry("1200x800")  # увеличил размер для лучшего размещения
        self.set_window_icon("assets/icon.ico")  # иконка
        
        # переменные для хранения данных
        self.points = []
        self.point_counter = 1
        self.scale_factor = 1.0  # для зума
        
        # настройки кфг по умолчанию
        self.bind_key = ctk.StringVar(value="o")
        self.folder_name = ctk.StringVar(value="i_like_furries")
        self.default_commands = "rcon tele\nrcon move_raw %coord%\ntoggle cl_dummy 0 1\nrcon tele\nrcon move_raw %opposite%\ntoggle cl_dummy 0 1"
        
        # пер-точечные команды (словарь: point_num -> custom_commands)
        self.per_point_commands = {}
        
        # настройки изображения (тии)
        self.tee_filename = "assets/tee.png"  # тиишка по середине полотна
        self.tee_id = None
        
        # создаем интерфейс
        self.create_widgets()
        self.load_and_display_tee()

    def set_window_icon(self, icon_path):
        """Sets the window icon for the application."""
        try:
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")

    def load_and_display_tee(self):
        """загружает тишку и отображает его в центре канваса с масштабированием по сетке."""
        try:
            img = Image.open(self.tee_filename)
            # масштабируем размер тии (55x55 в координатах канваса)
            scaled_size = (int(55 * self.scale_factor), int(55 * self.scale_factor))
            img = img.resize(scaled_size, Image.LANCZOS)
            self.tk_tee = ImageTk.PhotoImage(img)

            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            center_x, center_y = width // 2, height // 2
            tee_x = center_x - scaled_size[0] // 2
            tee_y = center_y - scaled_size[1] // 2

            if self.tee_id:
                self.canvas.delete(self.tee_id)
            self.tee_id = self.canvas.create_image(tee_x, tee_y, anchor="nw", image=self.tk_tee)
            self.canvas.tag_raise("grid")

        except FileNotFoundError:
            print(f"Error: tee file '{self.tee_filename}' not found.")
        except Exception as e:
            print(f"Error loading tee: {e}")

    def create_widgets(self):
        # основной фрейм
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # заголовок (смещен влево)
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="Aether Config Generator",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold"),
            text_color="#E0E0E0",
            anchor="w"
        )
        title_label.pack(side="left")
        
        # кнопка информации
        info_btn = ctk.CTkButton(
            title_frame, 
            text="Info & Changelog",
            command=self.show_info,
            fg_color="#4A4A4A",
            hover_color="#5A5A5A",
            font=ctk.CTkFont(family="Roboto", size=12),
            width=150
        )
        info_btn.pack(side="right", padx=10)
        
        # контейнер для основного содержимого
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # левая панель - канвас
        left_frame = ctk.CTkFrame(content_frame, fg_color="#2A2A2A", corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=10)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # заголовок для канваса
        canvas_label = ctk.CTkLabel(
            left_frame, 
            text="Coordinate Canvas", 
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            text_color="#B0B0B0"
        )
        canvas_label.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=15)
        
        # канвас
        self.canvas = ctk.CTkCanvas(
            left_frame, 
            width=550, 
            height=550, 
            bg="#1E1E1E", 
            highlightthickness=0
        )
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # для зума
        self.draw_grid()
        
        # кнопки управления
        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(0, 10))
        
        ctk.CTkButton(
            btn_frame, 
            text="Delete Last", 
            command=self.delete_last_point,
            fg_color="#4A4A4A",
            hover_color="#5A5A5A",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, 
            text="Delete Specific", 
            command=self.delete_specific_point,
            fg_color="#4A4A4A",
            hover_color="#5A5A5A",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, 
            text="Clear All", 
            command=self.delete_all_points,
            fg_color="#4A4A4A",
            hover_color="#5A5A5A",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, 
            text="Show Coordinates", 
            command=self.show_coordinates,
            fg_color="#4A4A4A",
            hover_color="#5A5A5A",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(side="left", padx=5)
        
        # кнопки импорта/экспорта
        import_export_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        import_export_frame.grid(row=3, column=0, pady=(0, 10))
        
        ctk.CTkButton(
            import_export_frame, 
            text="Export", 
            command=self.export_points,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            import_export_frame, 
            text="Import", 
            command=self.import_points,
            fg_color="#4169E1",
            hover_color="#6495ED",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(side="left", padx=5)
        
        # правая панель - настройки с прокруткой
        right_frame = ctk.CTkScrollableFrame(
            content_frame, 
            fg_color="#2A2A2A", 
            corner_radius=10,
            scrollbar_button_color="#4A4A4A",
            scrollbar_button_hover_color="#5A5A5A"
        )
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=10)
        right_frame.columnconfigure(0, weight=1)
        
        # заголовок настроек
        settings_label = ctk.CTkLabel(
            right_frame, 
            text="Configuration Settings",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            text_color="#B0B0B0"
        )
        settings_label.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=15)
        
        # поле бинда
        ctk.CTkLabel(
            right_frame, 
            text="Bind Key:",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color="#E0E0E0"
        ).grid(row=1, column=0, sticky="w", pady=(0, 5), padx=15)
        bind_entry = ctk.CTkEntry(
            right_frame, 
            textvariable=self.bind_key, 
            width=120,
            font=ctk.CTkFont(family="Roboto", size=12),
            fg_color="#3A3A3A",
            border_color="#5A5A5A"
        )
        bind_entry.grid(row=2, column=0, sticky="w", pady=(0, 15), padx=15)
        
        # поле имени папки
        ctk.CTkLabel(
            right_frame, 
            text="Folder Name:",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color="#E0E0E0"
        ).grid(row=3, column=0, sticky="w", pady=(0, 5), padx=15)
        folder_entry = ctk.CTkEntry(
            right_frame, 
            textvariable=self.folder_name,
            font=ctk.CTkFont(family="Roboto", size=12),
            fg_color="#3A3A3A",
            border_color="#5A5A5A"
        )
        folder_entry.grid(row=4, column=0, sticky="ew", pady=(0, 15), padx=15)
        
        # глобальные команды
        ctk.CTkLabel(
            right_frame, 
            text="Default Custom Commands:",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color="#E0E0E0"
        ).grid(row=5, column=0, sticky="w", pady=(0, 5), padx=15)
        self.commands_text = ctk.CTkTextbox(right_frame, width=400, height=150, fg_color="#3A3A3A", text_color="white", font=ctk.CTkFont(family="Roboto", size=14))
        self.commands_text.grid(row=6, column=0, sticky="nsew", pady=(0, 15), padx=15)
        self.commands_text.insert("0.0", self.default_commands)
        
        # кнопка редактирования пер-точечных команд
        per_point_btn = ctk.CTkButton(
            right_frame, 
            text="Edit Per-Point Commands",
            command=self.edit_per_point_commands,
            fg_color="#4A4A4A",
            hover_color="#5A5A5A",
            font=ctk.CTkFont(family="Roboto", size=12)
        )
        per_point_btn.grid(row=7, column=0, pady=(0, 15), padx=15, sticky="w")
        
        # подсказка по синтаксису
        syntax_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        syntax_frame.grid(row=8, column=0, sticky="ew", pady=(0, 15), padx=15)
        ctk.CTkLabel(
            syntax_frame, 
            text="Available placeholders:", 
            text_color="#A0C0FF",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold")
        ).pack(anchor="w")
        ctk.CTkLabel(
            syntax_frame, 
            text="%coord% - coordinates (x y)", 
            text_color="#B0B0B0",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(anchor="w")
        ctk.CTkLabel(
            syntax_frame, 
            text="%opposite% - opposite coordinates (-x -y)", 
            text_color="#B0B0B0",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(anchor="w")
        ctk.CTkLabel(
            syntax_frame, 
            text="%next% - next config file number", 
            text_color="#B0B0B0",
            font=ctk.CTkFont(family="Roboto", size=12)
        ).pack(anchor="w")
        
        # кнопка генерации
        generate_btn = ctk.CTkButton(
            right_frame, 
            text="Generate Configs",
            command=self.generate_configs,
            fg_color="#4A4A4A",
            hover_color="#5A5A5A",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
        )
        generate_btn.grid(row=9, column=0, pady=(10, 15), padx=15)
        
        # информационное поле
        self.info_text = ctk.CTkTextbox(right_frame, width=400, height=100, fg_color="#3A3A3A", text_color="#B0B0B0", font=ctk.CTkFont(family="Roboto", size=14))
        self.info_text.grid(row=10, column=0, sticky="nsew", pady=(0, 15), padx=15)
        self.info_text.insert("0.0", "Configure settings and click 'Generate Configs'")
        self.info_text.configure(state="disabled")
        
        right_frame.rowconfigure(6, weight=1)
        right_frame.rowconfigure(10, weight=1)
        
        # статус бар
        self.status_var = ctk.StringVar(value="Ready")
        status_bar = ctk.CTkLabel(
            self, 
            textvariable=self.status_var, 
            anchor="w",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color="#B0B0B0"
        )
        status_bar.pack(side="bottom", fill="x", padx=20, pady=10)

    def on_canvas_resize(self, event):
        """обработчик изменения размера канваса."""
        self.redraw_all()

    def redraw_all(self):
        """перерисовывает сетку, логотип и точки с учетом зума."""
        self.draw_grid()
        self.load_and_display_tee()
        self.redraw_points()

    def draw_grid(self):
        """рисует сетку на канвасе с учетом зума, исправляя смещение."""
        self.canvas.delete("grid")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            self.after(100, self.draw_grid)
            return
        
        center_x, center_y = width // 2, height // 2
        grid_step = int(32 * self.scale_factor)
        
        # рисуем основные оси
        self.canvas.create_line(0, center_y, width, center_y, fill="#444444", width=2, tags="grid")
        self.canvas.create_line(center_x, 0, center_x, height, fill="#444444", width=2, tags="grid")
        
        # рисуем сетку, выравнивая по центру
        start_x = center_x - (center_x // grid_step) * grid_step
        start_y = center_y - (center_y // grid_step) * grid_step
        
        for x in range(int(start_x), width, grid_step):
            color = "#333333" if (x - center_x) % grid_step != 0 else "#444444"
            self.canvas.create_line(x, 0, x, height, fill=color, tags="grid")
        for x in range(int(start_x - grid_step), 0, -grid_step):
            color = "#333333" if (x - center_x) % grid_step != 0 else "#444444"
            self.canvas.create_line(x, 0, x, height, fill=color, tags="grid")
        
        for y in range(int(start_y), height, grid_step):
            color = "#333333" if (y - center_y) % grid_step != 0 else "#444444"
            self.canvas.create_line(0, y, width, y, fill=color, tags="grid")
        for y in range(int(start_y - grid_step), 0, -grid_step):
            color = "#333333" if (y - center_y) % grid_step != 0 else "#444444"
            self.canvas.create_line(0, y, width, y, fill=color, tags="grid")
        
        # метки осей
        self.canvas.create_text(center_x + 15, 15, text="Y", fill="#888888", font=("Roboto", 10, "bold"), tags="grid")
        self.canvas.create_text(width - 15, center_y - 15, text="X", fill="#888888", font=("Roboto", 10, "bold"), tags="grid")

    def on_mouse_wheel(self, event):
        """зум с помощью колеса мыши."""
        if event.delta > 0:
            self.scale_factor *= 1.1
        else:
            self.scale_factor /= 1.1
        self.scale_factor = max(0.1, min(10, self.scale_factor))  # Лимиты зума
        self.redraw_all()

    def redraw_points(self):
        """перерисовывает точки с фиксированным размером."""
        for tag in [f"point_{i}" for i in range(1, self.point_counter)] + [f"text_{i}" for i in range(1, self.point_counter)]:
            self.canvas.delete(tag)
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x, center_y = width // 2, height // 2
        
        for x, y, num in self.points:
            scaled_x = x * self.scale_factor
            scaled_y = y * self.scale_factor
            dot_x = center_x + scaled_x
            dot_y = center_y - scaled_y
            dot_size = 5  # фиксированный размер точки
            self.canvas.create_oval(dot_x - dot_size, dot_y - dot_size, dot_x + dot_size, dot_y + dot_size, 
                                   fill="#A8E4A0", outline="white", width=2, tags=f"point_{num}")
            self.canvas.create_text(dot_x + 10, dot_y + 10, text=str(num), 
                                   fill="white", font=("Roboto", 10, "bold"), tags=f"text_{num}")

    def on_canvas_click(self, event):
        """обработчик клика по канвасу с учетом зума."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x, center_y = width // 2, height // 2
        x = (event.x - center_x) / self.scale_factor
        y = (center_y - event.y) / self.scale_factor
        x = round(x)
        y = round(y)
        
        if x == 0 and y == 0:
            return
            
        self.points.append((x, y, self.point_counter))
        self.redraw_points()
        
        print(f"Point {self.point_counter}: ({x}, {y})")
        self.point_counter += 1
        self.status_var.set(f"Point {self.point_counter-1} added at ({x}, {y})")
        
    def delete_last_point(self):
        """удаляет последнюю точку."""
        if not self.points:
            return
        point_num = self.points[-1][2]
        self.points.pop()
        self.point_counter -= 1
        self.canvas.delete(f"point_{point_num}")
        self.canvas.delete(f"text_{point_num}")
        self.status_var.set(f"Point {point_num} deleted")
        
    def delete_specific_point(self):
        """удаляет конкретную точку по номеру."""
        if not self.points:
            messagebox.showinfo("Info", "No points to delete")
            return
        
        num_str = ctk.CTkInputDialog(text="Enter point number to delete:", title="Delete Point").get_input()
        if num_str is None:
            return
        try:
            num = int(num_str)
            for i, (_, _, point_num) in enumerate(self.points):
                if point_num == num:
                    del self.points[i]
                    self.canvas.delete(f"point_{num}")
                    self.canvas.delete(f"text_{num}")
                    # Переименовываем последующие точки
                    for j in range(i, len(self.points)):
                        old_num = self.points[j][2]
                        new_num = old_num - 1
                        self.points[j] = (self.points[j][0], self.points[j][1], new_num)
                        self.canvas.delete(f"point_{old_num}")
                        self.canvas.delete(f"text_{old_num}")
                    self.point_counter -= 1
                    self.redraw_points()
                    self.status_var.set(f"Point {num} deleted")
                    return
            messagebox.showerror("Error", f"Point {num} not found")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")
        
    def delete_all_points(self):
        """удаляет все точки."""
        if not self.points:
            return
        for i in range(1, self.point_counter):
            self.canvas.delete(f"point_{i}")
            self.canvas.delete(f"text_{i}")
        self.points = []
        self.point_counter = 1
        self.per_point_commands = {}
        self.status_var.set("All points deleted")
        
    def show_coordinates(self):
        """показывает координаты всех точек."""
        if not self.points:
            messagebox.showinfo("Info", "No points to show")
            return
        coords_text = "Coordinates for game:\n\n"
        for x, y, num in self.points:
            coords_text += f"Point {num}: {x} {-y}\n"
        
        coord_window = ctk.CTkToplevel(self)
        coord_window.title("Coordinates")
        coord_window.geometry("300x400")
        coord_window.resizable(False, False)
        text_widget = ctk.CTkTextbox(coord_window, width=280, height=380, fg_color="#3A3A3A", text_color="white", font=ctk.CTkFont(family="Roboto", size=14))
        text_widget.pack(padx=10, pady=10, fill="both", expand=True)
        text_widget.insert("0.0", coords_text)
        text_widget.configure(state="disabled")
        
    def edit_per_point_commands(self):
        """редактор пер-точечных команд."""
        if not self.points:
            messagebox.showinfo("Info", "No points to edit commands")
            return
       
        editor_window = ctk.CTkToplevel(self)
        editor_window.title("Per-Point Commands Editor")
        editor_window.geometry("600x500")
       
        point_list = ctk.CTkScrollableFrame(editor_window, fg_color="transparent")
        point_list.pack(fill="both", expand=True, padx=10, pady=10)
       
        self.point_command_texts = {}
       
        for _, _, num in self.points:
            frame = ctk.CTkFrame(point_list)
            frame.pack(fill="x", pady=5)
           
            ctk.CTkLabel(frame, text=f"Point {num}:", font=ctk.CTkFont(family="Roboto", size=12)).pack(side="left", padx=5)
           
            text = ctk.CTkTextbox(frame, width=450, height=100, fg_color="#3A3A3A", text_color="white", font=ctk.CTkFont(family="Roboto", size=14))
            text.pack(side="left", fill="x", expand=True, padx=5)
            commands = self.per_point_commands.get(num, self.commands_text.get("0.0", "end").strip())
            text.insert("0.0", commands)
            self.point_command_texts[num] = text
           
            use_default = ctk.CTkCheckBox(frame, text="Use Default", command=lambda n=num: self.toggle_use_default(n))
            if num not in self.per_point_commands:
                use_default.select()
            use_default.pack(side="right", padx=5)
       
        def save():
            for num, text in self.point_command_texts.items():
                cmds = text.get("0.0", "end").strip()
                if cmds != self.commands_text.get("0.0", "end").strip():
                    self.per_point_commands[num] = cmds
                elif num in self.per_point_commands:
                    del self.per_point_commands[num]
            editor_window.destroy()
            self.status_var.set("Per-point commands saved")
        
        ctk.CTkButton(editor_window, text="Save", command=save, font=ctk.CTkFont(family="Roboto", size=12)).pack(pady=10)

    def toggle_use_default(self, num):
        """переключение на дефолтные команды."""
        text = self.point_command_texts[num]
        text.delete("0.0", "end")
        text.insert("0.0", self.commands_text.get("0.0", "end").strip())
    
    def show_info(self):
        """показывает информацию о программе, ссылки и ченджлог."""
        info_window = ctk.CTkToplevel(self)
        info_window.title("About Aether Config Generator")
        info_window.geometry("500x400")
        
        info_text = ctk.CTkTextbox(info_window, width=480, height=380, fg_color="#3A3A3A", text_color="white", font=ctk.CTkFont(family="Roboto", size=14))
        info_text.pack(padx=10, pady=10, fill="both", expand=True)
        
        content = """Aether Config Generator v2.0

Created by lapuhhh
Powered by Deepseek & Grok & Chatbotchatapp.com & kami

Discord: lapuhhh

Links:
- Hello!: https://www.youtube.com/watch?v=ax1zuFT0Ibc

Changelog:
- v2.0: Initial release

"""
        info_text.insert("0.0", content)
        info_text.configure(state="disabled")

    def encrypt_data(self, data):
        """шифрует данные с помощью base64."""
        json_data = json.dumps(data)
        encoded_bytes = base64.b64encode(json_data.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    
    def decrypt_data(self, encrypted_data):
        """расшифровывает данные из base64."""
        try:
            decoded_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            json_data = decoded_bytes.decode('utf-8')
            return json.loads(json_data)
        except (base64.binascii.Error, json.JSONDecodeError, UnicodeDecodeError):
            return None
    
    def export_points(self):
        """экспортирует точки и кастомные команды в зашифрованный файл."""
        if not self.points:
            messagebox.showerror("Error", "No points to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save points file"
        )
        
        if not file_path:
            return
            
        try:
            # создаем структуру данных для экспорта
            export_data = {
                'points': self.points,
                'point_counter': self.point_counter,
                'bind_key': self.bind_key.get(),
                'folder_name': self.folder_name.get(),
                'commands': self.commands_text.get("0.0", "end").strip(),
                'per_point_commands': {str(k): v for k, v in self.per_point_commands.items()},  # Преобразуем ключи в строки
                'scale_factor': self.scale_factor
            }
            
            # шифруем данные
            encrypted_data = self.encrypt_data(export_data)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(encrypted_data)
                
            self.status_var.set(f"Points and commands exported to {os.path.basename(file_path)}")
            messagebox.showinfo("Success", f"Points and commands successfully exported to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export points and commands: {str(e)}")
    
    def import_points(self):
        """импортирует точки и кастомные команды из зашифрованного файла."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Aether cfg", "*.txt"), ("All files", "*.*")],
            title="Open txt file (config)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                encrypted_data = f.read().strip()
                
            # расшифровываем данные
            import_data = self.decrypt_data(encrypted_data)
            
            if not import_data or 'points' not in import_data:
                messagebox.showerror("Error", "Invalid or corrupted points file")
                return
                
            # очищаем текущие точки и команды
            self.delete_all_points()
            
            # загружаем импортированные данные
            self.points = import_data['points']
            self.point_counter = import_data.get('point_counter', len(self.points) + 1)
            self.scale_factor = import_data.get('scale_factor', 1.0)
            
            if 'bind_key' in import_data:
                self.bind_key.set(import_data['bind_key'])
            if 'folder_name' in import_data:
                self.folder_name.set(import_data['folder_name'])
            if 'commands' in import_data:
                self.commands_text.delete("0.0", "end")
                self.commands_text.insert("0.0", import_data['commands'])
            if 'per_point_commands' in import_data:
                # Преобразуем строковые ключи обратно в числа
                self.per_point_commands = {int(k): v for k, v in import_data['per_point_commands'].items()}
            
            # перерисовываем
            self.redraw_all()
            
            self.status_var.set(f"Points and commands imported from {os.path.basename(file_path)}")
            messagebox.showinfo("Success", f"Successfully imported {len(self.points)} points and commands")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import points and commands: {str(e)}")
        
    def generate_configs(self):
        """генерирует конфигурационные файлы."""
        if not self.points:
            messagebox.showerror("Error", "No points to generate configs")
            return
        
        default_cmds = self.commands_text.get("0.0", "end").strip().split('\n')
        appdata_path = Path(os.environ['APPDATA'])
        folder_path = appdata_path / "DDnet" / self.folder_name.get()
        folder_path.mkdir(parents=True, exist_ok=True)
        
        for i, (x, y, num) in enumerate(self.points):
            next_index = (i + 1) % len(self.points)
            next_num = self.points[next_index][2]
            opposite_x = -x
            opposite_y = y
            
            config_content = f"# generated by lapuhhh \n# discord: lapuhhh \n\nbind {self.bind_key.get()} \"exec {self.folder_name.get()}/{next_num}\"\n"
            
            cmds = self.per_point_commands.get(num, '\n'.join(default_cmds)).split('\n')
            
            for cmd in cmds:
                if cmd.strip():
                    processed_cmd = cmd.strip()
                    processed_cmd = processed_cmd.replace("%coord%", f"{x} {-y}")
                    processed_cmd = processed_cmd.replace("%opposite%", f"{opposite_x} {opposite_y}")
                    processed_cmd = processed_cmd.replace("%next%", f"{next_num}")
                    config_content += f"{processed_cmd}\n"
            
            config_file = folder_path / f"{num}"
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)
        
        bind_info = f"bind {self.bind_key.get()} \"exec {self.folder_name.get()}/1\""
        with open(folder_path / "✦ bind_info.txt", 'w', encoding='utf-8') as f:
            f.write(bind_info)
        
        self.info_text.configure(state="normal")
        self.info_text.delete("0.0", "end")
        self.info_text.insert("0.0", f"Configs generated successfully!\n\nFolder: {folder_path}\n\nUse command:\n{bind_info}")
        self.info_text.configure(state="disabled")
        self.status_var.set("Configs generated successfully!")
        messagebox.showinfo("Success", f"Configs generated!\n\nUse command:\n{bind_info}")

if __name__ == "__main__":
    app = main()
    app.mainloop()