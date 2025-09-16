import requests
import time

# Written with GitHub Copilot

PICO_IP = "192.168.1.101"  # Change to Pico's IP

def test_health():
    url = f"http://{PICO_IP}/health"
    r = requests.get(url, timeout=2)
    print("GET /health:", r.status_code, r.json())

def test_sensor():
    url = f"http://{PICO_IP}/sensor"
    r = requests.get(url, timeout=2)
    print("GET /sensor:", r.status_code, r.json())

def test_tone():
    url = f"http://{PICO_IP}/tone"
    data = {"freq": 440, "ms": 300, "duty": 0.5}
    r = requests.post(url, json=data, timeout=2)
    print("POST /tone:", r.status_code, r.json())

def test_melody():
    url = f"http://{PICO_IP}/melody"
    data = {
        "notes": [
            {"freq": 523, "ms": 200},
            {"freq": 659, "ms": 200},
            {"freq": 784, "ms": 400}
        ],
        "gap_ms": 20 
    }
    r = requests.post(url, json=data, timeout=2)
    print("POST /melody:", r.status_code, r.json())

def test_stop():
    url = f"http://{PICO_IP}/stop"
    r = requests.post(url, timeout=2)
    print("POST /stop:", r.status_code, r.text)

if __name__ == "__main__":
    test_health()
    test_sensor()
    test_tone()
    time.sleep(1)
    test_melody()
    time.sleep(1)
    test_stop()