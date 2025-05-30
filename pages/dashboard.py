from nicegui import ui
from layouts.base_layout import base_layout
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.db import engine

def fetch_data():
    try:
        df = pd.read_sql("SELECT TOP 15 * FROM xiaomi_closing_data", engine)
        # Convert datetime columns to string format
        for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
        return df.to_dict("records")
    except Exception as e:
        print(f"Database connection failed: {e}")
        return []

def download_excel(df):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"xiaomi_data_{timestamp}.xlsx"
    downloads_path = str(Path.home() / "Downloads" / filename)
    
    try:
        df.to_excel(downloads_path, index=False, engine="openpyxl")
        ui.notify(f"Successfully downloaded to {downloads_path}", type="positive")
    except Exception as e:
        ui.notify(f"Error downloading file: {str(e)}", type="negative")

@ui.page("/dashboard")
def dashboard_page():
    base_layout(show_dashboard, current_url="/dashboard")

def show_dashboard():
    with ui.column().classes("w-full h-full"):
        # Page Title
        ui.label("📊 Xiaomi Dashboard").classes("text-3xl font-bold text-gray-800 dark:text-gray-100 mt-6 mb-2")

        df = pd.DataFrame(fetch_data())
        if df.empty:
            ui.label("⚠️ No data available.").classes("text-red-600 mt-4")
            return

        # Charts Section
        with ui.row().classes("w-full gap-4 flex justify-between"):
            with ui.card().classes("w-[49%] p-6 bg-white rounded-xl shadow-md"):
                ui.label("DC Bonus").classes("text-lg font-semibold text-gray-700 mb-2")
                plot_bar = ui.plotly(
                    px.bar(df, x=df.columns[0], y=df.columns[3], template="plotly_white")
                ).classes("w-full h-[500px]")

            with ui.card().classes("w-[49%] p-6 bg-white rounded-xl shadow-md"):
                ui.label("MD Bonus").classes("text-lg font-semibold text-gray-700 mb-2")
                plot_line = ui.plotly(
                    px.line(df, x=df.columns[12], y=df.columns[2], template="plotly_white", markers=True)
                ).classes("w-full h-[500px]")

        # Table Section
        with ui.card().classes("w-full mt-8 p-6 bg-white rounded-xl shadow-md"):
            with ui.row().classes("justify-between items-center mb-4"):
                ui.label("📋 Interactive Table").classes("text-xl font-semibold text-gray-700")
                with ui.row().classes("gap-2"):
                    ui.button("📥 Download Excel", on_click=lambda: download_excel(df)).classes(
                        "bg-green-600 text-white px-5 py-2 rounded-md hover:bg-green-700"
                    )
                    ui.button("🔄 Refresh", on_click=lambda: refresh()).classes(
                        "bg-blue-600 text-white px-5 py-2 rounded-md hover:bg-blue-700"
                    )

            grid_options = {
                "columnDefs": [
                    {"field": col, "sortable": True, "filter": True, "resizable": True} 
                    for col in df.columns
                ],
                "rowData": df.to_dict("records"),
                "pagination": True,
                "paginationPageSize": 15,
                "rowSelection": "multiple",
                "domLayout": "normal",
                "animateRows": True,
                "defaultColDef": {
                    "flex": 1,
                    "minWidth": 120,
                    "filter": True,
                    "sortable": True,
                    "resizable": True
                }
            }

            grid = ui.aggrid(options=grid_options).classes("w-full h-[600px] overflow-hidden")

            def refresh():
                new_data = fetch_data()
                new_df = pd.DataFrame(new_data)
                if not new_df.empty:
                    # Update Table - Use the correct update syntax
                    grid.options["rowData"] = new_data
                    grid.update()
                    print("Grid updated with new data.")

                    plot_bar.update_figure(
                        px.bar(new_df, x=new_df.columns[0], y=new_df.columns[3], 
                        template="plotly_white")
                    )
                    plot_line.update_figure(
                        px.line(new_df, x=new_df.columns[11], y=new_df.columns[2], 
                        template="plotly_white")
                    )
                    print("Plots updated with new data.")