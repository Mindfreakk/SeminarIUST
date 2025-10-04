from flask import Flask, render_template
import socket
import os

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT if available
    is_local = "PORT" not in os.environ     # Detect if running locally
if is_local:
    local_ip = get_local_ip()
    print("\n🚀 Flask Seminar Server Running Locally:")
    print(f"   Local:   http://127.0.0.1:{port}")
    print(f"   Network: http://{local_ip}:{port}  (mobile access)\n")
else:
    print("\n🚀 Flask Seminar Server Running on Render (or cloud):")
    print(f"   URL: https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'your-app.onrender.com')}\n")

# Listen on all interfaces so both local network and Render can access
app.run(host="0.0.0.0", port=port, debug=is_local)
