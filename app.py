from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# Blog post data structure
blog_posts = []
post_id_counter = 1  # Simple counter for unique IDs


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    global post_id_counter
    if request.method == 'POST':
        # Collect form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        tags = request.form.get('tags', '').split(',')

        # Create a new post
        new_post = {
            'id': post_id_counter,
            'author': author,
            'title': title,
            'content': content,
            'created_at': '2024-01-01 12:00:00',  # Placeholder for creation time
            'updated_at': '2024-01-01 12:00:00',  # Placeholder for update time
            'tags': [tag.strip() for tag in tags],  # Strip whitespace from tags
            'likes': 0,
            'comments': []
        }

        # Add the new post to the list
        blog_posts.append(new_post)
        post_id_counter += 1  # Increment the post ID counter

        return redirect(url_for('index'))  # Redirect to the homepage after adding

    return render_template('add.html')


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    # Find the post by its ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    # If the post is not found, return a 404 page
    if post is None:
        abort(404)

    return render_template('post.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global blog_posts
    # Find the post by its ID and remove it from the list
    post_to_delete = next((post for post in blog_posts if post['id'] == post_id), None)

    if post_to_delete:
        blog_posts.remove(post_to_delete)  # Remove the post
        return redirect(url_for('index'))  # Redirect to the homepage after deletion
    else:
        abort(404)  # If the post is not found, return a 404 error


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    # Find the post by its ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if post is None:
        abort(404)  # If the post is not found, return a 404 error

    if request.method == 'POST':
        # Update the post with new data
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        post['tags'] = request.form.get('tags', '').split(',')

        post['tags'] = [tag.strip() for tag in post['tags']]  # Strip whitespace from tags
        post['updated_at'] = '2024-01-01 12:00:00'  # Placeholder for updated time

        return redirect(url_for('index'))  # Redirect to the homepage after updating

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
