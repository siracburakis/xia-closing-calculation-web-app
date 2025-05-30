from nicegui import ui

dark = ui.dark_mode()
ui.switch("Dark mode").bind_value(dark)

def create_header():
    with ui.row().classes("items-center p-1"):
        ui.image("static/logo.png").classes("w-6 h-6 mr-2")
        ui.label("Xiaomi Calculation Web App").classes("text-base font-semibold text-white")
        ui.switch("Dark Mode", on_change=lambda e: ui.dark_mode().enable() if e.value else ui.dark_mode().disable())
