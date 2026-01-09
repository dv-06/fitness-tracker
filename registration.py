import pandas as pd
import os
from calculation import record_calculation
from workout import show_workout_menu
from streak import show_streak_menu

users = "File.xlsx"

# Create file if missing
if not os.path.exists(users) or os.path.getsize(users) == 0:
    df = pd.DataFrame(columns=[
        "Name", "Email", "Password", "Security Question",
        "Unit Select", "Weight_kg", "Height_cm", "Age", "Gender"
    ])
    df.to_excel(users, index=False)
else:
    df = pd.read_excel(users)

# ------------------ SHARED HELPERS ------------------

def emailid_valid(email):
    return isinstance(email, str) and "@" in email and "." in email

def emailid_exists(email, df):
    return email.strip().lower() in df["Email"].astype(str).str.strip().str.lower().values

def get_user_password(email, df):
    result = df.loc[df["Email"].str.strip().str.lower() == email.strip().lower(), "Password"]
    if not result.empty:
        return result.iloc[0]
    return None

def password_valid(password):
    if len(password) < 8:
        print("Invalid password: must be at least 8 characters")
        return False
    if not any(char.isdigit() for char in password):
        print("Invalid password: must contain a digit")
        return False
    if not any(char.isupper() for char in password):
        print("Invalid password: must contain an uppercase letter")
        return False
    return True

def kg_to_lbs(kg):
    return kg * 2.20462

def lbs_to_kg(lbs):
    return lbs * 0.453592

def cm_to_feet_inches(cm):
    total_inches = cm / 2.54
    feet = int(total_inches // 12)
    inches = int(total_inches % 12)
    return feet, inches

def feet_inches_to_cm(feet, inches):
    total_inches = feet * 12 + inches
    return total_inches * 2.54

def get_user_sq(email, df):
    result = df.loc[df["Email"].str.strip().str.lower() ==
                    email.strip().lower(), "Security Question"]
    if not result.empty:
        return result.iloc[0]
    return None

def change_password(email, new_password, df):
    df.loc[df["Email"].str.strip().str.lower() ==
           email.strip().lower(), "Password"] = new_password
    df.to_excel(users, index=False)
    print("\n✓ Password changed successfully!")

def get_user_info(email):
    """Get user information from File.xlsx"""
    df = pd.read_excel(users)
    user = df[df["Email"].str.strip().str.lower() == email.strip().lower()]
    if not user.empty:
        return user.iloc[0]
    return None

# ------------------ SIGNUP FUNCTION ------------------

def signup_user():
    df = pd.read_excel(users)
    
    name = input("Enter the Name of the user: ")

    # Email validation
    attempts = 0
    MAX_ATTEMPTS = 8
    while True:
        email = input("Enter the Email id of the user: ").strip()
        attempts += 1

        if not emailid_valid(email):
            print("Invalid email format. It must contain '@' and '.' (example: name@example.com).")
            if attempts >= MAX_ATTEMPTS:
                print("Too many invalid attempts. Exiting signup.")
                exit()
            continue

        if emailid_exists(email, df):
            print("Email id already exists. Try signing in or use a different email.")
            if attempts >= MAX_ATTEMPTS:
                print("Too many attempts. Exiting signup.")
                exit()
            continue

        break

    # Password validation
    while True:
        password = input("Enter the Password of the user: ")
        if password_valid(password):
            break

    print("Enter the Security Question")
    sq = input("Any Secret word: ")

    unit_select = input("Enter your unit of measurement (US Units or Metric): ").strip()

    # Get input in user's preferred units, but store in metric
    if unit_select.lower() == "us units":
        while True:
            weight_input = input("Enter your weight in lbs: ")
            height_input = input("Enter your height in feet and inches (ex: 5 10): ")
            height_parts = height_input.split()
            age = input("Enter your age: ")
            gender = input("Enter your gender: ")

            if (weight_input.replace('.','').isdigit() and age.isdigit() and
                len(height_parts) == 2 and height_parts[0].isdigit() and height_parts[1].isdigit()):
                weight_kg = lbs_to_kg(float(weight_input))
                height_cm = feet_inches_to_cm(int(height_parts[0]), int(height_parts[1]))
                break
            else:
                print("Invalid input. Please enter numeric values.")

    else:
        while True:
            weight_input = input("Enter your weight in kg: ")
            height_input = input("Enter your height in cm: ")
            age = input("Enter your age: ")
            gender = input("Enter your gender: ")
            if weight_input.replace('.','').isdigit() and height_input.replace('.','').isdigit() and age.isdigit():
                weight_kg = float(weight_input)
                height_cm = float(height_input)
                break
            else:
                print("Invalid input. Please enter numeric values.")

    new_data = pd.DataFrame([[name, email, password, sq, unit_select,
                              weight_kg, height_cm, age, gender]], columns=df.columns)

    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(users, index=False)

    print("\n✓ Signup Successful!")
    return email

# ------------------ PLAN SETUP FUNCTION ------------------

def setup_plan(email):
    df = pd.read_excel(users)
    user = df[df["Email"].str.strip().str.lower() == email.strip().lower()].iloc[0]
    
    weight_kg = user["Weight_kg"]
    height_cm = user["Height_cm"]
    age = user["Age"]
    gender = user["Gender"]
    unit_select = user["Unit Select"]

    print("\n--- Now let's set up your fitness goals ---\n")

    # Activity level selection
    print("Select your activity level:")
    print("1. Sedentary (little or no exercise)")
    print("2. Light (exercise 1-3 days/week)")
    print("3. Moderate (exercise 3-5 days/week)")
    print("4. Very Active (exercise 6-7 days/week)")
    print("5. Extremely Active (physical job or training twice per day)")

    activity_map = {
        "1": "sedentary",
        "2": "light",
        "3": "moderate",
        "4": "very_active",
        "5": "extremely_active"
    }

    while True:
        activity_choice = input("Enter choice (1-5): ").strip()
        if activity_choice in activity_map:
            activity = activity_map[activity_choice]
            break
        print("Invalid choice. Please enter 1-5.")

    # Goal selection
    print("\nSelect your fitness goal:")
    print("1. Weight Loss")
    print("2. Weight Gain")
    print("3. Muscle Building")

    goal_map = {
        "1": "loss",
        "2": "gain",
        "3": "muscle"
    }

    while True:
        goal_choice = input("Enter choice (1-3): ").strip()
        if goal_choice in goal_map:
            goal = goal_map[goal_choice]
            break
        print("Invalid choice. Please enter 1-3.")

    # Calculate BMR, TDEE, Protein
    result = record_calculation(
        email=email,
        weight_val=weight_kg,
        weight_unit="kg",
        height_val=height_cm,
        height_unit="cm",
        age=int(age),
        sex=gender,
        activity=activity,
        goal=goal
    )

    # Display in user's preferred units
    if unit_select.lower() == "us units":
        display_weight = kg_to_lbs(weight_kg)
        feet, inches = cm_to_feet_inches(height_cm)
        print(f"\n--- Your Profile ---")
        print(f"Weight: {display_weight:.1f} lbs")
        print(f"Height: {feet}'{inches}\"")
    else:
        print(f"\n--- Your Profile ---")
        print(f"Weight: {weight_kg:.1f} kg")
        print(f"Height: {height_cm:.1f} cm")

    print(f"Age: {age}")
    print(f"Gender: {gender}")
    print(f"\n--- Calculations ---")
    print(f"BMI: {result['BMI']:.2f}")
    print(f"BMI Category: {result['BMI_Category']}")
    print(f"BMR (Basal Metabolic Rate): {result['BMR']:.0f} calories/day")
    print(f"TDEE (Total Daily Energy Expenditure): {result['TDEE']:.0f} calories/day")
    print(f"Recommended Protein: {result['Protein_g']:.1f} g/day")

    # Show plans based on goal
    print(f"\n--- Available Plans for {goal.upper()} ---\n")

    plans_data = []

    if goal == "loss":
        plans = {
            "Mild": {"deficit_pct": 10, "calories": result['TDEE'] * 0.90},
            "Moderate": {"deficit_pct": 20, "calories": result['TDEE'] * 0.80},
            "Aggressive": {"deficit_pct": 25, "calories": result['TDEE'] * 0.75}
        }
        
        for plan_name, plan_info in plans.items():
            daily_deficit = result['TDEE'] - plan_info['calories']
            weekly_deficit = daily_deficit * 7
            monthly_deficit = weekly_deficit * 4
            
            weekly_loss_kg = weekly_deficit / 7700
            monthly_loss_kg = monthly_deficit / 7700
            
            if unit_select.lower() == "us units":
                weekly_loss = kg_to_lbs(weekly_loss_kg)
                monthly_loss = kg_to_lbs(monthly_loss_kg)
                unit_display = "lbs"
            else:
                weekly_loss = weekly_loss_kg
                monthly_loss = monthly_loss_kg
                unit_display = "kg"
            
            plans_data.append({
                "plan": plan_name,
                "calories": plan_info['calories'],
                "weekly_loss": weekly_loss,
                "monthly_loss": monthly_loss,
                "unit": unit_display
            })
            
            print(f"{plan_name} Plan ({plan_info['deficit_pct']}% deficit):")
            print(f"  Daily Calories: {plan_info['calories']:.0f}")
            print(f"  Projected Loss: {weekly_loss:.2f} {unit_display}/week, {monthly_loss:.2f} {unit_display}/month")
            print()

    elif goal == "gain":
        plans = {
            "Mild": {"surplus_pct": 10, "calories": result['TDEE'] * 1.10},
            "Moderate": {"surplus_pct": 15, "calories": result['TDEE'] * 1.15},
            "Aggressive": {"surplus_pct": 20, "calories": result['TDEE'] * 1.20}
        }
        
        for plan_name, plan_info in plans.items():
            daily_surplus = plan_info['calories'] - result['TDEE']
            weekly_surplus = daily_surplus * 7
            monthly_surplus = weekly_surplus * 4
            
            weekly_gain_kg = weekly_surplus / 7700
            monthly_gain_kg = monthly_surplus / 7700
            
            if unit_select.lower() == "us units":
                weekly_gain = kg_to_lbs(weekly_gain_kg)
                monthly_gain = kg_to_lbs(monthly_gain_kg)
                unit_display = "lbs"
            else:
                weekly_gain = weekly_gain_kg
                monthly_gain = monthly_gain_kg
                unit_display = "kg"
            
            plans_data.append({
                "plan": plan_name,
                "calories": plan_info['calories'],
                "weekly_gain": weekly_gain,
                "monthly_gain": monthly_gain,
                "unit": unit_display
            })
            
            print(f"{plan_name} Plan ({plan_info['surplus_pct']}% surplus):")
            print(f"  Daily Calories: {plan_info['calories']:.0f}")
            print(f"  Projected Gain: {weekly_gain:.2f} {unit_display}/week, {monthly_gain:.2f} {unit_display}/month")
            print()

    elif goal == "muscle":
        plan_name = "Mild"
        surplus_pct = 5
        calories = result['TDEE'] * 1.05
        
        daily_surplus = calories - result['TDEE']
        weekly_surplus = daily_surplus * 7
        monthly_surplus = weekly_surplus * 4
        
        weekly_gain_kg = weekly_surplus / 7700
        monthly_gain_kg = monthly_surplus / 7700
        
        if unit_select.lower() == "us units":
            weekly_gain = kg_to_lbs(weekly_gain_kg)
            monthly_gain = kg_to_lbs(monthly_gain_kg)
            unit_display = "lbs"
        else:
            weekly_gain = weekly_gain_kg
            monthly_gain = monthly_gain_kg
            unit_display = "kg"
        
        plans_data.append({
            "plan": plan_name,
            "calories": calories,
            "weekly_gain": weekly_gain,
            "monthly_gain": monthly_gain,
            "unit": unit_display
        })
        
        print(f"{plan_name} Plan ({surplus_pct}% surplus - Lean Bulk):")
        print(f"  Daily Calories: {calories:.0f}")
        print(f"  Projected Muscle Gain: {weekly_gain:.2f} {unit_display}/week, {monthly_gain:.2f} {unit_display}/month")
        print()

    # Plan selection
    if goal == "muscle":
        selected_plan = "Mild"
        print("Automatically selecting Mild plan for muscle building.\n")
    else:
        while True:
            plan_choice = input("Select your plan (Mild/Moderate/Aggressive): ").strip().capitalize()
            if plan_choice in ["Mild", "Moderate", "Aggressive"]:
                selected_plan = plan_choice
                break
            print("Invalid choice. Please enter Mild, Moderate, or Aggressive.")

    selected_plan_data = next((p for p in plans_data if p["plan"] == selected_plan), None)

    # Save to user_plans.xlsx
    plans_file = "user_plans.xlsx"

    if not os.path.exists(plans_file) or os.path.getsize(plans_file) == 0:
        plans_df = pd.DataFrame(columns=[
            "Email", "Goal", "Activity", "BMI", "BMI_Category", "BMR", "TDEE",
            "Protein_g", "Selected_Plan", "Daily_Calories", 
            "Weekly_Change", "Monthly_Change", "Unit"
        ])
    else:
        plans_df = pd.read_excel(plans_file)

    if goal == "loss":
        weekly_change = selected_plan_data['weekly_loss']
        monthly_change = selected_plan_data['monthly_loss']
    else:
        weekly_change = selected_plan_data['weekly_gain']
        monthly_change = selected_plan_data['monthly_gain']

    plan_record = pd.DataFrame([[
        email,
        goal,
        activity,
        result['BMI'],
        result['BMI_Category'],
        result['BMR'],
        result['TDEE'],
        result['Protein_g'],
        selected_plan,
        selected_plan_data['calories'],
        weekly_change,
        monthly_change,
        selected_plan_data['unit']
    ]], columns=plans_df.columns)

    plans_df = pd.concat([plans_df, plan_record], ignore_index=True)
    plans_df.to_excel(plans_file, index=False)

    print(f"\n✓ Your {selected_plan} plan has been saved!")
    print(f"\n--- Your Selected Plan Summary ---")
    print(f"Goal: {goal.upper()}")
    print(f"Plan: {selected_plan}")
    print(f"Daily Calorie Target: {selected_plan_data['calories']:.0f} calories")
    print(f"Daily Protein Target: {result['Protein_g']:.1f} g")

    if goal == "loss":
        print(f"Expected Fat Loss: {weekly_change:.2f} {selected_plan_data['unit']}/week")
        print(f"Expected Fat Loss: {monthly_change:.2f} {selected_plan_data['unit']}/month")
    else:
        print(f"Expected Weight Gain: {weekly_change:.2f} {selected_plan_data['unit']}/week")
        print(f"Expected Weight Gain: {monthly_change:.2f} {selected_plan_data['unit']}/month")

# ------------------ SIGN IN FUNCTION ------------------

def signin_user():
    df = pd.read_excel(users)
    
    print("\n" + "="*50)
    print("Sign In")
    print("="*50)

    while True:
        sign_in_email = input("Enter Email: ")
        if not emailid_valid(sign_in_email):
            continue
        if not emailid_exists(sign_in_email, df):
            print("Email not found. Please sign up first.")
            return None
        break

    while True:
        sign_in_password = input("Enter Password: ")
        actual_password = get_user_password(sign_in_email, df)

        if actual_password and sign_in_password.strip() == actual_password:
            print("\n✓ Login Successful!")
            return sign_in_email
        else:
            print("Invalid password. Try again.")

# ------------------ VIEW PLAN FUNCTION ------------------

def view_plan(email):
    plans_file = "user_plans.xlsx"
    
    if not os.path.exists(plans_file):
        print("\nNo plan found. Please set up your plan first.")
        return
    
    plans_df = pd.read_excel(plans_file)
    user_plan = plans_df[plans_df["Email"].str.strip().str.lower() == email.strip().lower()]

    if user_plan.empty:
        print("\nNo plan found. Please set up your plan first.")
        return
    
    user_plan = user_plan.iloc[-1]  # Get most recent plan
    
    print("\n" + "="*50)
    print("YOUR CURRENT FITNESS PLAN")
    print("="*50)
    print(f"Goal: {user_plan['Goal'].upper()}")
    print(f"Activity Level: {user_plan['Activity'].replace('_', ' ').title()}")
    print(f"Selected Plan: {user_plan['Selected_Plan']}")
    print(f"\nBody Metrics:")
    print(f"  BMI: {user_plan['BMI']:.2f} ({user_plan['BMI_Category']})")
    print(f"  BMR: {user_plan['BMR']:.0f} calories/day")
    print(f"  TDEE: {user_plan['TDEE']:.0f} calories/day")
    print(f"\nDaily Targets:")
    print(f"  Calories: {user_plan['Daily_Calories']:.0f}")
    print(f"  Protein: {user_plan['Protein_g']:.1f} g")
    print(f"\nProjected Results:")
    
    if user_plan['Goal'] == 'loss':
        print(f"  Weekly Fat Loss: {user_plan['Weekly_Change']:.2f} {user_plan['Unit']}")
        print(f"  Monthly Fat Loss: {user_plan['Monthly_Change']:.2f} {user_plan['Unit']}")
    else:
        print(f"  Weekly Weight Gain: {user_plan['Weekly_Change']:.2f} {user_plan['Unit']}")
        print(f"  Monthly Weight Gain: {user_plan['Monthly_Change']:.2f} {user_plan['Unit']}")
    
    print("="*50)

# ------------------ RESET PASSWORD FUNCTION ------------------

def reset_password(email):
    df = pd.read_excel(users)
    
    stored_sq = get_user_sq(email, df)
    if stored_sq is None:
        print("\nNo security question stored.")
        return
    
    fp_sq = input("\nEnter answer to security question: ").strip()

    if fp_sq.strip() == str(stored_sq).strip():
        while True:
            new_password = input("Enter new password: ").strip()
            if password_valid(new_password):
                change_password(email, new_password, df)
                break
            else:
                print("Try again.")
    else:
        print("Security answer incorrect.")

# ------------------ MAIN MENU ------------------

def main_menu(email):
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. View my fitness plan")
        print("2. Log a workout")
        print("3. Mark rest day")
        print("4. View recent workouts")
        print("5. View fitness streak")
        print("6. Reset password")
        print("7. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            view_plan(email)
        elif choice == "2":
            show_workout_menu(email)
        elif choice == "3":
            from streak import mark_rest_day
            mark_rest_day(email)
        elif choice == "4":
            from workout import show_recent_workouts
            show_recent_workouts(email)
        elif choice == "5":
            show_streak_menu(email)
        elif choice == "6":
            reset_password(email)
        elif choice == "7":
            print("\n✓ Thank you for using Fitness Tracker! Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1-7.")

# ------------------ MAIN PROGRAM ------------------

if __name__ == "__main__":
    print("="*50)
    print("WELCOME TO FITNESS TRACKER")
    print("="*50)
    
    while True:
        has_account = input("\nDo you have an account? (yes/no): ").strip().lower()
        
        if has_account == "no":
            email = signup_user()
            setup_plan(email)
            main_menu(email)
            break
        elif has_account == "yes":
            email = signin_user()
            if email:
                main_menu(email)
            break
        else:
            print("Please enter 'yes' or 'no'.")
