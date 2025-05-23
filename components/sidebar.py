# components/sidebar.py

from nicegui import ui

def create_sidebar(current_url="/"):
    links = {
        "Home": ("/", "home"),
        "Dashboard": ("/dashboard", "analytics"),
        "Calculation": ("/calculation", "calculate"),
        "Manual Edit": ("/manual_edit", "edit"),
        "Test Page": ("/test_page", "brush"),
    }

    ui.label("Navigation Menu").classes("text-lg font-bold mt-2 mb-2 pl-2 dark:text-gray-200")

    for name, (url, icon) in links.items():
        is_active = url == current_url
        base_classes = "w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-all"
        hover_classes = "hover:bg-gradient-to-r hover:from-blue-500 hover:to-blue-700 dark:hover:from-blue-600 dark:hover:to-blue-800"
        active_classes = "bg-blue-700 dark:bg-blue-800 font-semibold shadow" if is_active else ""
    
        with ui.button(
            on_click=lambda url=url: ui.run_javascript(f"window.location.href='{url}'")
        ).classes(f"{base_classes} {hover_classes} {active_classes}").style("background-color: transparent; color: white;"
        ):
            ui.icon(icon).classes("text-white dark:text-gray-200 mr-2") 
            ui.label(name).classes("text-white dark:text-gray-200 flex-1").tooltip(f"Navigate to {name}")
    
    with ui.element("div").classes("mt-auto pt-6 text-center text-sm text-gray-400 dark:text-gray-500"):
        with ui.row().classes("gap-2 mt-10 flex items-center justify-center"):
            ui.label("© 2025 GFC Loyalty").classes("my-auto dark:text-gray-400")
            ui.icon("info").classes("text-gray-400 dark:text-gray-500").tooltip("Xiaomi Calculation System v1.0")