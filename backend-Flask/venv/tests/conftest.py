import pytest
import sys
sys.path.append("../")
from app import app as flask_app
from flask import Flask
from flask import Flask, render_template, request,jsonify,redirect, url_for,session
from pymongo import MongoClient
import secrets
import os

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the home page" in response.data