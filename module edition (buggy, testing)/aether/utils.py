def set_window_icon(app, icon_path):
    """Sets the window icon for the application."""
    try:
        app.iconbitmap(icon_path)
    except Exception as e:
        print(f"Error setting icon: {e}")