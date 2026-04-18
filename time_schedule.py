import datetime

class TimeSchedule:
    @staticmethod
    def get_current_date():
        return datetime.date.today().strftime("%B %d, %Y")
    
    @staticmethod
    def calculate_arrival_date(delivery_days):
        current_date = datetime.date.today()
        arrival_date = current_date + datetime.timedelta(days=delivery_days)
        return arrival_date.strftime("%B %d, %Y")
    