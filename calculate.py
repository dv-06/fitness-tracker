def calculate_bmr(weight_kg, height_cm, age, sex):
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
    """
    if sex.lower() in ['male', 'm', 'man']:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:  # female
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    return bmr


def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure based on activity level
    """
    activity_multipliers = {
        'sedentary': 1.2,           # Little or no exercise
        'light': 1.375,             # Exercise 1-3 days/week
        'moderate': 1.55,           # Exercise 3-5 days/week
        'very_active': 1.725,       # Exercise 6-7 days/week
        'extremely_active': 1.9     # Physical job or training twice per day
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
    tdee = bmr * multiplier
    
    return tdee


def calculate_protein(weight_kg, goal):
    """
    Calculate daily protein requirement based on goal
    
    Scientific recommendations:
    - Weight Loss: 1.6-2.0g per kg (higher protein preserves muscle during deficit)
    - Weight Gain: 1.6-1.8g per kg (supports muscle growth)
    - Muscle Building: 1.8-2.2g per kg (optimal for hypertrophy)
    """
    protein_ranges = {
        'loss': 1.8,      # Higher end to preserve muscle during cut
        'gain': 1.7,      # Moderate for overall weight gain
        'muscle': 2.0     # Higher for optimal muscle building
    }
    
    protein_per_kg = protein_ranges.get(goal, 1.6)
    protein_g = weight_kg * protein_per_kg
    
    return protein_g


def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI and category
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return bmi, category


def record_calculation(email, weight_val, weight_unit, height_val, height_unit, 
                       age, sex, activity, goal):
    """
    Main function to calculate all metrics
    
    Parameters:
    - email: user email
    - weight_val: weight value
    - weight_unit: 'kg' or 'lbs'
    - height_val: height value
    - height_unit: 'cm' or 'inches'
    - age: age in years
    - sex: 'male' or 'female'
    - activity: activity level (sedentary, light, moderate, very_active, extremely_active)
    - goal: fitness goal ('loss', 'gain', 'muscle')
    """
    
    # Convert to metric if needed
    if weight_unit.lower() == 'lbs':
        weight_kg = weight_val * 0.453592
    else:
        weight_kg = weight_val
    
    if height_unit.lower() == 'inches':
        height_cm = height_val * 2.54
    else:
        height_cm = height_val
    
    # Calculate BMI
    bmi, bmi_category = calculate_bmi(weight_kg, height_cm)
    
    # Calculate BMR
    bmr = calculate_bmr(weight_kg, height_cm, age, sex)
    
    # Calculate TDEE
    tdee = calculate_tdee(bmr, activity)
    
    # Calculate Protein
    protein_g = calculate_protein(weight_kg, goal)
    
    # Return all calculations
    result = {
        'email': email,
        'BMI': bmi,
        'BMI_Category': bmi_category,
        'BMR': bmr,
        'TDEE': tdee,
        'Protein_g': protein_g
    }
    
    return result