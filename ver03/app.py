from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Sample data storage (in-memory)
posts = []

@app.route('/')
def index():
    return render_template('list.html', posts=posts)

@app.route('/item/<int:item_id>')
def view_item(item_id):
    if 0 <= item_id < len(posts):
        return render_template('item.html', post=posts[item_id])
    return redirect(url_for('index'))

@app.route('/write', methods=['GET', 'POST'])
def write_item():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        if username and title and content:
            posts.append({
                'username': username,
                'title': title,
                'content': content,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        return redirect(url_for('index'))
    return render_template('write.html')

if __name__ == '__main__':
    app.run(debug=True)
