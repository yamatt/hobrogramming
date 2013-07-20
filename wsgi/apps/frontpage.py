from flask import Blueprint, abort, g, session, jsonify, request, redirect, url_for, flash, current_app, render_template

frontpage = Blueprint('frontpage', __name__)

@frontpage.route("/", methods=["GET"])
def home():
    return render_template("frontpage.html")
