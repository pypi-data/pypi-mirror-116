from functools import wraps
import json


class HTTPError(Exception):

    def __init__(self, code):
        self.message = f"HTTP error with code: {code}"


class AuthenticationError(Exception):

    def __init__(self):
        self.message = "AuthenticationError"


class SaaSError(Exception):

    def __init__(self, details):
        self.message = f"The operation failed due to:\n{details}"


def http_resp_handler(func):

    @wraps(func)
    def decorator_wrapper(*args, **kwargs):
        self = args[0]

        response = func(*args, **kwargs)
        if response.status_code == 200:
            try:
                jsn_obj = response.json()
                if not jsn_obj["success"] is True:
                    raise SaaSError(jsn_obj["detail"])

                for k in ['ws_id', 'model_id', 'sample_id', 'loadable_id']:
                    if k in jsn_obj:
                        self.ws_params[k] = jsn_obj[k]

                for k in ['input_name', 'input_shape', 'input_as_nchw']:
                    if k in jsn_obj and 'model_id' in jsn_obj:
                        self.model_info[jsn_obj['model_id']] = {
                            'input_name': jsn_obj['input_name'],
                            'input_shape': jsn_obj['input_shape'],
                            'input_as_nchw': jsn_obj['input_as_nchw']
                        }
                        break

                return jsn_obj
            except json.decoder.JSONDecodeError:
                return {'success': True}

        elif response.status_code == 401:
            raise AuthenticationError()

        else:
            raise HTTPError(response.status_code)

        return response

    return decorator_wrapper
