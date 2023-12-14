import json
import urllib.parse

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200


def test_doctor_login(app, client):
    res = client.get('/doctor_login')
    assert res.status_code == 200
    assert b"<h1>Doctor Login</h1>" in res.data

def test_patient_login(app, client):
    res = client.get('/patient_login')
    assert res.status_code == 200
    assert b"<h1>Patient Login</h1>" in res.data

def test_patient_resgister(app, client):
    res = client.get('/patient_register')
    assert res.status_code == 200
    print(res.data)
    assert b"<h1>Patient Registration</h1>" in res.data

def test_doctor_dashboard(app, client):
    res = client.get('/patient-doctor-dashboard/1')
    assert res.status_code == 200
    print(res.data)
    assert b"<title>Weekly Schedule</title>" in res.data

