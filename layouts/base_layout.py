from nicegui import ui
from components.header import create_header
from components.sidebar import create_sidebar
from components.footer import create_footer

def _inject_custom_css():
    ui.add_head_html('<link rel="stylesheet" href="/static/styles.css">')

def base_layout(content_function, current_url):
    _inject_custom_css()

    # Sidebar (left drawer)
    with ui.left_drawer(fixed=False).classes("sidebar sidebar-drawer").props("bordered") as left_drawer:
        create_sidebar(current_url)

    # Header bar
    with ui.header(elevated=True).classes("header items-center justify-between"):
        ui.button(on_click=left_drawer.toggle, icon="menu").props("flat color=white")
        create_header()

    # Main content area - removed width constraint
    with ui.element("main").classes("main-content flex-1 p-4"):
        content_function()

    # Footer
    # with ui.footer().classes("footer").style("height: 30px; padding: 0 10px;"):
    #     create_footer()