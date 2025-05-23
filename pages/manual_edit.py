from nicegui import ui
from layouts.base_layout import base_layout
from sqlalchemy import create_engine, text
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.db import engine

# --- Data functions ---
def get_column_names():
    try:
        df = pd.read_sql("SELECT TOP 1 * FROM xiaomi_closing_data", engine)
        return list(df.columns)
    except Exception as e:
        print(f"Error fetching columns: {e}")
        return []

def get_closing_tags():
    try:
        df = pd.read_sql("SELECT DISTINCT closing_tag FROM xiaomi_closing_data", engine)
        return list(df['closing_tag'])
    except Exception as e:
        print(f"Error fetching tags: {e}")
        return []

def get_current_value(column, tag):
    try:
        df = pd.read_sql(f"SELECT [{column}] FROM xiaomi_closing_data WHERE closing_tag = ?", 
                         engine, params=(tag,))
        if not df.empty:
            value = df.iloc[0][0]
            # Convert datetime if needed
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            return str(value)
        return "No value found"
    except Exception as e:
        print(f"Error fetching value: {e}")
        return "Error fetching value"

def save_changes(column, tag, new_value):
    try:
        with engine.begin() as conn:
            query = text(f"UPDATE xiaomi_closing_data SET [{column}] = :val WHERE closing_tag = :tag")
            conn.execute(query, {"val": new_value, "tag": tag})
        ui.notify("✅ Value updated successfully!", type='positive')
        return True
    except Exception as e:
        print(f"Error updating: {e}")
        ui.notify(f"❌ Error updating value: {e}", type='negative')
        return False

# --- Page setup ---
@ui.page("/manual_edit")
def manual_edit_page():
    base_layout(show_manual_edit, current_url="/manual_edit")

def show_manual_edit():
    with ui.column().classes("w-full max-w-[1100px] mx-auto px-6"):
        # Page title
        ui.label("📝 Manual Data Edit").classes("text-3xl font-bold text-gray-800 dark:text-gray-100 mt-6 mb-2")

        # Internal state
        state = {"current_value": None}

        async def update_current_value():
            if column_select.value and tag_select.value:
                val = get_current_value(column_select.value, tag_select.value)
                current_value_label.text = f"Current Value: {val}"
                await update_row_preview()

        async def update_row_preview():
            if show_full_row.value and tag_select.value:
                try:
                    df = pd.read_sql(
                        "SELECT * FROM xiaomi_closing_data WHERE closing_tag = ?", 
                        engine, 
                        params=(tag_select.value,)
                    )
                    if not df.empty:
                        # Convert datetime columns to string format
                        for col in df.select_dtypes(include=['datetime64[ns]']).columns:
                            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                        
                        row_preview.columns = [
                            {"name": col, "label": col, "field": col, "align": "left"} 
                            for col in df.columns
                        ]
                        row_preview.rows = df.to_dict(orient="records")
                        row_preview.style("display: block;")
                    else:
                        row_preview.columns = []
                        row_preview.rows = []
                        row_preview.style("display: none;")
                except Exception as e:
                    ui.notify(f"Error loading row: {e}", type='negative')
            else:
                row_preview.style("display: none;")

        # Dropdowns
                # Dropdowns side by side in a grid
        with ui.grid(columns=2).classes('w-full gap-4'):  # Changed from row to grid with 2 columns
            column_select = ui.select(
                label="Select Column",
                options=get_column_names(),
                with_input=True,
                on_change=lambda _: update_current_value()
            ).classes("w-full")

            tag_select = ui.select(
                label="Select Closing Tag",
                options=get_closing_tags(),
                with_input=True,
                on_change=lambda _: update_current_value()
            ).classes("w-full")

        # Value + input
        with ui.row().classes("w-full gap-4 mt-4"):
            current_value_label = ui.label("Current Value: ...") \
                .classes("bg-gray-100 text-gray-700 rounded p-3 w-full text-sm")
            new_value_input = ui.input("New Value").classes("w-full")

        # Save
        async def handle_save():
            if not column_select.value or not tag_select.value or not new_value_input.value:
                ui.notify("⚠️ Please fill all fields", type='warning')
                return

            if save_changes(column_select.value, tag_select.value, new_value_input.value):
                await update_current_value()
                new_value_input.value = ""

        ui.button("💾 Save Changes", on_click=handle_save).classes(
            "bg-blue-600 text-white px-4 py-2 mt-6 rounded hover:bg-blue-700"
        )

        # Show row toggle
        show_full_row = ui.switch("Show full row").classes("mt-6")
        show_full_row.on("update:model-value", lambda _: update_row_preview())

        # Row preview table (initially hidden)
        row_preview = ui.table(columns=[], rows=[]).classes("w-full mt-4").style("display: none;")