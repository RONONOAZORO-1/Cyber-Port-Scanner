import streamlit as st
import socket
import threading
from datetime import datetime

# App setup
st.set_page_config(page_title="Cyber Port Scanner", layout="centered")
st.title("🔐 Cyber Port Scanner")

# Input fields
target = st.text_input("Enter Target IP or Domain:", "example.com")
start_port = st.number_input("Start Port", min_value=1, max_value=65535, value=1)
end_port = st.number_input("End Port", min_value=1, max_value=65535, value=1024)

# Shared list for open ports
open_ports = []

# Lock for thread-safe access to shared list
lock = threading.Lock()

# Function to scan a single port
def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)  # smaller timeout = faster
        result = s.connect_ex((ip, port))
        s.close()
        if result == 0:
            with lock:
                open_ports.append(port)
    except:
        pass

# Scan trigger
if st.button("Scan Ports"):
    if start_port > end_port:
        st.error("Start Port cannot be greater than End Port.")
    else:
        st.write(f"Scanning {target} from port {start_port} to {end_port}...")
        start_time = datetime.now()

        # Resolve IP
        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror:
            st.error("Hostname could not be resolved.")
            st.stop()

        # Launch threads
        threads = []
        for port in range(start_port, end_port + 1):
            t = threading.Thread(target=scan_port, args=(ip, port))
            threads.append(t)
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Display results
        duration = datetime.now() - start_time

        if open_ports:
            open_ports.sort()
            st.success(f"✅ Open Ports Found: {open_ports}")
        else:
            st.warning("No open ports found in the specified range.")

        st.info(f"Scan completed in {duration}")
