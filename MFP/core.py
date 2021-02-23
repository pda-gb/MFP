
def correct_url(url:str):
    # очищаем лишние пробклы
    url.strip()
    # если на конце нет '/', то добавляем
    if not url.endswith('/'):
        url += '/'
    return url

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
        # проверка на соответствие и корректировка по необходимости
        path = correct_url(path)
        # для каждой определяем PC
        if path in self.urls_view:
            page_controller = self.urls_view[path]
        else:
            # если страницы нет, то отдаём код 404 и возвращаем ответ в байтах
            start_response('404', [('Content-Type', 'text/html')])
            return [b'<h1>Page not found ! ! !</h1>']
        request = {}
        # применяем FC
        for fc in self.fronts:
            fc(request)
        # вызываем PC, получаем код и текст ответа
        code, answer = page_controller(request)
        # передаём код и заголовки
        start_response(code, [('Content-Type', 'text/html')])
        # возвращаем сам ответ в виде списка из bite
        return [answer.encode('utf-8')]
