# 📁 routes/main.py
from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/menu')
def menu():
    return render_template('menu.html')

@main_bp.route('/reset', methods=['POST'])
def reset_game():
    session.clear()
    return redirect(url_for('main.menu'))
