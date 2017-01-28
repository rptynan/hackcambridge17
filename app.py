#!/usr/bin/env python3
from flask import Flask, render_template
from api_keys import GOOGLE_KEY
app = Flask(__name__)


@app.route('/')
def index():
    trumpLocation = {'lat': 38.9, 'lng': -77.0}
    return render_template(
        'layout.html',
        GOOGLE_KEY=GOOGLE_KEY,
        # body="""<button onclick="setOurLocation({location})">
        #     Click
        # </button>""".format(location=trumpLocation)
    )


if __name__ == "__main__":
    app.run(debug=True)
    app.run()
