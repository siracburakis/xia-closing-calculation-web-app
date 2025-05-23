# pages/home.py

from nicegui import ui
from layouts.base_layout import base_layout

@ui.page("/")
def home_page():
    def content():
        with ui.column().classes("items-center justify-center w-full px-8"):
            ui.label("Welcome to the Xiaomi Calculation Web App").classes("text-3xl font-bold text-center mt-6")

            with ui.row().classes("gap-6 mt-10 flex-wrap justify-center"):

                # Dashboard Card
                with ui.card().classes("w-80 p-6 bg-gradient-to-br from-blue-600 to-blue-400 text-white shadow-md rounded-2xl"):
                    ui.icon("analytics").classes("text-4xl mb-2")
                    ui.label("Dashboard").classes("text-xl font-semibold mb-1")
                    ui.label("View data insights and charts").classes("text-sm mb-4 text-white/80 text-center")
                    ui.button("Go to Dashboard", on_click=lambda: ui.run_javascript("window.location.href='/dashboard'")) \
                        .props("flat") \
                        .style("color: rgb(37, 99, 235) !important") \
                        .classes("bg-white font-semibold px-4 py-2 rounded hover:bg-blue-50 transition-all")

                # Calculation Page Card
                with ui.card().classes("w-80 p-6 bg-gradient-to-br from-purple-600 to-purple-400 text-white shadow-md rounded-2xl"):
                    ui.icon("calculate").classes("text-4xl mb-2")
                    ui.label("Calculation Page").classes("text-xl font-semibold mb-1")
                    ui.label("Upload, process, and export Excel files").classes("text-sm mb-4 text-white/80 text-center")
                    ui.button("Go to Calculation", on_click=lambda: ui.run_javascript("window.location.href='/calculation'")) \
                        .props("flat") \
                        .style("color: rgb(147, 51, 234) !important") \
                        .classes("bg-white font-semibold px-4 py-2 rounded hover:bg-purple-50 transition-all")

                # Manual Edit Page Card
                with ui.card().classes("w-80 p-6 bg-gradient-to-br from-green-600 to-green-400 text-white shadow-md rounded-2xl"):
                    ui.icon("edit").classes("text-4xl mb-2")
                    ui.label("Manual Edit").classes("text-xl font-semibold mb-1")
                    ui.label("Edit data manually").classes("text-sm mb-4 text-white/80 text-center")
                    ui.button("Go to Manual Edit", on_click=lambda: ui.run_javascript("window.location.href='/manual_edit'")) \
                        .props("flat") \
                        .style("color: rgb(22, 163, 74) !important") \
                        .classes("bg-white font-semibold px-4 py-2 rounded hover:bg-green-50 transition-all")

    base_layout(content, current_url="/")
