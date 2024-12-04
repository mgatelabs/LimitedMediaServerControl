import subprocess
import webbrowser
from collections import deque
from threading import Thread
from tkinter import Tk, Text, Scrollbar, END, VERTICAL, RIGHT, Y, Button
import time

import infi
from infi.systray import SysTrayIcon

from constants import SERVER_ADDRESS
from plyer import notification

# Buffer to store the last 200 lines of output
output_buffer = deque(maxlen=100)
process = None
log_window = None
log_window_active = False
end_process = False

def update_menu():
    """Updates the system tray menu based on the process state."""
    global systray
    is_running = process and process.poll() is None

    if is_running:
        systray.update(icon="logo-play.ico", hover_text='Limited Media Server (Running)')
    else:
        systray.update(icon="logo-stop.ico", hover_text='Limited Media Server (Stopped)')

    # new_menu_options.append(("Show Output", None, show_output))

    # systray.update(menu_options=new_menu_options)
    # systray.update()

def show_notice(title, message):
    notification.notify(
        app_icon='logo.ico',
        title=title,
        message=message,
        app_name="Limited Media Server",
        timeout=5  # duration in seconds,
    )

def open_browser(systray):
    webbrowser.open(SERVER_ADDRESS)


def start_program(systray):
    """Starts the controlled process and monitors its output."""
    global process, end_process
    if process and process.poll() is None:
        print("Process is already running.")
        show_notice('Command skipped', 'Limited Media Server is already running!')
        update_menu()
        return

    end_process = False

    def run_process():
        global process
        while True:
            try:

                print("Starting Server...")
                process = subprocess.Popen(
                    ["limitedmediaserver.exe"],  # Replace with your program and arguments
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True
                )

                # Capture output
                for line in process.stdout:
                    if end_process:
                        break
                    output_buffer.append(line.strip())

                process.wait()

                if process.returncode == 69:
                    show_notice('Command skipped', 'Limited Media Server is restarting!')
                    print("Process exited with code 69. Performing extra work...")
                    # Perform extra work here
                else:
                    show_notice('Server Notice', 'Limited Media Server is shutting down!')
                    print(f"Process exited with code {process.returncode}. Stopping...")
                    break
            except Exception as e:
                print(f"Error: {e}")
                break
        process = None

    show_notice('Server Notice', 'Limited Media Server is starting!')

    thread = Thread(target=run_process, daemon=True)
    thread.start()

    time.sleep(2.5)

    update_menu()


def stop_program(systray):
    """Stops the controlled process."""
    global process, end_process
    end_process = True
    if process and process.poll() is None:
        show_notice('Server Notice', 'Stopping Limited Media Server!')
        print("Stopping Server...")
        process.terminate()
        process.wait()
        subprocess.run(["taskkill", "/IM", "limitedmediaserver.exe", "/F"], shell=True)
        process = None
        print("Process stopped.")
    else:
        show_notice('Command skipped', 'Limited Media Server is not running!')
        print("No process running.")
    update_menu()


def show_output(systray):
    """Shows the last 200 lines of output in a Tk window with a manual refresh button."""
    global root, log_window_active
    if log_window_active:
        show_notice('Command skipped', 'Log viewer is already open!')
        print("Log window is already open.")
        return

    log_window_active = True
    root = Tk()
    root.title("Limited Media Server Log Viewer")
    root.geometry("600x480")

    # Text widget for displaying log
    text_widget = Text(root, wrap='none', state='disabled')
    text_widget.pack(fill='both', expand=True, padx=5, pady=5)

    # Scrollbars
    scroll_y = Scrollbar(root, orient=VERTICAL, command=text_widget.yview)
    scroll_y.pack(side=RIGHT, fill=Y)
    text_widget.configure(yscrollcommand=scroll_y.set)

    def refresh_log():
        """Refresh the log and keep it scrolled to the bottom."""
        if log_window_active:
            text_widget.config(state='normal')
            text_widget.delete(1.0, END)
            for line in output_buffer:
                text_widget.insert(END, line + "\n")
            text_widget.config(state='disabled')
            text_widget.see(END)  # Scroll to the bottom

    def on_close():
        """Handle the window close event."""
        global log_window_active
        log_window_active = False
        root.destroy()

    # Refresh button
    refresh_button = Button(root, text="Refresh", command=refresh_log)
    refresh_button.pack(side='bottom', pady=5)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def quit_action(systray):
    """Quits the application."""
    print("Quitting...")
    stop_program(systray)
    pass


if __name__ == '__main__':
    menu_options = (("View Server", None, open_browser), ("Start", None, start_program), ("Stop", None, stop_program),
                    ("Show Output", None, show_output))

    systray = SysTrayIcon("logo.ico", "Limited Media Server", menu_options, on_quit=quit_action)

    systray.start()

    start_program(systray)
