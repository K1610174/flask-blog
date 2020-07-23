from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/home')

def home():
    return """
       <h1> Hello Internet!</h1>
       Will I see this?
       """
@app.route('/about')
def about():
    return """
        <h3>This is my about page.</h3>
        Maybe I won't.
        """
