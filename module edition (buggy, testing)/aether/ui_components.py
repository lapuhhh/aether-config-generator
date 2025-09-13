import customtkinter as ctk
from tkinter import messagebox
from canvas_utils import on_canvas_resize, on_mouse_wheel, on_canvas_click, delete_last_point, delete_specific_point, delete_all_points, show_coordinates, draw_grid
from data_management import export_points, import_points, generate_configs

def create_widgets(app):
    """Создает и настраивает виджеты интерфейса."""
    # основной фрейм
    main_frame = ctk.CTkFrame(app, fg_color="transparent")
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
        command=lambda: show_info(app),
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
    
    canvas_label = ctk.CTkLabel(
        left_frame, 
        text="Coordinate Canvas", 
        font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
        text_color="#B0B0B0"
    )
    canvas_label.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=15)
    
    app.canvas = ctk.CTkCanvas(
        left_frame, 
        width=550, 
        height=550, 
        bg="#1E1E1E", 
        highlightthickness=0
    )
    app.canvas.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
    app.canvas.bind("<Button-1>", lambda event: on_canvas_click(app, event))
    app.canvas.bind("<Configure>", lambda event: on_canvas_resize(app, event))
    app.canvas.bind("<MouseWheel>", lambda event: on_mouse_wheel(app, event))
    draw_grid(app)  # Исправлено: вызов функции из canvas_utils.py
    
    # кнопки управления
    btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    btn_frame.grid(row=2, column=0, pady=(0, 10))
    
    ctk.CTkButton(
        btn_frame, 
        text="Delete Last", 
        command=lambda: delete_last_point(app),
        fg_color="#4A4A4A",
        hover_color="#5A5A5A",
        font=ctk.CTkFont(family="Roboto", size=12)
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        btn_frame, 
        text="Delete Specific", 
        command=lambda: delete_specific_point(app),
        fg_color="#4A4A4A",
        hover_color="#5A5A5A",
        font=ctk.CTkFont(family="Roboto", size=12)
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        btn_frame, 
        text="Clear All", 
        command=lambda: delete_all_points(app),
        fg_color="#4A4A4A",
        hover_color="#5A5A5A",
        font=ctk.CTkFont(family="Roboto", size=12)
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        btn_frame, 
        text="Show Coordinates", 
        command=lambda: show_coordinates(app),
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
        command=lambda: export_points(app),
        fg_color="#2E8B57",
        hover_color="#3CB371",
        font=ctk.CTkFont(family="Roboto", size=12)
    ).pack(side="left", padx=5)
    ctk.CTkButton(
        import_export_frame, 
        text="Import", 
        command=lambda: import_points(app),
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
    
    settings_label = ctk.CTkLabel(
        right_frame, 
        text="Configuration Settings",
        font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
        text_color="#B0B0B0"
    )
    settings_label.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=15)
    
    ctk.CTkLabel(
        right_frame, 
        text="Bind Key:",
        font=ctk.CTkFont(family="Roboto", size=12),
        text_color="#E0E0E0"
    ).grid(row=1, column=0, sticky="w", pady=(0, 5), padx=15)
    bind_entry = ctk.CTkEntry(
        right_frame, 
        textvariable=app.bind_key, 
        width=120,
        font=ctk.CTkFont(family="Roboto", size=12),
        fg_color="#3A3A3A",
        border_color="#5A5A5A"
    )
    bind_entry.grid(row=2, column=0, sticky="w", pady=(0, 15), padx=15)
    
    ctk.CTkLabel(
        right_frame, 
        text="Folder Name:",
        font=ctk.CTkFont(family="Roboto", size=12),
        text_color="#E0E0E0"
    ).grid(row=3, column=0, sticky="w", pady=(0, 5), padx=15)
    folder_entry = ctk.CTkEntry(
        right_frame, 
        textvariable=app.folder_name,
        font=ctk.CTkFont(family="Roboto", size=12),
        fg_color="#3A3A3A",
        border_color="#5A5A5A"
    )
    folder_entry.grid(row=4, column=0, sticky="ew", pady=(0, 15), padx=15)
    
    ctk.CTkLabel(
        right_frame, 
        text="Default Custom Commands:",
        font=ctk.CTkFont(family="Roboto", size=12),
        text_color="#E0E0E0"
    ).grid(row=5, column=0, sticky="w", pady=(0, 5), padx=15)
    app.commands_text = ctk.CTkTextbox(right_frame, width=400, height=150, fg_color="#3A3A3A", text_color="white", font=ctk.CTkFont(family="Roboto", size=14))
    app.commands_text.grid(row=6, column=0, sticky="nsew", pady=(0, 15), padx=15)
    app.commands_text.insert("0.0", app.default_commands)
    
    per_point_btn = ctk.CTkButton(
        right_frame, 
        text="Edit Per-Point Commands",
        command=lambda: edit_per_point_commands(app),
        fg_color="#4A4A4A",
        hover_color="#5A5A5A",
        font=ctk.CTkFont(family="Roboto", size=12)
    )
    per_point_btn.grid(row=7, column=0, pady=(0, 15), padx=15, sticky="w")
    
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
    
    generate_btn = ctk.CTkButton(
        right_frame, 
        text="Generate Configs",
        command=lambda: generate_configs(app),
        fg_color="#4A4A4A",
        hover_color="#5A5A5A",
        font=ctk.CTkFont(family="Roboto", size=14, weight="bold")
    )
    generate_btn.grid(row=9, column=0, pady=(10, 15), padx=15)
    
    app.info_text = ctk.CTkTextbox(right_frame, width=400, height=100, fg_color="#3A3A3A", text_color="#B0B0B0", font=ctk.CTkFont(family="Roboto", size=14))
    app.info_text.grid(row=10, column=0, sticky="nsew", pady=(0, 15), padx=15)
    app.info_text.insert("0.0", "Configure settings and click 'Generate Configs'")
    app.info_text.configure(state="disabled")
    
    right_frame.rowconfigure(6, weight=1)
    right_frame.rowconfigure(10, weight=1)
    
    app.status_var = ctk.StringVar(value="Ready")
    status_bar = ctk.CTkLabel(
        app, 
        textvariable=app.status_var, 
        anchor="w",
        font=ctk.CTkFont(family="Roboto", size=12),
        text_color="#B0B0B0"
    )
    status_bar.pack(side="bottom", fill="x", padx=20, pady=10)

def show_info(app):
    """Показывает информацию о программе, ссылки и ченджлог."""
    info_window = ctk.CTkToplevel(app)
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

def edit_per_point_commands(app):
    """Редактор пер-точечных команд."""
    if not app.points:
        messagebox.showinfo("Info", "No points to edit commands")
        return
    
    editor_window = ctk.CTkToplevel(app)
    editor_window.title("Per-Point Commands Editor")
    editor_window.geometry("600x500")
    
    point_list = ctk.CTkScrollableFrame(editor_window, fg_color="transparent")
    point_list.pack(fill="both", expand=True, padx=10, pady=10)
    
    app.point_command_texts = {}
    
    for _, _, num in app.points:
        frame = ctk.CTkFrame(point_list)
        frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(frame, text=f"Point {num}:", font=ctk.CTkFont(family="Roboto", size=12)).pack(side="left", padx=5)
        
        text = ctk.CTkTextbox(frame, width=450, height=100, fg_color="#3A3A3A", text_color="white", font=ctk.CTkFont(family="Roboto", size=14))
        text.pack(side="left", fill="x", expand=True, padx=5)
        commands = app.per_point_commands.get(num, app.commands_text.get("0.0", "end").strip())
        text.insert("0.0", commands)
        app.point_command_texts[num] = text
        
        use_default = ctk.CTkCheckBox(frame, text="Use Default", command=lambda n=num: toggle_use_default(app, n))
        if num not in app.per_point_commands:
            use_default.select()
        use_default.pack(side="right", padx=5)
    
    def save():
        for num, text in app.point_command_texts.items():
            cmds = text.get("0.0", "end").strip()
            if cmds != app.commands_text.get("0.0", "end").strip():
                app.per_point_commands[num] = cmds
            elif num in app.per_point_commands:
                del app.per_point_commands[num]
        editor_window.destroy()
        app.status_var.set("Per-point commands saved")
    
    ctk.CTkButton(editor_window, text="Save", command=save, font=ctk.CTkFont(family="Roboto", size=12)).pack(pady=10)

def toggle_use_default(app, num):
    """Переключение на дефолтные команды."""
    text = app.point_command_texts[num]
    text.delete("0.0", "end")
    text.insert("0.0", app.commands_text.get("0.0", "end").strip())