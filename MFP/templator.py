""" Шаблонизатор на основе jinja2 """
from os import path
from jinja2 import Template

# для рендера наследованных шаблонов
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_file, temp_folder='templates/', **kwargs):
    """
    Рендер шаблона с указанными данными.
    :param template_file: файл шаблона
    :param temp_folder: папкав проекте, где находится шаблон
    :param kwargs: данные
    :return: отрендеренный шаблон
    """
    # создаём экземпляр загрузчика шаблонов
    env = Environment()
    # указываем место поиска шаблонов
    env.loader = FileSystemLoader(temp_folder)
    # отдаём загрузчику требуемый шаблон
    tmpl = env.get_template(template_file)

    # открываем и читаем файл
    # with open(path.join(temp_folder, template_file), encoding='utf-8') as f:
    #     template = Template(f.read())

    # рендерим с параметрами
    ready_template = tmpl.render(**kwargs)
    return ready_template
