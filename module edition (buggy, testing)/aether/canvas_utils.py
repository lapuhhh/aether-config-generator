from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox

def load_and_display_tee(app):
    """Загружает тишку и отображает его в центре канваса с масштабированием по сетке."""
    try:
        img = Image.open(app.tee_filename)
        scaled_size = (int(55 * app.scale_factor), int(55 * app.scale_factor))
        img = img.resize(scaled_size, Image.LANCZOS)
        app.tk_tee = ImageTk.PhotoImage(img)

        width = app.canvas.winfo_width()
        height = app.canvas.winfo_height()
        center_x, center_y = width // 2, height // 2
        tee_x = center_x - scaled_size[0] // 2
        tee_y = center_y - scaled_size[1] // 2

        if app.tee_id:
            app.canvas.delete(app.tee_id)
        app.tee_id = app.canvas.create_image(tee_x, tee_y, anchor="nw", image=app.tk_tee)
        app.canvas.tag_raise(app.tee_id, "grid")  # Исправлено: поднимаем tee над сеткой

    except FileNotFoundError:
        print(f"Error: tee file '{app.tee_filename}' not found.")
    except Exception as e:
        print(f"Error loading tee: {e}")

def draw_grid(app):
    """Рисует сетку на канвасе с учетом зума, исправляя смещение."""
    app.canvas.delete("grid")
    width = app.canvas.winfo_width()
    height = app.canvas.winfo_height()
    
    if width <= 1 or height <= 1:
        app.after(100, lambda: draw_grid(app))
        return
    
    center_x, center_y = width // 2, height // 2
    grid_step = int(32 * app.scale_factor)
    
    app.canvas.create_line(0, center_y, width, center_y, fill="#444444", width=2, tags="grid")
    app.canvas.create_line(center_x, 0, center_x, height, fill="#444444", width=2, tags="grid")
    
    start_x = center_x - (center_x // grid_step) * grid_step
    start_y = center_y - (center_y // grid_step) * grid_step
    
    for x in range(int(start_x), width, grid_step):
        color = "#333333" if (x - center_x) % grid_step != 0 else "#444444"
        app.canvas.create_line(x, 0, x, height, fill=color, tags="grid")
    for x in range(int(start_x - grid_step), 0, -grid_step):
        color = "#333333" if (x - center_x) % grid_step != 0 else "#444444"
        app.canvas.create_line(x, 0, x, height, fill=color, tags="grid")
    
    for y in range(int(start_y), height, grid_step):
        color = "#333333" if (y - center_y) % grid_step != 0 else "#444444"
        app.canvas.create_line(0, y, width, y, fill=color, tags="grid")
    for y in range(int(start_y - grid_step), 0, -grid_step):
        color = "#333333" if (y - center_y) % grid_step != 0 else "#444444"
        app.canvas.create_line(0, y, width, y, fill=color, tags="grid")
    
    app.canvas.create_text(center_x + 15, 15, text="Y", fill="#888888", font=("Roboto", 10, "bold"), tags="grid")
    app.canvas.create_text(width - 15, center_y - 15, text="X", fill="#888888", font=("Roboto", 10, "bold"), tags="grid")

def on_canvas_resize(app, event):
    """Обработчик изменения размера канваса."""
    redraw_all(app)

def redraw_all(app):
    """Перерисовывает сетку, логотип и точки с учетом зума."""
    draw_grid(app)
    load_and_display_tee(app)
    redraw_points(app)

def redraw_points(app):
    """Перерисовывает точки с фиксированным размером."""
    for tag in [f"point_{i}" for i in range(1, app.point_counter)] + [f"text_{i}" for i in range(1, app.point_counter)]:
        app.canvas.delete(tag)
    
    width = app.canvas.winfo_width()
    height = app.canvas.winfo_height()
    center_x, center_y = width // 2, height // 2
    
    for x, y, num in app.points:
        scaled_x = x * app.scale_factor
        scaled_y = y * app.scale_factor
        dot_x = center_x + scaled_x
        dot_y = center_y - scaled_y
        dot_size = 5
        app.canvas.create_oval(dot_x - dot_size, dot_y - dot_size, dot_x + dot_size, dot_y + dot_size, 
                               fill="#A8E4A0", outline="white", width=2, tags=f"point_{num}")
        app.canvas.create_text(dot_x + 10, dot_y + 10, text=str(num), 
                               fill="white", font=("Roboto", 10, "bold"), tags=f"text_{num}")

def on_mouse_wheel(app, event):
    """Зум с помощью колеса мыши."""
    if event.delta > 0:
        app.scale_factor *= 1.1
    else:
        app.scale_factor /= 1.1
    app.scale_factor = max(0.1, min(10, app.scale_factor))
    redraw_all(app)

def on_canvas_click(app, event):
    """Обработчик клика по канвасу с учетом зума."""
    width = app.canvas.winfo_width()
    height = app.canvas.winfo_height()
    center_x, center_y = width // 2, height // 2
    x = (event.x - center_x) / app.scale_factor
    y = (center_y - event.y) / app.scale_factor
    x = round(x)
    y = round(y)
    
    if x == 0 and y == 0:
        return
        
    app.points.append((x, y, app.point_counter))
    redraw_points(app)
    
    print(f"Point {app.point_counter}: ({x}, {y})")
    app.point_counter += 1
    app.status_var.set(f"Point {app.point_counter-1} added at ({x}, {y})")

def delete_last_point(app):
    """Удаляет последнюю точку."""
    if not app.points:
        return
    point_num = app.points[-1][2]
    app.points.pop()
    app.point_counter -= 1
    app.canvas.delete(f"point_{point_num}")
    app.canvas.delete(f"text_{point_num}")
    app.status_var.set(f"Point {point_num} deleted")

def delete_specific_point(app):
    """Удаляет конкретную точку по номеру."""
    if not app.points:
        messagebox.showinfo("Info", "No points to delete")
        return
    
    num_str = ctk.CTkInputDialog(text="Enter point number to delete:", title="Delete Point").get_input()
    if num_str is None:
        return
    try:
        num = int(num_str)
        for i, (_, _, point_num) in enumerate(app.points):
            if point_num == num:
                del app.points[i]
                app.canvas.delete(f"point_{num}")
                app.canvas.delete(f"text_{num}")
                for j in range(i, len(app.points)):
                    old_num = app.points[j][2]
                    new_num = old_num - 1
                    app.points[j] = (app.points[j][0], app.points[j][1], new_num)
                    app.canvas.delete(f"point_{old_num}")
                    app.canvas.delete(f"text_{old_num}")
                app.point_counter -= 1
                redraw_points(app)
                app.status_var.set(f"Point {num} deleted")
                return
        messagebox.showerror("Error", f"Point {num} not found")
    except ValueError:
        messagebox.showerror("Error", "Invalid number")

def delete_all_points(app):
    """Удаляет все точки."""
    if not app.points:
        return
    for i in range(1, app.point_counter):
        app.canvas.delete(f"point_{i}")
        app.canvas.delete(f"text_{i}")
    app.points = []
    app.point_counter = 1
    app.per_point_commands = {}
    app.status_var.set("All points deleted")

def show_coordinates(app):
    """Показывает координаты всех точек."""
    if not app.points:
        messagebox.showinfo("Info", "No points to show")
        return
    coords_text = "Coordinates for game:\n\n"
    for x, y, num in app.points:
        coords_text += f"Point {num}: {x} {-y}\n"
    
    coord_window = ctk.CTkToplevel(app)
    coord_window.title("Coordinates")
    coord_window.geometry("300x400")
    coord_window.resizable(False, False)
    text_widget = ctk.CTkTextbox(coord_window, width=280, height=380, fg_color="#3A3A3A", text_color="white", font=ctk.CTkFont(family="Roboto", size=14))
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)
    text_widget.insert("0.0", coords_text)
    text_widget.configure(state="disabled")