# 🏋️ Fitness Tracker

A comprehensive Python-based fitness tracking application with workout logging, BMR/TDEE calculations, personalized fitness plans, and weekly streak tracking.

## 🌟 Features

### User Management
- Secure signup with password validation
- Email-based authentication
- Security question for password recovery
- Support for both US Units (lbs, feet/inches) and Metric (kg, cm)
- All data stored in metric for consistency

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
- Results displayed in your preferred units

### Workout Logging
- Track workouts across 8 muscle groups:
  - Chest, Back, Legs, Shoulders, Arms, Core, Full Body, Cardio
- **Simple tracking:** Muscle group + Sets + Reps
- **Cardio tracking:** Duration-based (no sets/reps)
- View workout history
- Clean, focused workout entries

### Fitness Streak Tracking
- **Weekly goal-based streaks** - Set your weekly workout target (1-7 workouts/week)
- Track consecutive weeks meeting your goal
- View current and longest streaks
- Monitor weekly and monthly consistency
- Mark rest days for recovery tracking
- Motivational progress displays with emojis 🔥
- Automatic calculation from workout history

## 📋 Requirements
```bash
pip install pandas openpyxl
```

## 🚀 How to Use

### First Time Users:
```bash
python register.py
```
- Answer "no" when asked if you have an account
- Complete signup form (choose US Units or Metric)
- Select activity level (sedentary to extremely active)
- Choose fitness goal (weight loss/gain/muscle building)
- Pick your plan
- Access main menu automatically

### Returning Users:
```bash
python register.py
```
- Answer "yes" when asked if you have an account
- Sign in with email and password
- Access main menu

### Main Menu Options:
1. **View my fitness plan** - See your calorie/protein targets and projections
2. **Log a workout** - Quick muscle group + sets/reps entry
3. **Mark rest day** - Track recovery days
4. **View recent workouts** - See your last 5 workouts
5. **View fitness streak** - Check your weekly streak and consistency
6. **Reset password** - Change password with security question
7. **Exit** - Close the application

### Logging a Workout:
**For Strength Training:**
```
Select muscle group: Chest
Enter number of sets: 4
Enter number of reps: 10
✓ Workout logged successfully!
```

**For Cardio:**
```
Select muscle group: Cardio
Enter duration in minutes: 30
✓ Workout logged successfully!
```

### Viewing Streak Metrics:
```
🔥 YOUR FITNESS STREAK
==================================================

📊 Weekly Goal: 4 workouts
   This Week: 3/4 ⏳

🔥 Current Streak: 2 weeks 🔥🔥
🏆 Longest Streak: 5 weeks

📅 This Month:
   Consistency: 85.7%

💤 Rest Days Marked: 3

💪 One more workout to hit your goal this week!
==================================================
```

## 📁 Project Structure
```
fitness-tracker/
│
├── register.py           # Main application (signup, signin, menu)
├── calculate.py      # BMR, TDEE, protein calculations
├── workout_logger.py          # Workout logging system
├── streaks.py           # Fitness streak tracker
│
├── File.xlsx          # User profiles (auto-generated)
├── user_plans.xlsx    # Fitness plans (auto-generated)
├── workouts.xlsx      # Workout logs (auto-generated)
└── streaks.xlsx       # Streak data (auto-generated)
```

## 🔒 Data Storage

All user data is stored locally in Excel files:
- **File.xlsx**: User profiles with credentials (measurements stored in metric: kg, cm)
- **user_plans.xlsx**: Fitness goals, calorie/protein targets, and projections
- **workouts.xlsx**: Workout history (muscle group, sets, reps, duration)
- **streaks.xlsx**: Weekly workout goals and rest day tracking

⚠️ **Note**: Excel files are not tracked in git for privacy reasons.

## 🧮 Calculations

### BMR (Basal Metabolic Rate)
Uses the Mifflin-St Jeor equation:
- **Men**: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
- **Women**: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161

### TDEE Multipliers
- Sedentary (little/no exercise): BMR × 1.2
- Light activity (1-3 days/week): BMR × 1.375
- Moderate activity (3-5 days/week): BMR × 1.55
- Very active (6-7 days/week): BMR × 1.725
- Extremely active (physical job/2x daily): BMR × 1.9

### Protein Requirements
- Weight Loss: 1.8g per kg (preserves muscle during deficit)
- Weight Gain: 1.7g per kg (supports overall growth)
- Muscle Building: 2.0g per kg (optimal for hypertrophy)

### Weight Change Projections
Based on: 7,700 calories ≈ 1 kg of fat/weight
- Weekly change = (daily surplus/deficit × 7) ÷ 7,700 kg
- Monthly change = weekly change × 4

### Streak Calculation
- **Weekly Goal Streak**: Consecutive weeks where you meet your workout goal
- Example: Goal is 4 workouts/week
  - Week with 4+ workouts ✅ continues streak
  - Week with <4 workouts ❌ breaks streak
- **Monthly Consistency**: (Actual workouts ÷ Expected workouts) × 100%

## 👥 Contributors

This is a collaborative project. To contribute:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available for educational purposes.

## 🐛 Known Issues

None currently. Please report issues in the Issues tab.

## 🔮 Future Enhancements

- [ ] Progress tracking with charts
- [ ] Export workout data to CSV
- [ ] Progress photos

## 📧 Contact

For questions or suggestions, please open an issue in this repository.

---

**Happy Training! 💪**
