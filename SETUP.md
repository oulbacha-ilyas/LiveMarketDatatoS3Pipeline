Here’s a detailed **SETUP.md** to guide users through installing and running the AIM Flask app:

---

# Setup Guide for AIM Flask App

This guide will walk you through the steps to set up, configure, and run the AIM Flask app for testing. Ensure you have **Python 3** and **pip** installed on your system.

## 1. Clone the Repository
First, clone the project repository to your local environment:
```bash
git clone <repository-url>
cd <repository-name>
```

## 2. Set Up AWS S3 Bucket Access
The app uses an AWS S3 bucket to store live data from Yahoo Finance.

### If You Already Have an S3 Bucket:
Edit the environment variables to include your AWS credentials and S3 bucket information. If an `.env` file is provided, add the following details there, or edit directly in the application’s configuration file:
```plaintext
AWS_ACCESS_KEY_ID=<your-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_REGION=<your-region>
S3_BUCKET_NAME=<your-bucket-name>
```

### If You Don’t Have an S3 Bucket:
1. Log in to your **AWS Console** and navigate to **S3**.
2. Create a new S3 bucket (e.g., `marketdataaggregated`).
3. Enable programmatic access and obtain your **AWS Access Key ID** and **Secret Access Key**.
4. Set up the environment variables as shown above.

## 3. Create a Virtual Environment
It’s recommended to use a virtual environment to manage dependencies in isolation:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 4. Install Required Packages
Install all necessary dependencies specified in `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 5. Run the Flask App Using Waitress
The app uses **Waitress**, a production WSGI server, to run the application.

To start the Flask app, run:
```bash
python run_waitress.py
```

This command will start the server on `http://127.0.0.1:8080` (or another port if specified in `run_waitress.py`).

## 6. Access the Control Panel
- Open a web browser and go to `http://127.0.0.1:8080`.
- You should see the **Streaming Agent Control Panel** interface.

## 7. Start Live Data Streaming
Within the Control Panel, you can interact with the data streaming and storage functions:

- **Start Streaming**: Begins fetching live market data from Yahoo Finance.
- **Stop Streaming**: Stops the data stream.
- **Select Timeframe**: Choose a timeframe for data aggregation (e.g., `1min`, `1mls`).
- **Save to Bucket**: Saves the streamed data to your specified S3 bucket.
- **Current State**: Check the current state of the data in the bucket.
- **Reset DataFrame**: Clears data to reset the session.

## 8. Verify Data in S3
After starting the streaming:
- Log in to your **AWS S3 Console**.
- Open your S3 bucket (e.g., `marketdataaggregated`) to confirm data files are being saved as expected.
- Aggregated data will appear according to the configured timeframes, managed by the AWS Lambda function.
