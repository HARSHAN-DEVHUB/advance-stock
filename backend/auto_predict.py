import yfinance as yf
import pandas as pd
import joblib
import smtplib
from email.message import EmailMessage
import datetime
import os

# === Load model and scaler ===
model = joblib.load("./data/stock_prediction_model.pkl")
scaler = joblib.load("./data/scaler.pkl")

# === Fetch latest stock data ===
df = yf.download("INDUSINDBK.NS", period="10d", interval="1d")
df["Daily Change %"] = (df["Close"] - df["Open"]) / df["Open"] * 100
df["Volatility"] = (df["High"] - df["Low"]) / df["Open"] * 100
df["MA_5"] = df["Close"].rolling(window=5).mean()
df["MA_10"] = df["Close"].rolling(window=10).mean()
df.dropna(inplace=True)

# === Prepare input ===
latest = df.iloc[-1]
features = pd.DataFrame([[
    latest["Daily Change %"],
    latest["Volatility"],
    latest["MA_5"],
    latest["MA_10"]
]], columns=["Daily Change %", "Volatility", "MA_5", "MA_10"])

scaled = scaler.transform(features)
prediction = model.predict(scaled)[0]
trend = "HIGHER" if prediction == 1 else "LOWER"

# === Setup Email ===
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVER")

if not all([email_sender, email_password, email_receiver]):
    raise ValueError("EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECEIVER environment variables are required")


# === Format Email ===
today = datetime.datetime.now().strftime("%d %B %Y")
subject = f"📈 Stock Opening Prediction - {today}"
body = f"""Hey Harshan 👋,

🔮 Tomorrow’s stock opening trend is predicted to be: **{trend}**

This is an automated message from your Python predictor. 🚀
"""

msg = EmailMessage()
msg.set_content(body)
msg["Subject"] = subject
msg["From"] = email_sender
msg["To"] = email_receiver

# === Send Email ===
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)
    print(f"✅ Email sent to {email_receiver}")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
