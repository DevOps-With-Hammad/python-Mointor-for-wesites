import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage  # Import for image attachment
import os  # For accessing environment variables


def check_website_status(url):
    """Checks the website status and returns a dictionary with details."""
    try:
        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            return {"url": url, "status": "Up and Running", "error": None}
        else:
            error_message = f"Error (status code: {status_code})"
            # Provide more specific messages based on common error codes (examples):
            if status_code == 404:
                error_message += " - Page not found (404)"
            elif status_code == 500:
                error_message += " - Internal server error (500)"
            elif status_code == 502:
                error_message += " - Bad gateway (502)"
            return {"url": url, "status": "Down", "error": error_message}
    except requests.exceptions.RequestException as e:
        return {"url": url, "status": "Error", "error": str(e)}


def generate_report(website_data):
    """Generates a report listing only down websites and their statuses."""
    down_websites = [website for website in website_data if website["status"] != "Up and Running"]
    report = ""

    if not down_websites:
        # No websites are down, so don't send a report
        return None

    report += "**Down Websites:**\n"
    for website in down_websites:
        report += f"\n* {website['url']}: {website['status']}\n"
        if website["error"]:
            report += f"  Error details: {website['error']}\n"
    return report


def send_email_notification(report, recipient_list):
    """Sends a single email notification with the report (if there are down websites)."""

    # Access credentials securely from environment variables
    sender_email = os.environ.get("User_Email")
    sender_password = os.environ.get("User_Passwd")

    if not report:
        # No down websites, so skip sending the email
        return

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipient_list)  # Comma-separated recipient list
    message["Subject"] = "Website Monitoring Report (Down Websites)"

    body = f"""Hi Team,

This email provides a status report for down websites:

{report}

Thanks,
IT Department - DATA C
"""
    message.attach(MIMEText(body, "plain"))

    # Attach logo (optional)
    # You'll need to replace 'logo.png' with the actual logo file path
    with open("logo.png", "rb") as f:
        logo_attachment = MIMEImage(f.read(), _subtype="png")
        logo_attachment.add_header("Content-Disposition", "attachment; filename=logo.png")
        message.attach(logo_attachment)

    # Send email using a secure SMTP connection with TLS
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_list, message.as_string())
        print(f"Email sent successfully to {', '.join(recipient_list)} with website report.")


if __name__ == "__main__":
    websites = ['https://macro.care', 'https://datac.com', 'https://lovlov.com', 'https://pikaboom.gg/',
                'https://www.lightlogistics-eg.com' , 'https://uspa.datac.com', 'https://admin.pikaboom.gg',
                'https://dev.healsy.care', 'https://app.dolicense.com', 'https://admin.dolicense.com/']
    # Update with your website list
    recipient_list = ["hammad.ibrahim21994@gmail.com", "abonessma43@gmail.com"]  # Recipient list

    while True :
        website_data = []  # List to store website data
        for website in websites :
            website_data.append(check_website_status(website))

        report = generate_report(website_data)
        send_email_notification(report, recipient_list)

        # Sleep for 5 minutes (300 seconds)
        time.sleep(300)
