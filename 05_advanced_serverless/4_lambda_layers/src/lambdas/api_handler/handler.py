from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
from lambdas.layers.weather_forecast.forecast import get_weather_forecast

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info('Fetching weather forecast')
        weather_forecast = get_weather_forecast()

        return weather_forecast
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
