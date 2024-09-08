from database import MySQL 
from datetime import datetime

class Morning:
    def __init__(self, id):
        # get date and time
        self.today = str(datetime.now().date())
        self.time = str(datetime.now().time().strftime("%H:%M"))

        # set database
        self.db = MySQL()

        # add wake up time to db
        wutime_data = {"user_id":id, "date":self.today, "time": self.time}

        if not self.record_exists(id, "wakeup_times", wutime_data["date"]):
            self.db.add_data("wakeup_times", wutime_data)
            print(f"Added wake-up time for user {id}.")
        else:
            print(f"Wake-up time for user {id} already exists for today.")
        
        self.todays_wakeup_time = self.db.get_wakeup_time(id)


    def record_exists(self, user_id, table, date):
        return self.db.check_if_entry_exists(user_id, table, date)  