from datetime import datetime
from database import MySQL

class Night:
    def __init__(self, id, data):
        self.id = id
        self.data_values = data # [weight(kg),walking(0-300),exercise(0-300),learn(0-300),read(0-300),
                         # meditation(true/false), ifast(true/false)]

        self.data_keys = ["weight", "walking", "exercise", "skillup", "reading", "meditation", "ifast"]

        # combine keys and values from lists into a dict
        self.data = {key: value for key, value in zip(self.data_keys, self.data_values)}
        print(self.data)

        # get date and time
        self.today = str(datetime.now().date())
        self.time = str(datetime.now().time().strftime("%H:%M"))

        # set database
        self.db = MySQL()

        # calculate sleeptime
        self.yesterday_bedtime = self.db.get_bedtime(self.id)
        self.today_wutime = self.db.get_wakeup_time(self.id)
        if self.yesterday_bedtime == None or self.today_wutime == None:
            self.sleep_time = None
        else:
            self.sleep_time = self.get_sleep(self.yesterday_bedtime, self.today_wutime)

        # add extra attributes to the data and send to DB
        return_data = {
            "user_id": id,
            "date": self.today,
            "sleep": self.sleep_time,
        }
        return_data.update(self.data)

        if self.record_exists(id, "user_data", self.today):
            self.db.update_data(id, "user_data", return_data)
        else:
            self.db.add_data("user_data", return_data)

        # add todays bedtime to database
        self.bedtime_data = {"user_id": id, "date":self.today, "time": self.time}
        if self.record_exists(id, "bed_times", self.today):
            self.db.update_data(id, "bed_times", self.bedtime_data)
        else:
            self.db.add_data("bed_times", self.bedtime_data)

    def get_sleep(self, bedtime, wutime):
        bedtime_hour_minute= bedtime.split(":")
        wutime_hour_minute = wutime.split(":")
        bedtime_hour, bedtime_minute = int(bedtime_hour_minute[0]), int(bedtime_hour_minute[1])
        wakeup_hour, wakeup_minute = int(wutime_hour_minute[0]), int(wutime_hour_minute[1])

        hour_diff = (wakeup_hour + 24) - bedtime_hour
        minute_diff = bedtime_minute - wakeup_minute
        if minute_diff < 0:
            return f"{hour_diff}:{abs(minute_diff)}"
        elif minute_diff > 0:
            return f"{hour_diff - 1}:{60 - minute_diff}"
        else:
            return f"{hour_diff}:00"

    def record_exists(self, id, table, date):
        return self.db.check_if_entry_exists(id, table, date)
