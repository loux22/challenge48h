from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db
import os


image = Blueprint('image', __name__, url_prefix='/')

@image.route('/test')
def test1():
    alltest = []
    return render_template('pages/test.html', alltest=alltest)



