from nicegui import ui
from layouts.base_layout import base_layout
import pandas as pd
from io import BytesIO
import os
import sys
import io as io_mod
import threading
from datetime import datetime

@ui.page("/calculation")
def calculation():
    base_layout(upload_section, current_url="/calculation")

def upload_section():
    df_holder = {"df": None}
    result_holder = {"buffer": None, "result_df": None}
    
    with ui.column().classes("w-full max-w-[1100px] mx-auto px-6"):
        ui.label("🧮 Excel Calculation Page").classes("text-3xl font-bold text-gray-800 dark:text-gray-100 mt-6 mb-2")
        # Button Row
        with ui.row().classes("w-full gap-4 mb-4"):
            ui.upload(on_upload=lambda e: handle_upload_with_preview(
                e, df_holder, preview_card, preview_table)
            ).props('accept=.xlsx,.xls') \
             .classes("bg-white border px-4 py-2 rounded-md")

            ui.button("▶️ Run Function", on_click=lambda: threading.Thread(
                target=lambda: run_code(df_holder, code_input, log_output,
                                      result_holder, result_preview_card, result_table)
            ).start()).classes("bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700")

            ui.button("⬇️ Download File", on_click=lambda: download_excel(result_holder)) \
                .classes("bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700")

        # Upload Preview Section
        preview_card = ui.card().classes("w-full mt-4 hidden")
        with preview_card:
            ui.label("📊 Uploaded Data Preview").classes("text-lg font-semibold mb-2")
            with ui.row().classes("justify-between items-center"):
                ui.label("").bind_text_from(df_holder, 'df', lambda df: f'Rows: {len(df) if df is not None else 0}')
                ui.label("").bind_text_from(df_holder, 'df', lambda df: f'Columns: {len(df.columns) if df is not None else 0}')
            preview_table = ui.aggrid({
                'columnDefs': [],
                'rowData': [],
                'pagination': True,
                'paginationPageSize': 10,
                'defaultColDef': {'sortable': True, 'filter': True, 'resizable': True}
            }).classes("w-full h-[300px] mt-2")

        # Code Input Section
        code_input = ui.textarea(label='Python Code').classes("w-full mt-6 h-40 font-mono")
        log_output = ui.textarea(label='Terminal Output').props('readonly') \
            .classes("w-full h-40 font-mono bg-gray-100 mt-4 text-sm")

        # Result Preview Section
        result_preview_card = ui.card().classes("w-full mt-6 hidden")
        with result_preview_card:
            ui.label("🔄 Result Data Preview").classes("text-lg font-semibold mb-2")
            with ui.row().classes("justify-between items-center"):
                ui.label("").bind_text_from(result_holder, 'result_df', 
                    lambda df: f'Rows: {len(df) if df is not None else 0}')
                ui.label("").bind_text_from(result_holder, 'result_df', 
                    lambda df: f'Columns: {len(df.columns) if df is not None else 0}')
            result_table = ui.aggrid({
                'columnDefs': [],
                'rowData': [],
                'pagination': True,
                'paginationPageSize': 10,
                'defaultColDef': {'sortable': True, 'filter': True, 'resizable': True}
            }).classes("w-full h-[300px] mt-2")

def handle_upload_with_preview(e, df_holder, preview_card, preview_table):
    try:
        os.makedirs("uploads", exist_ok=True)
        path = f"uploads/{e.name}"
        with open(path, "wb") as f:
            f.write(e.content.read())
        df = pd.read_excel(path)
        df_holder["df"] = df

        preview_data = df.head(100)
        for col in preview_data.select_dtypes(include=['datetime64[ns]']).columns:
            preview_data[col] = preview_data[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        preview_table.options['columnDefs'] = [
            {'field': str(col), 'headerName': str(col), 'flex': 1} 
            for col in preview_data.columns
        ]
        preview_table.options['rowData'] = preview_data.to_dict('records')
        preview_table.update()
        preview_card.classes(remove="hidden")

        ui.notify(f"✅ File uploaded: {df.shape[0]} rows", type='positive')
    except Exception as ex:
        ui.notify(f"❌ Upload failed: {ex}", type='negative')

def run_code(df_holder, code_input, log_output, result_holder, result_preview_card, result_table):
    df = df_holder.get("df")
    if df is None:
        ui.notify("⚠️ No DataFrame uploaded!", type='warning')
        return
    try:
        buffer_out = io_mod.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = buffer_out

        # Create namespace for code execution
        namespace = {"df": df.copy(), "pd": pd}
        
        # Execute the code in the namespace
        exec(code_input.value, namespace)
        
        # Get the modified DataFrame from namespace
        result_df = namespace["df"]

        sys.stdout = sys_stdout_original
        log_output.value = buffer_out.getvalue()

        # Update the result preview
        preview_data = result_df.head(100)
        for col in preview_data.select_dtypes(include=['datetime64[ns]']).columns:
            preview_data[col] = preview_data[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        result_table.options['columnDefs'] = [
            {'field': str(col), 'headerName': str(col), 'flex': 1} 
            for col in preview_data.columns
        ]
        result_table.options['rowData'] = preview_data.to_dict('records')
        result_table.update()
        result_preview_card.classes(remove="hidden")

        # Store results
        buffer = BytesIO()
        result_df.to_excel(buffer, index=False)
        buffer.seek(0)
        result_holder["buffer"] = buffer
        result_holder["result_df"] = result_df

        ui.notify("✅ Code executed and file ready to download", type='positive')
    except Exception as ex:
        sys.stdout = sys_stdout_original
        ui.notify(f"❌ Code error: {ex}", type='negative')

def download_excel(result_holder):
    buffer = result_holder.get("buffer")
    if buffer:
        os.makedirs("downloads", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"downloads/calculated_result_{timestamp}.xlsx"
        with open(path, "wb") as f:
            f.write(buffer.getvalue())
        ui.download(src=path)
    else:
        ui.notify("⚠️ No data to download!", type='warning')