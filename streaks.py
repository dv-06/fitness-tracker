import pandas as pd
import os
from datetime import datetime, timedelta
import calendar

STREAK_FILE = "streaks.xlsx"
WORKOUT_FILE = "workouts.xlsx"

def init_streak_file():
    """Initialize streak file if it doesn't exist"""
    if not os.path.exists(STREAK_FILE):
        df = pd.DataFrame(columns=[
            "Email",
            "Weekly_Goal",
            "Rest_Days_Marked"
        ])
        df.to_excel(STREAK_FILE, index=False)

def get_user_streak_data(email):
    """Get user's streak settings from streaks.xlsx"""
    init_streak_file()
    df = pd.read_excel(STREAK_FILE)
    user = df[df["Email"].str.strip().str.lower() == email.strip().lower()]
    
    if user.empty:
        # Create default entry for new user
        new_row = pd.DataFrame([[email.lower(), 4, 0]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(STREAK_FILE, index=False)
        return {"Weekly_Goal": 4, "Rest_Days_Marked": 0}
    
    return {
        "Weekly_Goal": int(user.iloc[0]["Weekly_Goal"]),
        "Rest_Days_Marked": int(user.iloc[0]["Rest_Days_Marked"])
    }

def set_weekly_goal(email, goal):
    """Set or update user's weekly workout goal"""
    init_streak_file()
    df = pd.read_excel(STREAK_FILE)
    
    user_exists = df["Email"].str.strip().str.lower() == email.strip().lower()
    
    if user_exists.any():
        df.loc[user_exists, "Weekly_Goal"] = int(goal)
    else:
        new_row = pd.DataFrame([[email.lower(), int(goal), 0]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
    
    df.to_excel(STREAK_FILE, index=False)
    print(f"\n✓ Weekly goal set to {goal} workouts per week!")

def mark_rest_day(email):
    """Mark a rest day for the user"""
    init_streak_file()
    df = pd.read_excel(STREAK_FILE)
    
    user_exists = df["Email"].str.strip().str.lower() == email.strip().lower()
    
    if user_exists.any():
        current_rest = df.loc[user_exists, "Rest_Days_Marked"].iloc[0]
        df.loc[user_exists, "Rest_Days_Marked"] = current_rest + 1
    else:
        new_row = pd.DataFrame([[email.lower(), 4, 1]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
    
    df.to_excel(STREAK_FILE, index=False)
    print("\n✓ Rest day marked! Recovery is important 💤")

def get_user_workouts(email):
    """Get all workout dates for a user from workouts.xlsx"""
    if not os.path.exists(WORKOUT_FILE):
        return []
    
    df = pd.read_excel(WORKOUT_FILE)
    user_workouts = df[df["Email"].str.strip().str.lower() == email.strip().lower()]
    
    if user_workouts.empty:
        return []
    
    # Convert dates to datetime objects and sort
    dates = pd.to_datetime(user_workouts["Date"]).dt.date.tolist()
    return sorted(set(dates))  # Remove duplicates and sort

def get_week_number(date):
    """Get ISO week number and year for a date"""
    return date.isocalendar()[1], date.year

def calculate_weekly_streak(email, weekly_goal):
    """Calculate streak based on weekly workout goals"""
    workout_dates = get_user_workouts(email)
    
    if not workout_dates:
        return 0, 0
    
    # Group workouts by week
    weekly_counts = {}
    for date in workout_dates:
        week, year = get_week_number(date)
        key = (year, week)
        weekly_counts[key] = weekly_counts.get(key, 0) + 1
    
    # Sort weeks chronologically
    sorted_weeks = sorted(weekly_counts.keys())
    
    if not sorted_weeks:
        return 0, 0
    
    # Calculate current streak (from most recent week backwards)
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    # Get current week
    today = datetime.today().date()
    current_week, current_year = get_week_number(today)
    
    # Check if current week meets goal
    current_week_key = (current_year, current_week)
    if current_week_key in weekly_counts and weekly_counts[current_week_key] >= weekly_goal:
        current_streak = 1
        temp_streak = 1
    
    # Go backwards from current week to find streak
    check_year, check_week = current_year, current_week
    
    while True:
        # Move to previous week
        check_date = datetime.strptime(f"{check_year}-W{check_week}-1", "%Y-W%W-%w").date()
        check_date -= timedelta(days=7)
        check_week, check_year = get_week_number(check_date)
        
        week_key = (check_year, check_week)
        
        if week_key not in weekly_counts:
            break
        
        if weekly_counts[week_key] >= weekly_goal:
            current_streak += 1
        else:
            break
        
        # Stop if we've gone back too far
        if check_date < workout_dates[0]:
            break
    
    # Calculate longest streak
    temp_streak = 0
    for i in range(len(sorted_weeks)):
        year, week = sorted_weeks[i]
        
        if weekly_counts[(year, week)] >= weekly_goal:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0
    
    return current_streak, longest_streak

def workouts_this_week(email):
    """Count workouts in current week"""
    workout_dates = get_user_workouts(email)
    today = datetime.today().date()
    current_week, current_year = get_week_number(today)
    
    count = 0
    for date in workout_dates:
        week, year = get_week_number(date)
        if week == current_week and year == current_year:
            count += 1
    
    return count

def workouts_this_month(email):
    """Count workouts in current month"""
    workout_dates = get_user_workouts(email)
    today = datetime.today().date()
    
    count = 0
    for date in workout_dates:
        if date.month == today.month and date.year == today.year:
            count += 1
    
    return count

def monthly_consistency(email, weekly_goal):
    """Calculate monthly consistency based on weekly goals"""
    today = datetime.today().date()
    
    # Calculate how many complete weeks in current month
    first_day = datetime(today.year, today.month, 1).date()
    last_day = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).date()
    
    # Count complete weeks (from Monday to Sunday)
    current_week_num = (today - first_day).days // 7 + 1
    weeks_in_month = (last_day - first_day).days // 7 + 1
    
    # Expected workouts based on complete weeks so far
    expected_workouts = current_week_num * weekly_goal
    actual_workouts = workouts_this_month(email)
    
    if expected_workouts == 0:
        return 0
    
    consistency = (actual_workouts / expected_workouts) * 100
    return min(round(consistency, 1), 100)  # Cap at 100%

def get_streak_metrics(email):
    """Get all streak metrics for a user"""
    user_data = get_user_streak_data(email)
    weekly_goal = user_data["Weekly_Goal"]
    rest_days = user_data["Rest_Days_Marked"]
    
    current_streak, longest_streak = calculate_weekly_streak(email, weekly_goal)
    workouts_week = workouts_this_week(email)
    consistency = monthly_consistency(email, weekly_goal)
    
    return {
        "Weekly_Goal": weekly_goal,
        "Current_Streak": current_streak,
        "Longest_Streak": longest_streak,
        "Workouts_This_Week": workouts_week,
        "Rest_Days_Marked": rest_days,
        "Monthly_Consistency": consistency
    }

def display_streak_metrics(email):
    """Display streak metrics in a nice format"""
    metrics = get_streak_metrics(email)
    
    print("\n" + "="*50)
    print("🔥 YOUR FITNESS STREAK")
    print("="*50)
    
    # Weekly goal and progress
    goal = metrics["Weekly_Goal"]
    this_week = metrics["Workouts_This_Week"]
    progress = "✅" if this_week >= goal else "⏳"
    
    print(f"\n📊 Weekly Goal: {goal} workouts")
    print(f"   This Week: {this_week}/{goal} {progress}")
    
    # Streaks
    current = metrics["Current_Streak"]
    longest = metrics["Longest_Streak"]
    
    if current > 0:
        streak_emoji = "🔥" * min(current, 5)  # Max 5 fire emojis
        print(f"\n🔥 Current Streak: {current} week{'s' if current != 1 else ''} {streak_emoji}")
    else:
        print(f"\n🔥 Current Streak: 0 weeks (Start your streak today!)")
    
    print(f"🏆 Longest Streak: {longest} week{'s' if longest != 1 else ''}")
    
    # Monthly stats
    print(f"\n📅 This Month:")
    print(f"   Consistency: {metrics['Monthly_Consistency']}%")
    
    # Rest days
    print(f"\n💤 Rest Days Marked: {metrics['Rest_Days_Marked']}")
    
    # Motivation message
    if this_week >= goal:
        print("\n💪 Great job! You've hit your weekly goal!")
    elif this_week == goal - 1:
        print(f"\n💪 One more workout to hit your goal this week!")
    elif this_week == 0:
        print("\n💪 Let's get started! Log your first workout this week!")
    else:
        remaining = goal - this_week
        print(f"\n💪 Keep going! {remaining} more workout{'s' if remaining != 1 else ''} to hit your goal!")
    
    print("="*50)

def show_streak_menu(email):
    """Show streak management menu"""
    while True:
        print("\n" + "="*50)
        print("STREAK TRACKER MENU")
        print("="*50)
        print("1. View streak metrics")
        print("2. Set/change weekly goal")
        print("3. Mark rest day")
        print("4. Back to main menu")
        print("="*50)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            display_streak_metrics(email)
        elif choice == "2":
            while True:
                goal_input = input("\nEnter your weekly workout goal (1-7): ").strip()
                if goal_input.isdigit() and 1 <= int(goal_input) <= 7:
                    set_weekly_goal(email, int(goal_input))
                    break
                print("Please enter a number between 1 and 7.")
        elif choice == "3":
            mark_rest_day(email)
        elif choice == "4":
            break
        else:
            print("\nInvalid choice. Please enter 1-4.")
