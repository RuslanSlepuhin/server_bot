from django.http import QueryDict


class GetRequestParams:
    @staticmethod
    def get_request_params(query_params: QueryDict) -> dict:

        query_string = next(iter(query_params.keys()))

        params_list = query_string.split("&")
        parsed_params = {}

        for param in params_list:
            key, value = param.split("=", 1)
            parsed_params[key] = value

        return parsed_params
