from jinja2 import Template, Environment, PackageLoader
import json
import os
from markdown import markdown

CONFIG_PATH = 'config.json'
ARTICLES_PATH = 'articles'
SITE_PATH = 'docs'

def load_json(json_name):
    with open(json_name) as json_file:
        return json.load(json_file)

def get_config(file_name):
    config = load_json(file_name)
    return config

def build_structure_of_site(config):
    site_structure = {}
    articles_types = {}
    for element in config['topics']:
        topic = element['title']
        site_structure[topic ] = []      
        articles_types[topic] = element['slug']
    return site_structure, articles_types


def build_content_table(config, site_structure, articles_types):
    articles = config['articles']
    for topic in site_structure:    
        for article in articles:
                    if article['topic'] == articles_types[topic]:
                        directory, file_name = os.path.split(article['source'])
                        name, md_ext = os.path.splitext(file_name)
                        html_ext = '.html'
                        file_name = file_name.replace(md_ext, html_ext)
                        directory = os.path.join(ARTICLES_PATH, directory)
                        href = os.path.join( directory, file_name)
                        article_source = os.path.join(ARTICLES_PATH,article['source'])
                        site_structure[topic].append({
                            'source' : article_source,
                            'href'   : href,
                            'title'  : article['title'],
                            })
    return site_structure

def create_index_page(structure, template):
    if template is None:
        return
    if not os.path.exists(SITE_PATH):
        os.makedirs(SITE_PATH)
    with open(os.path.join(SITE_PATH,'index.html'), 'w+') as index_file:
        index_file.write(template.render(title='Энциклопедия', structure = structure))


def create_articles_page(structure, template):
    for topic in structure:
        for article in structure[topic]:
            html_article = convert_md_to_html(article['source'])
            article_path_on_site = os.path.join(SITE_PATH,article['href'])
            directory, file_name = os.path.split(article_path_on_site)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(article_path_on_site, 'w+') as html_file:
                html_file.write(template.render(title=article['title'], content=html_article))


def convert_md_to_html(md_path):
    with open(md_path) as md_file:
        return markdown(md_file.read())




if __name__ == '__main__':
    config = get_config(CONFIG_PATH)
    env = Environment(loader=PackageLoader('site_generator', 'templates'))
    index_template = env.get_template('index.html')
    article_template = env.get_template('docs_page.html')

    site_structure, articles_types = build_structure_of_site(config)
    site_structure = build_content_table(config, site_structure, articles_types)
    create_index_page(site_structure, index_template)
    create_articles_page(site_structure, article_template)
