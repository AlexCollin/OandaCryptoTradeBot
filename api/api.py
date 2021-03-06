import oandapy
import json

from api.stream.quotations import Quotations
from providers.config import get_config


class Api(object):
    api = None
    account_id = None
    instruments = None
    environment = None
    access_token = None
    stream = None

    def __init__(self):
        config = get_config()
        self.account_id = config.get_broker_account_id()
        self.environment = config.get_broker_environment()
        self.access_token = config.get_broker_access_token()
        self.api = oandapy.API(**{
            "environment": config.get_broker_environment(),
            "access_token": config.get_broker_access_token(),
        })

    def get_instruments(self):
        return self.api.get_instruments(self.account_id)["instruments"]

    def quotations_stream(self, quotation, instrument):
        self.stream = Quotations(quotation, 0, environment=self.environment, access_token=self.access_token)
        self.stream.rates(self.account_id, instrument.instrument)

    def get_history(self, **params):
        try:
            return self.api.get_history(**params)
        except json.JSONDecodeError:
            return []
