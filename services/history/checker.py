import time
import datetime

from helpers.exthread import ExThread
from models.quotation import Quotation
from services.controller import Controller
from services.analyzer import Analyzer
from models.prediction import Prediction
from models.pattern import Pattern
from models.signal import Signal
from providers.providers import Providers


class Checker:
    def __init__(self, task):
        self.task = task
        self.instrument = task.setting.instrument
        start = self.task.get_param("start")
        end = self.task.get_param("end")
        quotations = Quotation.get_from_interval(start, end, self.instrument.id)
        self.task.update_status("checker_total_quotations", len(quotations))
        last_quotation = None

        if Providers.config().flush_history:
            Prediction.empty_table(task)
            Pattern.empty_table(task)

        Signal.empty_table(task)

        if len(quotations) > 0:
            checked_quotations = self.task.get_param("checker_checked_quotations")
            if not checked_quotations:
                checked_quotations = 0

            for row in quotations:

                analyzer = Analyzer(task)
                analyzer.quotation = row
                analyzer.do_analysis()

                last_quotation = analyzer.quotation

                Prediction.calculation_cost_for_topical(task, last_quotation)
                Controller.update_expired_signals(self.task, last_quotation)

                checked_quotations += 1
                if checked_quotations % 10 == 0:
                    # Обновляем параметры стоимости прогнозов
                    self.task.update_status("checker_checked_quotations", checked_quotations)

                # Запускаем демона для проверки кеша и получения результата торгов
                self.checker_predictions(last_quotation)
                if checked_quotations % 100 == 0:
                    success_percent = Signal.get_success_percent(self.task)
                    print(datetime.datetime.fromtimestamp(last_quotation.ts), success_percent)

            # Обновляем параметры стоимости прогнозов
            if last_quotation:
                self.checker_predictions(last_quotation)

    def checker_predictions(self, last_quotation):
        Controller.check_expired_predictions(self.task, last_quotation)
