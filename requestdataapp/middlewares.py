from time import time
from typing import Callable

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden



class ThrottlingMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        '''
        requests -
            Ключ: IP - адрес пользователя
            Значение: время последнего запроса(в секундах)
        '''
        self.requests = {}

        self.time_limit = 1


    def __call__(self, request: HttpRequest) -> HttpResponse:
        ip_address = self.get_client_ip(request)

        current_time = time()

        if ip_address in self.requests:
            last_request_time = self.requests[ip_address]
            if current_time - last_request_time < self.time_limit:
                return HttpResponseForbidden('Превышен лимит запросов. Пожалуйста, подождите')

        self.requests[ip_address] = current_time
        self.clean_old_request(current_time)

        return self.get_response(request)

    def get_client_ip(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    def clean_old_request(self, current_time: float):
        to_delete = []
        for ip, last_time in self.requests.items():
            if current_time - last_time > 60:
                to_delete.append(ip)

        for ip in to_delete:
            del self.requests[ip]

# def set_useragent_request_middleware(get_response: Callable) -> Callable:
#
#     print('initial call')
#
#     def middleware(request: HttpRequest) -> HttpResponse:
#
#         print('before get response')
#         request.user_agent = request.META.get('HTTP_USER_AGENT')
#         response = get_response(request)
#         print('after get response')
#         return response
#
#     return middleware
#
# class CountRequestMiddleware:
#     def __init__(self, get_response: Callable) -> Callable:
#         self.get_response = get_response
#         self.requests_count = 0
#         self.responses_count = 0
#         self.exceptions_count = 0
#
#     def __call__(self, request: HttpRequest) -> HttpResponse:
#         self.requests_count += 1
#         print('request count', self.requests_count)
#         response = self.get_response(request)
#         self.responses_count += 1
#         print('response count', self.responses_count)
#         return response
#
#     def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse:
#         self.exceptions_count += 1
#         print('exception count', self.exceptions_count)