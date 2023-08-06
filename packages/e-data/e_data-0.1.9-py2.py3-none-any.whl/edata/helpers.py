import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from edata.connectors import *
from edata.processors import *
import asyncio

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PLATFORMS = ['datadis', 'edistribucion']
ATTRIBUTES = {
    "cups": None,
    "contract_p1_kW": 'kW',
    "contract_p2_kW": 'kW',
    "today_kWh": 'kWh',
    "today_p1_kWh": 'kWh',
    "today_p2_kWh": 'kWh',
    "today_p3_kWh": 'kWh',
    "yesterday_kWh": 'kWh',
    "yesterday_p1_kWh": 'kWh',
    "yesterday_p2_kWh": 'kWh',
    "yesterday_p3_kWh": 'kWh',
    "month_kWh": 'kWh',
    "month_daily_kWh": 'kWh',
    "month_days": 'd',
    "month_p1_kWh": 'kWh',
    "month_p2_kWh": 'kWh',
    "month_p3_kWh": 'kWh',
    "last_month_kWh": 'kWh',
    "last_month_daily_kWh": 'kWh',
    "last_month_days_kWh": 'd',
    "last_month_p1_kWh": 'kWh',
    "last_month_p2_kWh": 'kWh',
    "last_month_p3_kWh": 'kWh',
    "max_power_kW": 'kW',
    "max_power_date": None,
    "max_power_mean_kW": 'kW',
    "max_power_90perc_kW": 'kW'
}

class PlatformError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return f'{self.message}'

class ReportHelper ():

    data = {}
    attributes = {}

    def __init__(self, platform, username, password, cups) -> None:
        _LOGGER.debug ('ReportHelper: initializing')
        self.__cups = cups
        self.__loop = None
        if platform == 'datadis':
            self.__conn = DatadisConnector (username, password)
        elif platform == 'edistribucion':
            self.__conn = EdistribucionConnector (username, password)
        else:
            raise PlatformError (f'platform {platform} not supported, valid options are {PLATFORMS}')

    async def async_update (self):
        _LOGGER.debug ('ReportHelper: requesting an async update')
        if self.__loop is None:
            self.__loop = asyncio.get_event_loop()
        self.__loop.run_in_executor(None, self.update)

    def update (self):
        date_from = datetime (
                datetime.today ().year, 
                datetime.today ().month, 
                1, 0, 0, 0
            ) - relativedelta (months=12)
        date_to = datetime.today()
        _LOGGER.debug (f'ReportHelper: requesting an update from {date_from} to {date_to}')
        if self.update_data (self.__cups, date_from, date_to):
            self.data = self.__conn.data
            self.update_attr ()

    def update_data (self, cups, date_from=None, date_to=None):
        _LOGGER.debug (f'ReportHelper: updating data from {date_from} to {date_to}')
        return self.__conn.update (cups, date_from, date_to)

    def update_attr (self):
        _LOGGER.debug ('ReportHelper: updating attributes')

        self.update_attr_supplies ()
        self.update_attr_contracts ()
        self.update_attr_consumptions ()
        self.update_attr_maximeter ()

        _LOGGER.debug ('ReportHelper: rounding attributes')
        for a in self.attributes:
            if a in ATTRIBUTES and ATTRIBUTES[a] is not None:
                self.attributes[a] = round(self.attributes[a], 2) if self.attributes[a] is not None else '-'

    def update_attr_supplies (self):
        try:
            for i in self.data['supplies']:
                if i['cups'] == self.__cups:
                    self.attributes['cups'] = self.__cups
                    break
        except Exception as e:
            _LOGGER.exception (e)

    def update_attr_contracts (self):
        try:
            for i in self.data['contracts']:
                if i['date_end'] is None:
                    self.attributes['contract_p1_kW'] = i['power_p1'] if 'power_p1' in i else None
                    self.attributes['contract_p2_kW'] = i['power_p2'] if 'power_p2' in i else None
                    break
        except Exception as e:
            _LOGGER.exception (e)

    def update_attr_consumptions (self):

        try:
            processor = ConsumptionProcessor (self.data['consumptions'])

            today_starts = datetime (
                datetime.today ().year, 
                datetime.today ().month, 
                datetime.today ().day, 0, 0, 0
            )
            
            # update yesterday
            a = processor.get_stats (today_starts-timedelta(days=1), today_starts)
            self.attributes["yesterday_kWh"] = a['total_kWh'] if 'total_kWh' in a else None
            self.attributes["yesterday_p1_kWh"] = a['p1_kWh'] if 'p1_kWh' in a else None
            self.attributes["yesterday_p2_kWh"] = a['p2_kWh'] if 'p2_kWh' in a else None
            self.attributes["yesterday_p3_kWh"] = a['p3_kWh'] if 'p3_kWh' in a else None

            cycle_starts = datetime (
                datetime.today ().year, 
                datetime.today ().month, 1, 0, 0, 0
            )

            # update current cycle
            a = processor.get_stats (cycle_starts, cycle_starts + relativedelta(months=1))
            self.attributes["month_kWh"] = a['total_kWh'] if 'total_kWh' in a else None
            self.attributes["month_days"] = a['days'] if 'days' in a else None
            self.attributes["month_daily_kWh"] = a['daily_kWh'] if 'daily_kWh' in a else None
            self.attributes["month_p1_kWh"] = a['p1_kWh'] if 'p1_kWh' in a else None
            self.attributes["month_p2_kWh"] = a['p2_kWh'] if 'p2_kWh' in a else None
            self.attributes["month_p3_kWh"] = a['p3_kWh'] if 'p3_kWh' in a else None

            # update last cycle
            a = processor.get_stats (cycle_starts - relativedelta (months=1), cycle_starts)
            self.attributes["last_month_kWh"] = a['total_kWh'] if 'total_kWh' in a else None
            self.attributes["last_month_days_kWh"] = a['days'] if 'days' in a else None
            self.attributes["last_month_daily_kWh"] = a['daily_kWh'] if 'daily_kWh' in a else None
            self.attributes["last_month_p1_kWh"] = a['p1_kWh'] if 'p1_kWh' in a else None
            self.attributes["last_month_p2_kWh"] = a['p2_kWh'] if 'p2_kWh' in a else None
            self.attributes["last_month_p3_kWh"] = a['p3_kWh'] if 'p3_kWh' in a else None
        except Exception as e:
            _LOGGER.exception (e)

    def update_attr_maximeter (self):
        try:
            processor = MaximeterProcessor (self.data['maximeter'])
            a = processor.get_stats (datetime.today() - timedelta(days=365), datetime.today())
            self.attributes['max_power_kW'] = a['peak_kW'] if 'peak_kW' in a else None
            self.attributes['max_power_date'] = a['peak_date'] if 'peak_date' in a else None
            self.attributes['max_power_mean_kW'] = a['peak_mean_kWh'] if 'peak_mean_kWh' in a else None
            self.attributes['max_power_90perc_kW'] = a['peak_tile90_kWh'] if 'peak_tile90_kWh' in a else None
        except Exception as e:
            _LOGGER.exception (e)

    def __str__(self) -> str:
        return '\n'.join([f'{i}: {self.attributes[i]}' for i in self.attributes])