
def correct_url(url:str):
    # очищаем лишние пробклы
    url.strip()
    # если на конце нет '/', то добавляем
    if not url.endswith('/'):
        url += '/'
    return url


def pars_input_data(input_data: str):
    """Парсинг и приведение к словарю  строковых данных входящего
    GET/POST запроса"""
    param_request = {}
    if input_data:
        # разделяем параметры
        list_param = input_data.split('&')
        for i in list_param:
            # преобразуем в словарь
            key, value = i.split('=')
            param_request[key] = value
    return param_request


def get_post_input_data(input_data) -> bytes:
    """Получение данных от пост-запроса"""
    param_request = {}
    if input_data:
        # узнаём длину тела контента
        content_len = int(input_data.get('CONTENT_LENGTH'))
        if content_len:
            # считываем данные
            param_request = input_data['wsgi.input'].read(content_len)
        else:
            b''
    return param_request


def pars_post_input_data(input_data: bytes) -> dict:
    """Декодирование и парсинг данных пост-запроса"""
    param_request = {}
    if input_data:
        input_data_str = input_data.decode(encoding='utf-8')
        param_request = pars_input_data(input_data_str)
    return param_request


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

        # определение типа запроса(GET/POST)
        req_method = environ['REQUEST_METHOD']
        print(f'================\nREQUEST_METHOD: {req_method}\n'
              f'================\n')

        # если GET
        if req_method == 'GET':
            # получаем строку с параметрами
            query_string = environ['QUERY_STRING']
            print(f'================\nQUERY_STRING: {query_string}\n'
                  f'================\n')
            request_param = pars_input_data(query_string)
            print(f'================\nrequest_param: {request_param}\n'
                  f'================\n')
        elif req_method == 'POST':
            # получение данных
            req_raw_data = get_post_input_data(environ)
            print(f'================\nreq_raw_data: {req_raw_data}\n'
                  f'================\n')
            # парсинг данных, выведение в словарь
            request_param = pars_post_input_data(req_raw_data)
            print(f'================\nPOST request_param: {request_param}\n'
                  f'================\n')

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
