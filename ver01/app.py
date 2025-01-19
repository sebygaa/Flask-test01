from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data storage (in-memory)
posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    username = request.form['username']
    content = request.form['content']
    if username and content:
        posts.append({'username': username, 'content': content})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)