# PC. отдельные контроллеры на каждую страницу
def index_view(request):
    return '200', [b'MAIN']


def products_view(request):
    return '200', [b'products view']


def about_view(request):
    return '200', [b'about']


def contacts_view(request):
    return '200', [b'contact']


def page_404_view(request):
    return '404', [b'page_404']


# def _view(request):
#     return '00',[b'']

# FC. общие контроллеры на все страницы
def fc_secret_key(request):
    # добавляем данные в запрос
    request['secret_key'] = '123456'


def fc_login(request):
    request['login'] = 'user'


def fc_password(request):
    request['password'] = 'password'


def fc_is_admin(request):
    request['is_admin'] = False


fronts_controllers = [fc_secret_key, fc_login, fc_password, fc_is_admin]

# Routes. соответствие адресу свой контроллер
routes = {
    '/': index_view,
    '/products/': products_view,
    '/about/': about_view,
    '/contacts/': contacts_view
}


class Application:
    """
    Класс создания объекта вызываемого WSGI-сервером.
    urls_view - словарь {'адрес': контроллер,}
    fronts_controllers - список фронт-контроллеров
    """

    def __init__(self, urls_view, fronts):
        self.urls_view = urls_view
        self.fronts = fronts

    def __call__(self, environ, start_response):
        """
        Вызов бъекта.
        В функцию start_response передаем код ответа и заголовки.
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """
        # определяем запрошенную страницу
        path = environ['PATH_INFO']
        # для каждой определяем PC
        if path in self.urls_view:
            page_controller = self.urls_view[path]
        else:
            page_controller = page_404_view
        request = {}
        # применяем FC
        for fc in self.fronts:
            fc(request)
        # вызываем PC, получаем код и текст ответа
        code, answer = page_controller(request)
        # передаём код и заголовки
        start_response(code, [('Content-Type', 'text/html')])
        # возвращаем сам ответ в виде списка из bite
        return [answer]


application = Application(routes, fronts_controllers)
