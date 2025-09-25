from flask import Flask, render_template
import socket

app = Flask(__name__)

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
    """
    Get the correct local network IP for the machine.
    Works even if multiple adapters exist.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to connect, just used to get the correct interface IP
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip


if __name__ == "__main__":
    local_ip = get_local_ip()
    print("\n🚀 Flask Seminar Server Running:")
    print(f"   Local:   http://127.0.0.1:5000")
    print(f"   Network: http://{local_ip}:5000\n")
    
    # Listen on all interfaces so mobile can access via local IP
    app.run(host="0.0.0.0", port=5000, debug=True)
