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
    df_holder = {"df": None, "file_info": {"name": "", "size": 0, "upload_time": ""}}
    result_holder = {"buffer": None, "result_df": None, "execution_time": 0}
    
    # Remove the max-width constraint
    with ui.column().classes("w-full, h-full"):
        # Hero Section
        with ui.card().classes("w-full mx-auto max-w-5xl mb-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white"):
            with ui.card_section().classes("text-center py-8 mx-auto"):
                ui.icon("calculate", size="3rem").classes("mb-2")
                ui.label("Excel Data Processing Studio").classes("text-4xl font-bold mb-2")
                ui.label("Upload • Process • Transform • Download").classes("text-lg opacity-90")
        
        # Stats Dashboard
        stats_card = ui.card().classes("w-full mb-6 hidden mx-auto").style("background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);")
        with stats_card:
            with ui.card_section().classes("text-white p-4"):
                ui.label("📊 Data Overview").classes("text-xl font-semibold mb-4")
                with ui.row().classes("w-full justify-around"):
                    with ui.column().classes("text-center"):
                        rows_label = ui.label("0").classes("text-3xl font-bold")
                        ui.label("Rows").classes("text-sm opacity-80")
                    with ui.column().classes("text-center"):
                        cols_label = ui.label("0").classes("text-3xl font-bold") 
                        ui.label("Columns").classes("text-sm opacity-80")
                    with ui.column().classes("text-center"):
                        size_label = ui.label("0 KB").classes("text-3xl font-bold")
                        ui.label("File Size").classes("text-sm opacity-80")
                    with ui.column().classes("text-center"):
                        time_label = ui.label("--:--").classes("text-3xl font-bold")
                        ui.label("Upload Time").classes("text-sm opacity-80")

        # Control Panel
        with ui.card().classes("w-full mb-6 mx-auto"):
            with ui.card_section().classes("p-4 mx-auto"):
                ui.label("🔧 Control Panel").classes("text-xl font-semibold mb-4")
                with ui.row().classes("w-full gap-6"):
                    # Upload Section
                    with ui.column().classes("flex-1 min-w-[400px]"):
                        ui.label("📁 Upload File").classes("font-medium mb-2")
                        upload_btn = ui.upload(
                            on_upload=lambda e: handle_enhanced_upload(
                                e, df_holder, stats_card, rows_label, cols_label, 
                                size_label, time_label, preview_section, preview_table
                            )
                        ).props("accept=.xlsx,.xls") \
                         .classes("w-full bg-blue-50 border-2 border-dashed border-blue-300 rounded-lg p-4 hover:bg-blue-100 transition-colors")
                        
                    # Action Buttons
                    with ui.column().classes("flex-1 min-w-[400px]"):
                        ui.label("⚡ Actions").classes("font-medium mb-2 mx-auto")
                        with ui.row().classes("gap-2"):
                            run_btn = ui.button("▶️ Execute Code", 
                                on_click=lambda: execute_with_feedback(
                                    df_holder, code_input, result_holder, 
                                    result_section, result_table, progress_bar
                                )
                            ).classes("bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors shadow-md")
                            
                            download_btn = ui.button("⬇️ Download", 
                                on_click=lambda: download_with_notification(result_holder)
                            ).classes("bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors shadow-md")

        # Code Editor Section
        with ui.card().classes("w-full mb-6 mx-auto"):
            with ui.card_section().classes("p-4 mx-auto w-full max-w-[900px]"):
                ui.label("🔧 Python Code Editor").classes("text-xl font-semibold mb-4")
                with ui.column().classes("w-full space-y-6 max-w-[1000px]"):
                    with ui.column().classes("flex-1 min-w-[400px] w-full"):
                        code_input = ui.textarea(
                            label="Enter your pandas code here...",
                            placeholder="""# Example code:\n    df['new_column'] = df['existing_column'] * 2\n    df = df.dropna()\n    df = df.sort_values(['column_name'])\n    print(f\"Processed {len(df)} rows\")"""
                        ).classes("w-full h-[600px] font-mono bg-gray-50 border rounded-lg p-4")
        
                    with ui.column().classes("flex-1 min-w-[400px] w-full"):
                        ui.label("📟 Execution Log").classes("font-medium mb-2")
                        log_output = ui.textarea(
                            placeholder="Execution logs will appear here..."
                        ).props("readonly") \
                         .classes("w-full h-[600px] font-mono text-green-400 bg-gray-900 border rounded-lg")

        # Progress Bar
        progress_bar = ui.linear_progress(value=0).classes("w-full mb-4 hidden")

        # Data Preview and Results sections
        preview_section = ui.card().classes("w-full mb-6 hidden")
        with preview_section:
            with ui.card_section().classes("p-4"):
                ui.label("📟 Data Preview").classes("text-xl font-semibold mb-4")
                preview_table = ui.aggrid({
                    "columnDefs": [],
                    "rowData": [],
                    "pagination": True,
                    "paginationPageSize": 15,
                    "defaultColDef": {
                        "sortable": True, 
                        "filter": True, 
                        "resizable": True,
                        "cellStyle": {"fontSize": "12px"}
                    },
                    "theme": "alpine"
                }).classes("w-full h-[500px] rounded-lg shadow-inner")

        # Results Section
        result_section = ui.card().classes("w-full mb-6 hidden")
        with result_section:
            with ui.card_section():
                ui.label("✨ Processing Results").classes("text-xl font-semibold mb-4")
                with ui.row().classes("w-full justify-between items-center mb-4"):
                    result_info = ui.label("").classes("text-sm text-gray-600")
                    execution_time_label = ui.label("").classes("text-sm font-mono bg-gray-100 px-2 py-1 rounded")
                
                result_table = ui.aggrid({
                    "columnDefs": [],
                    "rowData": [],
                    "pagination": True,
                    "paginationPageSize": 15,
                    "defaultColDef": {
                        "sortable": True, 
                        "filter": True, 
                        "resizable": True,
                        "cellStyle": {"fontSize": "12px"}
                    },
                    "theme": "alpine"
                }).classes("w-full h-[400px] rounded-lg shadow-inner")

def handle_enhanced_upload(e, df_holder, stats_card, rows_label, cols_label, size_label, time_label, preview_section, preview_table):
    try:
        # Create uploads directory
        os.makedirs("uploads", exist_ok=True)
        path = f"uploads/{e.name}"
        
        # Save file
        with open(path, "wb") as f:
            f.write(e.content.read())
        
        # Read Excel file
        df = pd.read_excel(path)
        
        # Store file info
        file_size = os.path.getsize(path)
        upload_time = datetime.now().strftime("%H:%M")
        
        df_holder["df"] = df
        df_holder["file_info"] = {
            "name": e.name,
            "size": file_size,
            "upload_time": upload_time
        }
        
        # Update stats
        rows_label.text = f"{len(df):,}"
        cols_label.text = str(len(df.columns))
        size_label.text = f"{file_size / 1024:.1f} KB"
        time_label.text = upload_time
        
        # Show stats card
        stats_card.classes(remove="hidden")
        
        # Update preview
        update_table_preview(df, preview_table)
        preview_section.classes(remove="hidden")
        
        # Success notification
        ui.notify(
            f"✅ Successfully uploaded {e.name} ({len(df):,} rows × {len(df.columns)} columns)",
            type="positive",
            timeout=3000
        )
        
    except Exception as ex:
        ui.notify(f"❌ Upload failed: {str(ex)}", type="negative", timeout=5000)

def execute_with_feedback(df_holder, code_input, result_holder, result_section, result_table, progress_bar):
    """Execute code with enhanced feedback and progress indication"""
    
    df = df_holder.get("df")
    if df is None:
        ui.notify("⚠️ Please upload a file first!", type="warning")
        return
    
    if not code_input.value.strip():
        ui.notify("⚠️ Please enter some Python code!", type="warning")
        return
    
    # Start progress animation
    progress_bar.classes(remove="hidden")
    progress_bar.value = 0.1
    
    def run_in_thread():
        try:
            start_time = datetime.now()
            
            # Capture stdout
            buffer_out = io_mod.StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = buffer_out
            
            # Progress update
            progress_bar.value = 0.3
            
            # Create execution namespace
            namespace = {"df": df.copy(), "pd": pd, "np": None}
            
            # Try to import numpy if available
            try:
                import numpy as np
                namespace["np"] = np
            except ImportError:
                pass
            
            # Execute code
            exec(code_input.value, namespace)
            progress_bar.value = 0.7
            
            # Get results
            result_df = namespace["df"]
            sys.stdout = sys_stdout_original
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            result_holder["execution_time"] = execution_time
            
            # Update log output (assuming it exists in the global scope)
            # log_output.value = buffer_out.getvalue()
            
            # Progress update
            progress_bar.value = 0.9
            
            # Update result table
            update_table_preview(result_df, result_table)
            
            # Store results for download
            buffer = BytesIO()
            result_df.to_excel(buffer, index=False)
            buffer.seek(0)
            result_holder["buffer"] = buffer
            result_holder["result_df"] = result_df
            
            # Show results section
            result_section.classes(remove="hidden")
            progress_bar.value = 1.0
            
            # Hide progress bar after completion
            ui.timer(1.0, lambda: progress_bar.classes(add="hidden"), once=True)
            
            # Success notification
            ui.notify(
                f"✅ Code executed successfully in {execution_time:.2f}s! Result: {len(result_df):,} rows",
                type="positive",
                timeout=3000
            )
            
        except Exception as ex:
            sys.stdout = sys_stdout_original
            progress_bar.classes(add="hidden")
            ui.notify(f"❌ Execution error: {str(ex)}", type="negative", timeout=5000)
    
    # Run in separate thread
    threading.Thread(target=run_in_thread).start()

def update_table_preview(df, table_component):
    """Update AG Grid table with dataframe data"""
    # Handle datetime columns
    preview_data = df.head(100).copy()
    for col in preview_data.select_dtypes(include=["datetime64[ns]"]).columns:
        preview_data[col] = preview_data[col].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Create column definitions
    column_defs = []
    for col in preview_data.columns:
        col_def = {
            "field": str(col),
            "headerName": str(col),
            "flex": 1,
            "minWidth": 100
        }
        # Add type-specific formatting
        if preview_data[col].dtype in ['int64', 'float64']:
            col_def["type"] = "numericColumn"
            col_def["cellStyle"] = {"textAlign": "right"}
        
        column_defs.append(col_def)
    
    # Update table
    table_component.options["columnDefs"] = column_defs
    table_component.options["rowData"] = preview_data.to_dict("records")
    table_component.update()

def download_with_notification(result_holder):
    """Enhanced download with better feedback"""
    buffer = result_holder.get("buffer")
    result_df = result_holder.get("result_df")
    
    if buffer and result_df is not None:
        try:
            os.makedirs("downloads", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"processed_data_{timestamp}.xlsx"
            path = f"downloads/{filename}"
            
            with open(path, "wb") as f:
                f.write(buffer.getvalue())
            
            # Trigger download
            ui.download(src=path)
            
            # Success notification with file info
            ui.notify(
                f"📥 Downloaded {filename} ({len(result_df):,} rows × {len(result_df.columns)} columns)",
                type="positive",
                timeout=3000
            )
            
        except Exception as ex:
            ui.notify(f"❌ Download failed: {str(ex)}", type="negative")
    else:
        ui.notify("⚠️ No processed data available for download!", type="warning")