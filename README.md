## AIM: Automated Intelligence in Market Analysis

### Scope
**Domains:** Finance, IT, Data Science  
**Status:** Ongoing  
**Start Date:** December 2022  
**Current Phase:** Python application to collect live market data and save it to AWS S3 for further analysis and strategy deployment.  

### Phases Overview
1. **Research & Model Development**  
   - Comparative study of ML models and statistical approaches in stock price prediction (dissertation project, focused on tech giants: Google, Facebook, Netflix, and Apple).  
   - Published a related article in the IA Conference, London.

2. **Strategy Testing**  
   - Developed a trading strategy, combining statistical and machine learning insights.  
   - Conducted manual tests over 1 year and tracked results bi-monthly.

3. **Automated Trading & Performance Analysis**  
   - Tested the strategy with APIs from OANDA and Yahoo Finance.  
   - Notable challenges included differences in data aggregation (Yahoo Finance data vs. real-time data) and technical issues like network instability.

4. **Application Development and Deployment**  
   - Built a Flask app for live streaming market data from the Yahoo Finance API, storing it in an AWS S3 bucket.  
   - Backend AWS Lambda function for automated data aggregation across timeframes, saved to a second S3 bucket.

### Current Objectives
- **Strategy Deployment:** The app now supports live trading with custom-built strategies, which can be refined in a web-based interface.
- **Next Steps:** Expand app functionality for testing and developing additional strategies.

### Technical Setup
**Backend:** Python, Flask, AWS Lambda, Yahoo Finance API  
**Data Storage:** AWS S3 for raw and aggregated data  
**Analysis & Aggregation:** Automated Lambda functions to create consistent timeframes  

### Description
This project represents the culmination of my skills and expertise in finance, IT, and data science. My journey began by exploring machine learning’s impact on finance, where I tested multiple models and strategies with real data. After obtaining promising results, I shifted toward automating the entire process, with the aim of creating a deployable, user-friendly web application for ongoing strategy testing and development.
User Guide
Follow these steps to set up and test the AIM Flask app on your local environment. For more detailed instructions, refer to the [Setup Guide](SETUP.md).

### Basic Setup Instructions
1. Clone the Repository
2. Set Up AWS S3 Bucket Access
3. Create a Virtual Environment
4. Install Required Packages
5. Run the Flask App Using Waitress
6. Access the Control Panel
7. Start Live Data Streaming
8. Verify Data in S3
