from flask import Flask, render_template
import socket
import os
from colorama import Fore, Style
import qrcode
import qrcode.console_scripts  # for terminal rendering

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def home():
    seminar_data = {
        "speakers": [
            {"name": "Prof. A. Rahman", "image": "speaker1.jpg", "bio": "Dean, School of AI, IUST"},
            {"name": "Dr. S. Kaur", "image": "speaker2.jpg", "bio": "AI Researcher, XYZ Institute"},
            {"name": "Dr. R. Sharma", "image": "speaker3.jpg", "bio": "ML Specialist, ABC Labs"}
        ],
        "schedule": [
            {"day": "Day 1", "time": "09:00 - 10:00", "event": "Opening Ceremony", "speaker": "Prof. A. Rahman"},
            {"day": "Day 1", "time": "10:15 - 12:00", "event": "Keynote: AI in Healthcare", "speaker": "Dr. S. Kaur"},
            {"day": "Day 2", "time": "09:00 - 11:00", "event": "Workshop: Deep Learning", "speaker": "Dr. R. Sharma"},
            {"day": "Day 3", "time": "11:00 - 13:00", "event": "Panel Discussion: Future of AI", "speaker": "Multiple Experts"}
        ]
    }
    return render_template("index.html", seminar_data=seminar_data)


def get_local_ip():
    """Get the local network IP of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def get_local_ip():
    """Get the LAN IP for mobile access."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def print_qr(url):
    """Print QR code in terminal."""
    qr = qrcode.QRCode(border=2)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)  # Works nicely in most terminals

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    is_local = "PORT" not in os.environ

    # Detect Render domain or fallback
    render_domain = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if not render_domain:
        app_name = os.environ.get("RENDER_APP_NAME", "seminariust")
        render_domain = f"{app_name}.onrender.com"

    print("\n" + "=" * 60)
    print(Fore.CYAN + "🚀 Flask Seminar Server Status".center(60) + Style.RESET_ALL)
    print("=" * 60 + "\n")

    # 🖥️ Local info
    local_ip = get_local_ip()
    local_url = f"http://127.0.0.1:{port}"
    network_url = f"http://{local_ip}:{port}"

    print(Fore.GREEN + "🖥️  Running Locally:" + Style.RESET_ALL)
    print(f"   • Local:   {Fore.YELLOW}{local_url}{Style.RESET_ALL}")
    print(f"   • Network: {Fore.YELLOW}{network_url}{Style.RESET_ALL}  (mobile access)")
    print(Fore.BLUE + "\n   • Scan this QR to open locally:" + Style.RESET_ALL)
    print_qr(network_url)

    # ☁️ Cloud / Render info
    render_url = f"https://{render_domain}"
    print(Fore.MAGENTA + "\n☁️  Render Cloud URL:" + Style.RESET_ALL)
    print(f"   → {Fore.CYAN}{render_url}{Style.RESET_ALL}")
    print(Fore.BLUE + "\n   • Scan this QR for cloud access:" + Style.RESET_ALL)
    print_qr(render_url)

    print("\n" + "=" * 60 + "\n")

    app.run(host="0.0.0.0", port=port, debug=is_local)