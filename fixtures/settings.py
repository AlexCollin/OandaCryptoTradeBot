import time
import json

from models.setting import Setting
from models.instrument import Instrument
from fixtures.instruments import Instruments as InstrumentsFixture


class Settings:
    @staticmethod
    def up():
        if Setting.get_count() == 0:
            instrument = Instrument.get_instrument_by_name("EUR_USD")
            if not instrument:
                InstrumentsFixture.up()
            model = Setting()
            model.user_id = 0  # TODO: Create real users
            model.name = "Default",
            model.is_default = True,
            model.created_at = time.time(),
            model.updated_at = time.time(),
            model.instrument_id = instrument.id,
            model.candles_durations = json.dumps([60]),
            model.analyzer_working_interval_sec = 5,
            model.analyzer_collect_interval_sec = 1,
            model.analyzer_bid_times = json.dumps([
                {"time": 60, "admission": 60},
                {"time": 120, "admission": 120},
                {"time": 180, "admission": 180},
                {"time": 240, "admission": 240},
                {"time": 300, "admission": 300}
            ]),
            model.analyzer_deep = 5,
            model.analyzer_min_deep = 5,
            model.analyzer_prediction_expire = json.dumps([{"expire": 0, "history_duration": 0}]),
            model.analyzer_candles_parent_relation = "parent"
            model.analyzer_expiry_time_bid_divider = 30
            model.signaler_min_chance = 70,
            model.signaler_min_repeats = 2,
            model.signaler_delay_on_trend = 0,
            model.signaler_put_max_change_cost = 0
            model.signaler_call_max_change_cost = 0
            model.signaler_min_ticks_count = 0.5
            model.signaler_trend_chance = 70
            model.save()
