from flask import Flask, render_template, request, redirect, url_for

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
        content = request.form['content']
        if username and content:
            posts.append({'username': username, 'content': content})
        return redirect(url_for('index'))
    return render_template('write.html')

if __name__ == '__main__':
    app.run(debug=True)
