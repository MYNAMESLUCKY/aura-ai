import subprocess
import webbrowser

def open_browser(browser_path: str, url: str):
    try:
        subprocess.Popen([browser_path, url])
        return True
    except Exception as e:
        print("⚠️ Failed to open browser:", e)
        return False
