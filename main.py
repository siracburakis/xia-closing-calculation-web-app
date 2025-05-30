from nicegui import ui, app
from pathlib import Path
import pages.home
import pages.dashboard
import pages.calculation
import pages.manual_edit
import pages.test_page
import time

static_path = Path(__file__).parent / "static"
app.add_static_files("/static", static_path)

# Dark mode script
ui.add_head_html("""
<script>
    function syncDarkMode() {
        const isDark = localStorage.getItem("darkMode") === "true";
        if (isDark) {
            document.documentElement.classList.add("dark");
            window._nicegui.dark_mode = true;
        } else {
            document.documentElement.classList.remove("dark");
            window._nicegui.dark_mode = false;
        }
    }
    document.addEventListener("DOMContentLoaded", syncDarkMode);
    window._nicegui.on("dark_mode", function(isDark) {
        localStorage.setItem("darkMode", isDark);
        if (isDark) {
            document.documentElement.classList.add("dark");
        } else {
            document.documentElement.classList.remove("dark");
        }
    });
</script>
""")

ui.run(
    title="Xiaomi Calculation Web App",
    reload=True
)