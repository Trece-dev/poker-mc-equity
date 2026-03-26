# 🃏 Monte Carlo Poker Equity Calculator

**Live App:** https://poker-mc-equity-egaxzpekfyvgphyzigzsun.streamlit.app/

An interactive web application built with Python that calculates real-time win probabilities (Equity) for Texas Hold'em poker hands. 

Instead of relying on massive combinatorial calculations, this engine leverages **Monte Carlo Simulations** to run thousands of randomized scenarios, delivering highly accurate results in milliseconds.

## 🎯 The Problem & The Solution

**The Problem:** Poker, much like financial trading, revolves around making decisions with incomplete information under strict time constraints. Calculating exact win probabilities on the fly requires processing too many variables.
**The Solution:** Applying the Law of Large Numbers. The app removes known cards from the deck and simulates the remaining board and opponent's cards thousands of times, outputting an actionable and clearly visualized metric (Equity).

## ⚙️ Tech Stack (Data Pipeline)

* **Language:** Python
* **Mathematical Engine / Data Parsing:** `Treys` (Ultra-fast hand evaluation).
* **User Interface (UI):** `Streamlit` (Transforming data scripts into interactive web apps).
* **Data Visualization:** `Plotly` (Interactive pie charts for outcome distribution).

## 🚀 Core Features

* **Visual UX:** Strict parsing engine that translates visual, user-friendly inputs (e.g., "Ace of Spades") into machine code, preventing user-side errors (Data Quality).
* **Logical Error Prevention:** The deck updates dynamically; cards selected in your hand disappear from the community board options to prevent duplication bugs.
* **Interactive Dashboard:** Instant visualization of Win, Loss, and Tie percentages through interactive charts.

## 🧠 Key Learnings
This project was designed to apply fundamental **Data Science** and **Programming** concepts:
1. Python loop logic and functions.
2. Data parsing and cleaning.
3. Applied statistics (Monte Carlo simulations).
4. Cloud deployment.

---
*Developed to explore the intersection of probability, data science, and product development.*
