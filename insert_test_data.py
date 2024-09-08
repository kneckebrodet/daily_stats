import random
from datetime import datetime, timedelta
from database import MySQL

class DataInserter:
    def __init__(self, start_date, end_date, user_id):
        self.db = MySQL()
        self.start_date = datetime.strptime(start_date, "%Y/%m/%d")
        self.end_date = datetime.strptime(end_date, "%Y/%m/%d")
        self.current_weight = 75.0  # Starting weight in kg
        self.user_id = user_id  # User ID for inserting data

    def random_sleep_time(self):
        """Generate a random bedtime between 21:00 and 24:00."""
        hour = random.randint(21, 23)
        minute = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"

    def random_exercise_and_walking(self):
        """Generate random exercise and walking values."""
        return random.randint(0, 10), random.randint(0, 10)

    def adjust_weight(self, exercise, walking):
        """Adjust weight based on exercise and walking."""
        if exercise + walking > 12:
            self.current_weight -= random.uniform(0.1, 0.3)
        else:
            self.current_weight += random.uniform(0.1, 0.3)
        # Keep weight within realistic bounds
        self.current_weight = max(60.0, min(self.current_weight, 75.0))
        return round(self.current_weight, 1)

    def random_meditation_and_ifast(self):
        """Generate random meditation and ifast values."""
        return random.choice([0, 1]), random.choice([0, 1])

    def random_skillup_and_reading(self):
        """Generate random skillup and reading values."""
        return random.choice([0, 1]), random.choice([0, 1])

    def insert_data(self):
        """Insert random data into the database."""
        current_date = self.start_date

        while current_date <= self.end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            # Generate random data for this day
            sleep = self.random_sleep_time()
            exercise, walking = self.random_exercise_and_walking()
            weight = self.adjust_weight(exercise, walking)
            meditation, ifast = self.random_meditation_and_ifast()
            skillup, reading = self.random_skillup_and_reading()

            # Prepare data for insertion
            data = {
                "user_id": self.user_id,
                "date": date_str,
                "sleep": sleep,
                "weight": weight,
                "walking": walking,
                "exercise": exercise,
                "skillup": skillup,
                "reading": reading,
                "meditation": meditation,
                "ifast": ifast
            }

            # Insert the data into the database if it does not already exist
            if not self.db.check_if_entry_exists(self.user_id, 'user_data', date_str):
                self.db.add_data('user_data', data)
                print(f"Inserted data for {date_str}: Sleep: {sleep}, Weight: {weight}, Exercise: {exercise}, Walking: {walking}, Skillup: {skillup}, Reading: {reading}, Meditation: {meditation}, IFast: {ifast}")

            # Move to the next day
            current_date += timedelta(days=1)

# Run the data insertion
if __name__ == "__main__":
    # Example usage: Insert data from 2024/01/01 until today for user with ID 1
    start_date = "2024/01/01"
    end_date = datetime.today().strftime("%Y/%m/%d")
    user_id = 1  # Replace with the appropriate user ID

    data_inserter = DataInserter(start_date, end_date, user_id)
    data_inserter.insert_data()
