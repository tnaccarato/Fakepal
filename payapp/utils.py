import requests
from decimal import Decimal

from payapp.custom_exceptions import CurrencyConversionError


def convert_currency(currency1, currency2, amount_of_currency1):
    """
    Utility function to convert an amount of currency1 to currency2 using the currency conversion RESTful service
    :param currency1:
    :param currency2:
    :param amount_of_currency1:
    :return:
    """
    # If the currencies are the same, return the amount of currency1
    if currency1 == currency2:
        return amount_of_currency1
    url = (f'https://ec2-52-203-137-55.compute-1.amazonaws.com/webapps2024/conversion/'
           f'{currency1.upper()}/'
           f'{currency2.upper()}/'
           f'{amount_of_currency1}')
    try:
        response = requests.get(url, verify='/home/ubuntu/webapps2024/webapps.crt')
        response.raise_for_status()  # Raises HTTPError for bad responses (400 or 500 level responses)
    except Exception:
        raise CurrencyConversionError('Error in currency conversion, please try again')
    # If the request is unsuccessful, raise an exception
    if response.status_code != 200:
        raise CurrencyConversionError('Error in currency conversion, please try again')

    # If the request is successful, returns the result, which is the amount of currency1 converted to currency2
    converted_amount = Decimal(float(response.content))
    return converted_amount
