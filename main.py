from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from datetime import *

# CONSTANTS
DAYS_IN_WEEK = 7  # number of days in a week
DAYS_IN_PREG = 7 * 40  # number of days in expected pregnancy
MIN_WEEKS = 8  # minimum number of weeks into pregnancy to have data
MAX_WEEKS = 44  # maximum number of weeks into pregnancy to have data

# Dictionary for weight at each pregnancy week
weights = {8: '<1g',
           9: '1-2g', 10: '2-4g', 11: '4-7g', 12: '7-14g', 13: '14-25g', 14: '25-45g',
           15: '45-70g', 16: '70-100g', 17: '100-140g', 18: '140-190g', 19: '190-240g',
           20: '240-300g', 21: '300-360g', 22: '360-430g', 23: '430-500g', 24: '500-600g',
           25: '600-700g', 26: '700-800g', 27: '800-900g', 28: '900-1000g', 29: '1000-1175g',
           30: '1175-1350g', 31: '1350-1500g', 32: '1500-1675g', 33: '1675-1825g',
           34: '1825-2000g', 35: '2000-2150g', 36: '2150-2350g', 37: '2350-2500g',
           38: '2500-2725g', 39: '2725-3000g', 40: '3000-3250g', 41: '3250-3500g',
           42: '3500-4000g', 43: '4000-4500g', 44: '>4500g'}

# Dictionary for length at each pregnancy week
lengths = {8: '<4cm',
           9: '4cm', 10: '4-6.5cm', 11: '6.5cm', 12: '6.5-9cm', 13: '9cm', 14: '9-12.5cm',
           15: '12.5cm', 16: '12.5-16cm', 17: '16cm', 18: '16-20.5cm', 19: '20.5cm',
           20: '20.5-25cm', 21: '25cm', 22: '25-27.5cm', 23: '27.5cm', 24: '27.5-30cm',
           25: '30cm', 26: '30-32.5cm', 27: '32.5cm', 28: '32.5-35cm', 29: '35cm',
           30: '35-37.5cm', 31: '37.5cm', 32: '37.5-40cm', 33: '40cm',
           34: '40-42.5cm', 35: '42.5cm', 36: '42.5-45cm', 37: '45cm',
           38: '45-47.5cm', 39: '47.5cm', 40: '47.5-50cm', 41: '50cm',
           42: '50-52.5cm', 43: '52.5cm', 44: '>52.5'}


# This method returns the fetus status today and at projected date, using
# the date of the last period
def get_results(prj_date, last_period):
    # Catch any exceptions caused by bad input
    try:
        s1 = status_today(last_period)
        s2 = status_at_date(prj_date, last_period)
        return "Today: {}, {}\nProjected Date: {}, {}".format(s1['length'], s1['weight'], s2['length'], s2['weight'])
    except:
        return "invalid format/date"


# This method gets the fetus status today, using date of last period
def status_today(last_period):
    return status_at_date(date.today().isoformat(), last_period)


# This method gets the fetus status at a given date, using date of last period
def status_at_date(prj_date, last_period):
    status = dict()
    status['length'] = length_at_date(prj_date, last_period)
    status['weight'] = weight_at_date(prj_date, last_period)
    return status


# This method gets the fetus length at a given date, using date of last period.
def length_at_date(prj_date, lp_date):
    # Get number of weeks between dates
    num_weeks = round(week_delta(prj_date, lp_date))

    # Return length based on weeks
    return lengths[num_weeks] if (MIN_WEEKS <= num_weeks < MAX_WEEKS) else "N/A"


# This method gets the fetus weight at a given date, using date of last period.
def weight_at_date(prj_date, lp_date):
    # Get number of weeks between dates
    num_weeks = round(week_delta(prj_date, lp_date))

    # Return length based on weeks
    return weights[num_weeks] if (MIN_WEEKS <= num_weeks < MAX_WEEKS) else "N/A"


# This method gets the difference in weeks between projected date and date of last period.
def week_delta(prj_date, lp_date):
    try:
        # Create date objects from given ISO formats
        arb_date = date.fromisoformat(prj_date)
        last_period = date.fromisoformat(lp_date)

        # Calculate delta
        delta = arb_date - last_period

        # Return number of weeks
        return delta.days / DAYS_IN_WEEK
    except:
        return -1


# This method converts a given number of days into weeks.
def days_to_weeks(num_days):
    weeks = int(num_days / DAYS_IN_WEEK)
    days = num_days % DAYS_IN_WEEK

    return str(weeks) + " weeks,\n" + str(days) + " days"


# Class used to build and run app
class MyRoot(BoxLayout):
    # Constructor for app
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

    # This method calculates the status of the fetus today and at projected date. It
    # calculates the estimated delivery date and updates the info for the user.
    def calc(self):
        # Create ISO format dates with info
        self.prj_date = self.prj_year + "-" + self.prj_month + "-" + self.prj_day
        self.lp_date = self.lp_year + "-" + self.lp_month + "-" + self.lp_day

        # Try creating date from given ISO format
        try:
            last_prd = date.fromisoformat(self.lp_date)
            future_date = date.fromisoformat(self.prj_date)
            est_delv = last_prd + timedelta(days=7 * 40)
        except ValueError:
            return

        # Enter dates
        self.td_date_btn.text = date.today().isoformat()
        self.prj_date_btn.text = self.prj_date
        self.delv_date_btn.text = est_delv.isoformat()

        # Enter ages
        self.td_age_btn.text = days_to_weeks((date.today() - last_prd).days)
        self.prj_age_btn.text = days_to_weeks((future_date - last_prd).days)
        self.delv_age_btn.text = days_to_weeks((est_delv - last_prd).days)

        # Enter weights
        self.td_weight_btn.text = weight_at_date(date.today().isoformat(), self.lp_date)
        self.prj_weight_btn.text = weight_at_date(self.prj_date, self.lp_date)
        self.delv_weight_btn.text = weight_at_date(est_delv.isoformat(), self.lp_date)

        # Enter lengths
        self.td_length_btn.text = length_at_date(date.today().isoformat(), self.lp_date)
        self.prj_length_btn.text = length_at_date(self.prj_date, self.lp_date)
        self.delv_length_btn.text = length_at_date(est_delv.isoformat(), self.lp_date)

    # This method is called when last period year is selected. It updates the appropriate variable.
    def lp_year_clicked(self, value):
        self.lp_year = value

    # This method is called when last period month is selected. It updates the appropriate variable.
    def lp_month_clicked(self, value):
        self.lp_month = value

    # This method is called when last period day is selected. It updates the appropriate variable.
    def lp_day_clicked(self, value):
        self.lp_day = value

    # This method is called when projected date year is selected. It updates the appropriate variable.
    def prj_year_clicked(self, value):
        self.prj_year = value

    # This method is called when projected date month is selected. It updates the appropriate variable.
    def prj_month_clicked(self, value):
        self.prj_month = value

    # This method is called when projected date day is selected. It updates the appropriate variable.
    def prj_day_clicked(self, value):
        self.prj_day = value


# Class representing the app
class GestationCalcApp(App):
    def build(self):
        return MyRoot()


# Create and run the app
GestationCalcApp().run()
