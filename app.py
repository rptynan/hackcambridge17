#!/usr/bin/env python3
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/buttonjstest')
def buttonjstest():
    return render_template(
        'layout.html',
        body="""<script type=text/javascript>
            $(function() {
                $('a#fetchtext').bind(
                    'click',
                    function() {
                                console.log($SCRIPT_ROOT + 'hii');
                        $.get(
                            $SCRIPT_ROOT + '/buttonjstest_getstring',
                            {},
                            function(data) {
                                console.log(data);
                                $('#result').text(data);
                            }
                        );
                        return false;
                    }
                );
            });
            </script>
            <a href=# id=fetchtext>fetch some text</a>
            <span id=result>?</span>"""
    )


@app.route('/buttonjstest_getstring')
def buttonjstest_getstring():
    return 'fetched this through javascript'


if __name__ == "__main__":
    app.run()
