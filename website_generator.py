## File: website_generator.py

import os

def generate_website(storage, template_path, output_path, title):
    """
    Generate a static HTML page from a template and movie data.

    :param storage: IStorage instance to fetch movies
    :param template_path: Path to index_template.html
    :param output_path: Path where index.html will be written
    :param title: Title to insert in the template
    """
    # Load template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Fetch movie data
    movies = storage.list_movies()

    # Build movie grid items
    grid_items = []
    for name, info in movies.items():
        poster = info.get('poster', '')
        year = info.get('year', '')
        rating = info.get('rating', '')
        item_html = (
            f"<li class=\"movie-item\">"
            f"<div class=\"poster\"><img src=\"{poster}\" alt=\"{name} poster\"/></div>"
            f"<div class=\"details\">"
            f"<h2>{name}</h2>"
            f"<p>Year: {year}</p>"
            f"<p>Rating: {rating}</p>"
            f"</div>"
            f"</li>"
        )
        grid_items.append(item_html)

    grid_html = "\n".join(grid_items)

    # Replace placeholders
    html_output = template.replace('__TEMPLATE_TITLE__', title)
    html_output = html_output.replace('__TEMPLATE_MOVIE_GRID__', grid_html)

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Write final HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
