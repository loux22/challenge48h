from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Test
import os


test = Blueprint('test', __name__, url_prefix='/')

@test.route('/test')
def test1():
    louis = Test(username='louis')
    db.session.add(louis)
    db.session.commit()

    alltest = Test.query.all()
    return render_template('pages/test.html', alltest=alltest)



