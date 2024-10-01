from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime

app = Flask(__name__)

# Blog post data structure
blog_posts = []
post_id_counter = 1  # Simple counter for unique IDs

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """
    Add a new blog post.

    If the request method is POST, collects form data from the user,
    creates a new post, and adds it to the blog posts list.
    Redirects to the index page after adding the post.

    Returns:
        Rendered template for adding a post or redirects to index.
    """
    global post_id_counter
    if request.method == 'POST':
        # Collect form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        tags = request.form.get('tags', '').split(',')

        # Get current timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a new post
        new_post = {
            'id': post_id_counter,
            'author': author,
            'title': title,
            'content': content,
            'created_at': now,
            'updated_at': now,
            'tags': [tag.strip() for tag in tags],
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
    """
    Render the homepage displaying all blog posts.

    Returns:
        Rendered template for the index page with all blog posts.
    """
    return render_template('index.html', posts=blog_posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    """
    Render a specific blog post by its ID.

    Args:
        post_id (int): The ID of the post to display.

    Returns:
        Rendered template for the specific post or raises a 404 error if not found.
    """
    # Find the post by its ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    # If the post is not found, return a 404 page
    if post is None:
        abort(404)

    return render_template('post.html', post=post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """
    Delete a blog post by its ID.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        Redirects to the homepage after deletion or raises a 404 error if not found.
    """
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
    """
    Update an existing blog post by its ID.

    Args:
        post_id (int): The ID of the post to update.

    If the request method is POST, updates the post with new data
    and redirects to the index page. If the post is not found,
    raises a 404 error.

    Returns:
        Rendered template for updating a post or redirects to index.
    """
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

        # Get current timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post['updated_at'] = now  # Update the timestamp to the current time

        return redirect(url_for('index'))  # Redirect to the homepage after updating

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
