import pandas as pd
import os
from datetime import datetime

WORKOUT_FILE = "workouts.xlsx"

def init_workout_file():
    """Initialize workout file if it doesn't exist"""
    if not os.path.exists(WORKOUT_FILE):
        df = pd.DataFrame(columns=[
            "Email",
            "Date",
            "Muscle",
            "Sets",
            "Reps",
            "Duration_Min"
        ])
        df.to_excel(WORKOUT_FILE, index=False)

def log_workout(email, muscle, sets=None, reps=None, duration=None):
    """Log a workout to workouts.xlsx"""
    init_workout_file()

    row = {
        "Email": email.lower(),
        "Date": datetime.now().date().isoformat(),
        "Muscle": muscle,
        "Sets": int(sets) if sets is not None else None,
        "Reps": int(reps) if reps is not None else None,
        "Duration_Min": duration
    }

    df = pd.read_excel(WORKOUT_FILE)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(WORKOUT_FILE, index=False)
    
    print("\n✓ Workout logged successfully!")

def show_recent_workouts(email, limit=5):
    """Show recent workouts for a user"""
    if not os.path.exists(WORKOUT_FILE):
        print("\nNo workouts logged yet.")
        return

    df = pd.read_excel(WORKOUT_FILE)
    user_df = df[df["Email"].str.strip().str.lower() == email.strip().lower()]

    if user_df.empty:
        print("\nNo workouts found for your account.")
        return
    
    print("\n" + "="*60)
    print(f"YOUR LAST {min(limit, len(user_df))} WORKOUTS")
    print("="*60)
    
    for _, r in user_df.sort_values("Date", ascending=False).head(limit).iterrows():
        print(f"\nDate: {r['Date']}")
        print(f"Muscle Group: {r['Muscle']}")
        
        if pd.notna(r['Sets']) and pd.notna(r['Reps']):
            print(f"Sets x Reps: {int(r['Sets'])}x{int(r['Reps'])}")
        
        if pd.notna(r['Duration_Min']):
            print(f"Duration: {int(r['Duration_Min'])} minutes")
        
        print("-" * 60)

def show_workout_menu(email):
    """Display workout logging menu"""
    print("\n" + "="*50)
    print("LOG A WORKOUT")
    print("="*50)
    
    # Muscle group selection
    print("\nSelect muscle group:")
    print("1. Chest")
    print("2. Back")
    print("3. Legs")
    print("4. Shoulders")
    print("5. Arms")
    print("6. Core")
    print("7. Full Body")
    print("8. Cardio")
    
    muscle_map = {
        "1": "Chest",
        "2": "Back",
        "3": "Legs",
        "4": "Shoulders",
        "5": "Arms",
        "6": "Core",
        "7": "Full Body",
        "8": "Cardio"
    }
    
    while True:
        muscle_choice = input("\nEnter choice (1-8): ").strip()
        if muscle_choice in muscle_map:
            muscle = muscle_map[muscle_choice]
            break
        print("Invalid choice. Please enter 1-8.")
    
    # If cardio, only ask for duration
    if muscle == "Cardio":
        while True:
            duration_input = input("\nEnter duration in minutes: ").strip()
            if duration_input.replace('.','').isdigit() and float(duration_input) > 0:
                duration = float(duration_input)
                break
            print("Please enter a positive number.")
        
        log_workout(email, muscle, sets=None, reps=None, duration=duration)
    
    else:
        # For non-cardio: ask sets and reps only
        while True:
            sets_input = input("\nEnter number of sets: ").strip()
            if sets_input.isdigit() and int(sets_input) > 0:
                sets = int(sets_input)
                break
            print("Please enter a positive number.")
        
        while True:
            reps_input = input("Enter number of reps: ").strip()
            if reps_input.isdigit() and int(reps_input) > 0:
                reps = int(reps_input)
                break
            print("Please enter a positive number.")
        
        log_workout(email, muscle, sets=sets, reps=reps, duration=None)
