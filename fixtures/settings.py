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
            model.name = "Default"
            model.is_default = True,
            model.created_at = time.time()
            model.updated_at = time.time()
            model.instrument_id = instrument.id
            model.candles_durations = json.dumps([180])
            model.analyzer_working_interval_sec = 5
            model.analyzer_collect_interval_sec = 1
            model.analyzer_bid_times = json.dumps([
                {"time": 300, "admission": 60},
            ]),
            model.analyzer_deep = 5
            model.analyzer_min_deep = 5
            model.analyzer_patterns_control = json.dumps([
                {"expire": 0,
                 "sequence_min_duration": 1,
                 "min_work_time": 0
                 }]),
            model.analyzer_candles_parent_relation = "parent"
            model.analyzer_expiry_time_bid_divider = 5
            model.analyzer_capacity_granularity = 1
            model.analyzer_capacity_type = "change"  # "change","potential"
            model.signaler_min_chance = 80
            model.signaler_min_repeats = 3
            model.signaler_delay_on_trend = 0
            model.signaler_put_max_change_cost = 0
            model.signaler_call_max_change_cost = 0
            model.signaler_min_ticks_count = 0
            model.signaler_trend_chance = 0
            model.save()
