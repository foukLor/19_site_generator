from jinja2 import Template, Environment, PackageLoader
import json
import os

CONFIG_PATH = 'config.json'
ARTICLES_PATH = 'articles'
SITE_PATH = 'site'

def load_json(json_name):
    with open(json_names) as json_file:
        return json.read(json_file)

def get_config(file_name):
    config = load_json(config)
    return config

def built_structure_of_site(structure):
    site_structure = []
    for item in structure['articles']:


def create_index_page(structure, template):
    if template is None:
        return
    if not os.path.exist():
        os.makedirs(SITE_PATH)
    with open(os.path.join(SITE_PATH,'index.html', 'w')) as index_file:
        index_file.write(template.render(title='Энциклопедия', structure = structure))


def render_site():
    env = Environment(loader=PackageLoader('site_generator', 'templates'))
    index_template = environment.get_template('index.html')
    pass

if __name__ == '__main__':
    config = load_config(CONFIG_PATH)

