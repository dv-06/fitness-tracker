from datetime import datetime, timedelta
import calendar

class FitnessStreak:
    def __init__(self):
        self.workout_dates = []
        self.current_streak = 0
        self.longest_streak = 0
        self.rest_days = 0

    def add_workout(self, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")

        if self.workout_dates:
            last_date = self.workout_dates[-1]
            diff = (date - last_date).days

            if diff == 1:
                self.current_streak += 1
            else:
                self.current_streak = 1
        else:
            self.current_streak = 1

        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.workout_dates.append(date)

    def add_rest_day(self):
        self.rest_days += 1

    def workouts_this_week(self):
        today = datetime.today()
        return len([
            d for d in self.workout_dates
            if d.isocalendar()[1] == today.isocalendar()[1] and d.year == today.year
        ])

    def monthly_consistency(self):
        today = datetime.today()
        days_in_month = calendar.monthrange(today.year, today.month)[1]

        workouts = len([
            d for d in self.workout_dates
            if d.month == today.month and d.year == today.year
        ])

        return round((workouts / days_in_month) * 100, 2)

    def get_metrics(self):
        return {
            "Current Streak": self.current_streak,
            "Longest Streak": self.longest_streak,
            "Workouts This Week": self.workouts_this_week(),
            "Rest Days Taken": self.rest_days,
            "Monthly Consistency (%)": self.monthly_consistency()
        }


if __name__ == "__main__":
    tracker = FitnessStreak()

    while True:
        action = input("\nEnter 'w' to add workout, 'r' for rest day, 'm' to show metrics, 'q' to quit: ").lower()

        if action == 'w':
            date_str = input("Enter workout date (YYYY-MM-DD): ")
            try:
                tracker.add_workout(date_str)
                print("Workout added!")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        elif action == 'r':
            tracker.add_rest_day()
            print("Rest day added!")
        elif action == 'm':
            print("\n--- Fitness Metrics ---")
            for k, v in tracker.get_metrics().items():
                print(f"{k}: {v}")
        elif action == 'q':
            print("Exiting tracker. Stay consistent 💪")
            break
        else:
            print("Invalid choice. Try again.")

    print(tracker.get_metrics())
