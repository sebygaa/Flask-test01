from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Utility function to handle form processing for each page
def handle_form(page_id, page_title):
    # On POST, calculate the sum of six inputs; on GET, prepare empty values.
    if request.method == 'POST':
        # Retrieve values from the submitted form
        values = [request.form.get(f'input{i}', '') for i in range(1, 7)]
        total = 0.0
        for v in values:
            try:
                total += float(v)
            except:
                # treat non-numeric or blank as 0
                pass
        result = total
    else:
        values = [''] * 6
        result = None
    # Render the main template with provided values and result
    return render_template('index.html', page_title=page_title, 
                           active=page_id, values=values, result=result)

# Define routes for each section
@app.route('/')
def home():
    # Redirect to first section as default homepage
    return redirect(url_for('catalyst'))

@app.route('/catalyst', methods=['GET', 'POST'])
def catalyst():
    return handle_form('catalyst', 'Catalyst param. est.')

@app.route('/membrane', methods=['GET', 'POST'])
def membrane():
    return handle_form('membrane', 'Membrane param. est.')

@app.route('/reactor', methods=['GET', 'POST'])
def reactor():
    return handle_form('reactor', 'Reactor Performance')

@app.route('/module', methods=['GET', 'POST'])
def module():
    return handle_form('module', 'Membrane Module Performance')

@app.route('/supplychain', methods=['GET', 'POST'])
def supplychain():
    return handle_form('supplychain', 'Green H2 Supply Chain')

@app.route('/optimization', methods=['GET', 'POST'])
def optimization():
    return handle_form('optimization', 'Process Optimization')

if __name__ == '__main__':
    app.run(debug=True)
