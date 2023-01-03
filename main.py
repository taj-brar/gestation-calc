from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from datetime import *

DAYS_IN_WEEK = 7
MIN_WEEKS = 8
MAX_WEEKS = 44

weights = {8: '<1g',
           9: '1-2g', 10: '2-4g', 11: '4-7g', 12: '7-14g', 13: '14-25g', 14: '25-45g',
           15: '45-70g', 16: '70-100g', 17: '100-140g', 18: '140-190g', 19: '190-240g',
           20: '240-300g', 21: '300-360g', 22: '360-430g', 23: '430-500g', 24: '500-600g',
           25: '600-700g', 26: '700-800g', 27: '800-900g', 28: '900-1000g', 29: '1000-1175g',
           30: '1175-1350g', 31: '1350-1500g', 32: '1500-1675g', 33: '1675-1825g',
           34: '1825-2000g', 35: '2000-2150g', 36: '2150-2350g', 37: '2350-2500g',
           38: '2500-2725g', 39: '2725-3000g', 40: '3000-3250g', 41: '3250-3500g',
           42: '3500-4000g', 43: '4000-4500g', 44: '>4500g'}

lengths = {8: '<4cm',
           9: '4cm', 10: '4-6.5cm', 11: '6.5cm', 12: '6.5-9cm', 13: '9cm', 14: '9-12.5cm',
           15: '12.5cm', 16: '12.5-16cm', 17: '16cm', 18: '16-20.5cm', 19: '20.5cm',
           20: '20.5-25cm', 21: '25cm', 22: '25-27.5cm', 23: '27.5cm', 24: '27.5-30cm',
           25: '30cm', 26: '30-32.5cm', 27: '32.5cm', 28: '32.5-35cm', 29: '35cm',
           30: '35-37.5cm', 31: '37.5cm', 32: '37.5-40cm', 33: '40cm',
           34: '40-42.5cm', 35: '42.5cm', 36: '42.5-45cm', 37: '45cm',
           38: '45-47.5cm', 39: '47.5cm', 40: '47.5-50cm', 41: '50cm',
           42: '50-52.5cm', 43: '52.5cm', 44: '>52.5'}


def get_results(prj_date, last_period):
    # Catch any exceptions caused by bad input
    try:
        s1 = status_today(last_period)
        s2 = status_at_date(prj_date, last_period)
        return "Today: {}, {}\nProjected Date: {}, {}".format(s1['length'], s1['weight'], s2['length'], s2['weight'])
    except:
        return "invalid format/date"


def status_today(last_period):
    return status_at_date(date.today().isoformat(), last_period)


def status_at_date(prj_date, last_period):
    status = dict()
    status['length'] = length_at_date(prj_date, last_period)
    status['weight'] = weight_at_date(prj_date, last_period)
    return status


def length_at_date(prj_date, lp_date):
    # Get number of weeks between dates
    num_weeks = week_delta(prj_date, lp_date)

    # Return length based on weeks
    return lengths[num_weeks] if (MIN_WEEKS <= num_weeks < MAX_WEEKS) else "N/A"


def weight_at_date(prj_date, lp_date):
    # Get number of weeks between dates
    num_weeks = week_delta(prj_date, lp_date)

    # Return length based on weeks
    return weights[num_weeks] if (MIN_WEEKS <= num_weeks < MAX_WEEKS) else "N/A"


def week_delta(prj_date, lp_date):
    # Create date objects from given ISO formats
    arb_date = date.fromisoformat(prj_date)
    last_period = date.fromisoformat(lp_date)

    # Calculate delta
    delta = arb_date - last_period

    # Return number of weeks
    return round(delta.days / DAYS_IN_WEEK)


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

        # Instantiate
        self.lp_year = "-1"
        self.lp_month = "-1"
        self.lp_day = "-1"
        self.prj_year = "-1"
        self.prj_month = "-1"
        self.prj_day = "-1"
        self.prj_date = "-1"
        self.lp_date = "-1"

    def calc(self):
        # Create dates
        self.prj_date = self.prj_year + "-" + self.prj_month + "-" + self.prj_day
        self.lp_date = self.lp_year + "-" + self.lp_month + "-" + self.lp_day

        # Enter result into text field
        self.results.text = get_results(self.prj_date, self.lp_date)

    def lp_year_clicked(self, value):
        self.lp_year = value

    def lp_month_clicked(self, value):
        self.lp_month = value

    def lp_day_clicked(self, value):
        self.lp_day = value

    def prj_year_clicked(self, value):
        self.prj_year = value

    def prj_month_clicked(self, value):
        self.prj_month = value

    def prj_day_clicked(self, value):
        self.prj_day = value


class GestationCalcApp(App):
    def build(self):
        return MyRoot()


GestationCalcApp().run()
