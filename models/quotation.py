from providers.providers import Providers


class Quotation(object):
    ts = 0
    instrument_id = None
    ask = None
    bid = None
    value = None

    def __init__(self, raw=None):
        if raw:
            self.__dict__.update(raw._asdict())

    def save(self):
        cursor = Providers.db().get_cursor()
        row = cursor.execute("INSERT INTO quotations (ts, instrument_id, ask, bid, value) "
                             "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (ts,instrument_id) DO NOTHING RETURNING ts",
                             (self.ts, self.instrument_id, self.ask, self.bid, self.value))

        Providers.db().commit()
        if row:
            return self

    def __tuple_str(self):
        return str((self.ts, self.instrument_id, self.ask, self.bid, self.value))

    @staticmethod
    def model(raw=None):
        return Quotation(raw)

    @staticmethod
    def save_many(quotations: list):
        cursor = Providers.db().get_cursor()
        query = 'INSERT INTO quotations (ts, instrument_id, ask, bid, "value") VALUES ' + \
                ','.join(v.__tuple_str() for v in quotations) + \
                ' ON CONFLICT (ts,instrument_id) DO NOTHING RETURNING ts as ts'
        cursor.execute(query)
        Providers.db().commit()
        res = cursor.fetchall()
        if res:
            return res
        return []

    @staticmethod
    def prepare_candle(from_ts, duration, instrument_id):
        cursor = Providers.db().get_cursor()
        cursor.execute("SELECT "
                       "MAX(value) OVER w AS high, "
                       "MIN(value) OVER w AS low, "
                       "first_value(value) OVER w AS open, "
                       "last_value(value) OVER w AS close, "
                       "AVG(value) OVER w AS average "
                       "FROM quotations WHERE ts>=%s AND instrument_id=%s AND ts<=%s "
                       "WINDOW w AS () "
                       "ORDER BY ts DESC LIMIT 1",
                       [from_ts - duration, instrument_id, from_ts])
        candle_raw = cursor.fetchone()
        if candle_raw:
            return candle_raw

    @staticmethod
    def get_from_interval(start_ts, end_ts, instrument_id):
        cursor = Providers.db().get_cursor()
        cursor.execute(
            "SELECT * FROM quotations WHERE ts>=%s AND ts<=%s AND instrument_id=%s ORDER BY ts;",
            (start_ts, end_ts, instrument_id))
        rows = cursor.fetchall()
        res = []
        if rows:
            for row in rows:
                res.append(Quotation.model(row))
        return res

    @staticmethod
    def get_one_to_ts(ts, instrument_id):
        cursor = Providers.db().get_cursor()
        cursor.execute(
            "SELECT * FROM quotations WHERE ts<=%s AND instrument_id=%s ORDER BY ts LIMIT 1",
            (ts, instrument_id))
        row = cursor.fetchone()
        if row:
            return Quotation.model(row)
