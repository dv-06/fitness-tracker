# 🏋️ Fitness Tracker

A comprehensive Python-based fitness tracking application with workout logging, BMR/TDEE calculations, and personalized fitness plans.

##  Features

### User Management
- Secure signup with password validation
- Email-based authentication
- Security question for password recovery
- Support for both US Units (lbs, feet/inches) and Metric (kg, cm)

### Fitness Calculations
- **BMI** (Body Mass Index) calculation and categorization
- **BMR** (Basal Metabolic Rate) using Mifflin-St Jeor equation
- **TDEE** (Total Daily Energy Expenditure) based on 5 activity levels
- **Protein recommendations** tailored to fitness goals

### Personalized Plans
Three fitness goals with customized plans:

1. **Weight Loss**
   - Mild (10% deficit)
   - Moderate (20% deficit)
   - Aggressive (25% deficit)

2. **Weight Gain**
   - Mild (10% surplus)
   - Moderate (15% surplus)
   - Aggressive (20% surplus)

3. **Muscle Building**
   - Lean bulk approach (5% surplus)

Each plan includes:
- Daily calorie targets
- Daily protein targets
- Weekly and monthly weight change projections

### Workout Logging
- Track workouts across 8 muscle groups:
  - Chest, Back, Legs, Shoulders, Arms, Core, Full Body, Cardio
- Log sets, reps, and weight for strength training
- Track duration for cardio exercises
- View workout history
- Automatic unit conversion (weights displayed in your preferred units)

##  Requirements
```bash
pip install pandas openpyxl
```

##  How to Use

1. **First Time Users:**
```bash
   python signup.py
```
   - Answer "no" when asked if you have an account
   - Complete signup form
   - Select activity level
   - Choose fitness goal
   - Pick your plan

2. **Returning Users:**
```bash
   python signup.py
```
   - Answer "yes" when asked if you have an account
   - Sign in with email and password
   - Access main menu

3. **Main Menu Options:**
   - View your fitness plan
   - Log a workout
   - View recent workouts
   - Reset password
   - Exit

## 📁 Project Structure
```
fitness-tracker/
│
├── signup.py           # Main application (signup, signin, menu)
├── calculation.py      # BMR, TDEE, protein calculations
├── workout_logger.py          # Workout logging system
│
├── File.xlsx          # User profiles (auto-generated)
├── user_plans.xlsx    # Fitness plans (auto-generated)
└── workouts.xlsx      # Workout logs (auto-generated)
```

## 🔒 Data Storage

All user data is stored locally in Excel files:
- **File.xlsx**: User profiles with credentials (all measurements stored in metric)
- **user_plans.xlsx**: Fitness goals and calorie/protein targets
- **workouts.xlsx**: Workout history with exercises, sets, reps, weights

⚠️ **Note**: Excel files are not tracked in git for privacy reasons.

##  Calculations

### BMR (Basal Metabolic Rate)
Uses the Mifflin-St Jeor equation:
- **Men**: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
- **Women**: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161

### TDEE Multipliers
- Sedentary: BMR × 1.2
- Light activity: BMR × 1.375
- Moderate activity: BMR × 1.55
- Very active: BMR × 1.725
- Extremely active: BMR × 1.9

### Protein Requirements
- Weight Loss: 1.8g per kg (preserves muscle during deficit)
- Weight Gain: 1.7g per kg (supports overall growth)
- Muscle Building: 2.0g per kg (optimal for hypertrophy)

### Weight Change Projections
Based on: 7,700 calories ≈ 1 kg of fat/weight

##  Contributors

This is a collaborative project. To contribute:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available for educational purposes.

## 🐛 Known Issues

None currently. Please report issues in the Issues tab.

##  Future Enhancements

- [ ] Progress tracking with charts
- [ ] Export workout data
- [ ] Water intake tracking
      
##  Contact

For questions or suggestions, please open an issue in this repository.

---
