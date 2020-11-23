from flask import render_template
from .core import core_bp


@core_bp.route('/')
def home():
    """Shows indexing homepage."""
    title = 'PsychoMusic'
    return render_template('index.html', title=title)


@core_bp.route('/about')
def about():
    """Shows indexing page with info about us."""
    title = 'About Us'
    return render_template('index.html', title=title)
