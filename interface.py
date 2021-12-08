import sys
import json
from db import db
from flask import Flask, render_template, request, Response, flash, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy

core = Blueprint(__name__, __name__, template_folder=".")

def compute_data(df):
    df.columns = [col.replace(' ', '_').lower() for col in df.columns]
    df.columns = [col.replace('-', '_').lower() for col in df.columns]
    all_regions = df['region'].unique()
    return all_regions

@core.route('/evaluate', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return compute_data(db.session)

    return render_template('main.html')
