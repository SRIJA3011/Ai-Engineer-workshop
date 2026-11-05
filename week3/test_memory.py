import requests
BASE = "http://localhost:8000"

def test_followup():
    r1 = requests.post(f"{BASE}/chat", json={"message": "My name is Ravi."}).json()
    sid = r1["session_id"]
    r2 = requests.post(f"{BASE}/chat", json={"session_id": sid, "message": "What is my name?"}).json()
    assert "Ravi" in r2["reply"]
    print(" Follow-up memory works")

def test_isolation():
    a = requests.post(f"{BASE}/chat", json={"message": "I like cricket."}).json()["session_id"]
    b = requests.post(f"{BASE}/chat", json={"message": "What do I like?"}).json()["session_id"]
    assert a != b
    print(" Sessions isolated")

if __name__ == "__main__":
    test_followup()
    test_isolation()