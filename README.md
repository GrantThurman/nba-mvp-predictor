# 🏀 NBA MVP Prediction Model

## 📖 Overview
This project predicts NBA MVP voting share based on player performance data from 2000–2025.
It combines traditional box score stats, team success, and some engineered stats

## 🎯 Objective
To use machine learning (Random Forest regression) to model the relationship between season performance and MVP voting results — and explore what factors most influence MVP outcomes.

## 🧩 Data Sources
	•	🏀 Basketball Reference￼: MVP voting & advanced player stats
	•	🏀 NBA API￼: Box score and team statistics

## 📊 Features
	•	Basic: Points, assists, rebounds, steals, blocks, and shooting percentages
	•	Team context: Player & team win percentage
	•	Engineered: Per-minute stats, efficiency metrics

## ⚙️ Model
	•	Algorithm: Random Forest Regressor
	•	Target: MVP vote share (`MVP_PCT_SHARE`)
	•	Result: R² = 0.83 (strong fit; model explains ~83% of MVP voting variation)

## 🧠 Insights
	•	Team success and all-around efficiency are major MVP predictors.
	•	Efficiency, team win percentage, and points scored have the strongest feature importances.
	•	Players on losing teams rarely receive MVP votes, even with elite stats.

## 🚀 Future Work
	•	Add advanced metrics (PER, WS, BPM, VORP)
	•	Build a Streamlit dashboard for live MVP race predictions
	•	Explore time-series trends in MVP criteria

## 🧑‍💻 Author
Grant Thurman
