import uuid

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/black', methods=['POST'])
def my_form_post():
    text = request.form['text']
    
    print(request.form)
    if 'black' in request.form:
        import black
        processed_text = black.format_str(text, mode=black.FileMode())
        print(processed_text)
        return render_template('my-form.html', my_text=text, black_text=processed_text)

    elif 'yapf' in request.form:
        from yapf.yapflib.yapf_api import FormatCode
        processed_text = FormatCode(text, style_config='google')[0]
        print(processed_text)
        return render_template('my-form.html', my_text=text, yapf_text=processed_text)



@app.route('/yapf', methods=['POST'])
def yapf_post():
    
    text = request.form['text']
    from yapf.yapflib.yapf_api import FormatCode
    processed_text = FormatCode(text)
    print(processed_text)
    # processed_text = text.upper()
    return render_template('my-form.html', my_text=text, yapf_text=processed_text)

if __name__ == '__main__':
    app.run()