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
            "Exercise",
            "Sets",
            "Reps",
            "Weight_kg",
            "Duration_Min"
        ])
        df.to_excel(WORKOUT_FILE, index=False)

def get_user_unit(email):
    """Get user's preferred unit from File.xlsx"""
    users_file = "File.xlsx"
    if os.path.exists(users_file):
        df = pd.read_excel(users_file)
        user = df[df["Email"].str.strip().str.lower() == email.strip().lower()]
        if not user.empty:
            return user.iloc[0]["Unit Select"]
    return "Metric"

def kg_to_lbs(kg):
    """Convert kg to lbs"""
    if kg is None or pd.isna(kg):
        return None
    return kg * 2.20462

def lbs_to_kg(lbs):
    """Convert lbs to kg"""
    if lbs is None or pd.isna(lbs):
        return None
    return lbs * 0.453592

def log_workout(email, muscle, exercise, sets=None, reps=None, weight_kg=None, duration=None):
    """Log a workout to workouts.xlsx"""
    init_workout_file()

    row = {
        "Email": email.lower(),
        "Date": datetime.now().date().isoformat(),
        "Muscle": muscle,
        "Exercise": exercise,
        "Sets": int(sets) if sets is not None else None,
        "Reps": int(reps) if reps is not None else None,
        "Weight_kg": weight_kg,
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

    user_unit = get_user_unit(email)
    
    print("\n" + "="*60)
    print(f"YOUR LAST {min(limit, len(user_df))} WORKOUTS")
    print("="*60)
    
    for _, r in user_df.sort_values("Date", ascending=False).head(limit).iterrows():
        print(f"\nDate: {r['Date']}")
        print(f"Muscle Group: {r['Muscle']}")
        print(f"Exercise: {r['Exercise']}")
        
        if pd.notna(r['Sets']) and pd.notna(r['Reps']):
            print(f"Sets x Reps: {int(r['Sets'])}x{int(r['Reps'])}")
        
        if pd.notna(r['Weight_kg']):
            if user_unit.lower() == "us units":
                weight_display = kg_to_lbs(r['Weight_kg'])
                print(f"Weight: {weight_display:.1f} lbs")
            else:
                print(f"Weight: {r['Weight_kg']:.1f} kg")
        
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
    
    # Exercise name
    exercise = input(f"\nEnter exercise name: ").strip()
    
    if not exercise:
        print("Exercise name cannot be empty. Workout not logged.")
        return
    
    # Get user's preferred unit
    user_unit = get_user_unit(email)
    
    # If cardio, only ask for duration
    if muscle == "Cardio":
        while True:
            duration_input = input("\nEnter duration in minutes: ").strip()
            if duration_input.replace('.','').isdigit() and float(duration_input) > 0:
                duration = float(duration_input)
                break
            print("Please enter a positive number.")
        
        log_workout(email, muscle, exercise, sets=None, reps=None, weight_kg=None, duration=duration)
    
    else:
        # For non-cardio: ask sets, reps, weight
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
        
        # Ask for weight in user's preferred unit
        if user_unit.lower() == "us units":
            weight_prompt = "Enter weight in lbs (or press Enter to skip): "
        else:
            weight_prompt = "Enter weight in kg (or press Enter to skip): "
        
        while True:
            weight_input = input(weight_prompt).strip()
            
            if weight_input == "":
                weight_kg = None
                break
            
            if weight_input.replace('.','').isdigit() and float(weight_input) > 0:
                if user_unit.lower() == "us units":
                    weight_kg = lbs_to_kg(float(weight_input))
                else:
                    weight_kg = float(weight_input)
                break
            print("Please enter a positive number or press Enter to skip.")
        
        log_workout(email, muscle, exercise, sets=sets, reps=reps, weight_kg=weight_kg, duration=None)