from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/')
def main():  # put application's code here
    return render_template("html/index.html")


if __name__ == '__main__':
    app.run()
