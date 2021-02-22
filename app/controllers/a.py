from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models import db, User, Post, Comment, Message, Follow
import os


main = Blueprint('main', __name__, url_prefix='/')

@main.route('/test2')
def test2():
    return render_template('pages/test2.html')