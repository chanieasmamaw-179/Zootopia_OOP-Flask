from flask import Flask, render_template, abort

app = Flask(__name__)

# Blog post data structure
blog_posts = [
    {
        'id': 1,
        'author': 'Asmamaw Yehun',
        'title': 'First Post',
        'content': 'This is my first post.',
        'created_at': '2024-01-01 12:00:00',
        'updated_at': '2024-01-02 14:00:00',
        'tags': ['flask', 'python', 'tutorial'],
        'likes': 10,
        'comments': [
            {'author': 'Jane', 'content': 'Great post!', 'created_at': '2024-01-02 13:00:00'},
            {'author': 'Mike', 'content': 'Very informative, thanks!', 'created_at': '2024-01-02 14:00:00'}
        ]
    },
    {
        'id': 2,
        'author': 'Jane Doe',
        'title': 'Second Post',
        'content': 'This is another post.',
        'created_at': '2024-01-03 10:00:00',
        'updated_at': '2024-01-04 16:00:00',
        'tags': ['web development', 'flask'],
        'likes': 20,
        'comments': [
            {'author': 'John', 'content': 'Thanks for sharing!', 'created_at': '2024-01-04 12:00:00'}
        ]
    }
]

# Route for the home page that displays a list of blog posts
@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)

# Route for displaying an individual post by its ID
@app.route('/post/<int:post_id>')
def post(post_id):
    # Find the post by its ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    # If the post is not found, return a 404 page
    if post is None:
        abort(404)

    return render_template('post.html', post=post)

# Optional: Route for fetching job posts from a file
@app.route('/jobs')
def jobs():
    # You can implement logic to fetch job posts from a file here
    # For example, you could read from a JSON or CSV file.
    # Here is a placeholder for the job posts.
    job_posts = [
        {'id': 1, 'title': 'Software Engineer', 'company': 'Tech Corp', 'location': 'Remote'},
        {'id': 2, 'title': 'Web Developer', 'company': 'Web Solutions', 'location': 'On-site'},
    ]
    return render_template('jobs.html', jobs=job_posts)

if __name__ == '__main__':
    app.run(debug=True)
