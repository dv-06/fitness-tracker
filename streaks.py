from datetime import datetime, timedelta

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
            elif diff > 1:
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
            if (today - d).days <= 7
        ])

    def monthly_consistency(self):
        today = datetime.today()
        days_in_month = (today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)).day

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
    tracker.add_workout("2026-01-01")
    tracker.add_workout("2026-01-02")
    tracker.add_workout("2026-01-03")
    tracker.add_rest_day()
    tracker.add_workout("2026-01-05")

    print(tracker.get_metrics())
