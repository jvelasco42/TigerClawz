from flask_login import login_required
from forms import SearchForm
from models import User

@app.route('/')
def index():
  if current_user.is_authenticated:
    return redirect(url_for('profile'))
  return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  # some code to display user profile page

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))  # or what you want
    return render_template('search.html', form=form)
    
@app.route('/search_results/<query>')
@login_required
def search_results(query):
  results = User.query.whoosh_search(query).all()
  return render_template('search_results.html', query=query, results=results)