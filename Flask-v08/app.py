from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv
import os

app = Flask(__name__)

# File and upload configurations
DATA_FILE = 'posts.csv'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to load posts from the CSV file
def load_posts():
    posts = []
    try:
        with open(DATA_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                posts.append(row)
    except FileNotFoundError:
        pass
    return sorted(posts, key=lambda x: x['timestamp'], reverse=True)

# Helper function to save posts to the CSV file
def save_posts(posts):
    with open(DATA_FILE, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'title', 'content', 'password', 'file_path', 'timestamp'])
        writer.writeheader()
        writer.writerows(posts)

# Helper function to save a new post to the CSV file
def save_post(post):
    posts = load_posts()
    posts.append(post)
    save_posts(posts)

@app.route('/')
def index():
    posts = load_posts()
    page = int(request.args.get('page', 1))
    per_page = 40
    start = (page - 1) * per_page
    end = start + per_page
    paginated_posts = posts[start:end]
    total_pages = (len(posts) + per_page - 1) // per_page
    return render_template('list.html', posts=paginated_posts, page=page, total_pages=total_pages)

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def view_item(item_id):
    posts = load_posts()
    if 0 <= item_id < len(posts):
        post = posts[item_id]
        if request.method == 'POST':
            password = request.form['password']
            if password == post['password']:
                if post['file_path'] and os.path.exists(post['file_path']):
                    os.remove(post['file_path'])
                posts.pop(item_id)
                save_posts(posts)
                return redirect(url_for('index'))
            else:
                return render_template('item.html', post=post, error="Incorrect password")
        return render_template('item.html', post=post)
    return redirect(url_for('index'))

@app.route('/write', methods=['GET', 'POST'])
def write_item():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        password = request.form['password']
        file = request.files['file']
        file_path = ''

        if username and title and content and password:
            if file and file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

            post = {
                'username': username,
                'title': title,
                'content': content,
                'password': password,
                'file_path': file_path,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            save_post(post)
        return redirect(url_for('index'))
    return render_template('write.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    posts = load_posts()
    filtered_posts = [
        post for post in posts 
        if query in post['username'].lower() or query in post['title'].lower() or query in post['content'].lower()
    ]
    return render_template('list.html', posts=filtered_posts, page=1, total_pages=1, query=query)

if __name__ == '__main__':
    app.run(debug=True)
