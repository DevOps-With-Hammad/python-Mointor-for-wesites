import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.mime.image
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


def send_email_notification(website_data, recipient_list):
    """Sends email notifications with website status details and an image."""

    # Access credentials securely from environment variables
    sender_email = os.environ.get('User_Email')
    sender_password = os.environ.get('User_Passwd')

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipient_list)  # Comma-separated recipient list
    message["Subject"] = f"Website Status Report: {website_data['url']}"

    # Content with website status and action if needed
    body = f"""Hi Team,

This email provides a status update for the website: {website_data['url']}.

Current Status: {website_data['status']}

"""
    if website_data["status"] != "Up and Running":
        body += f"""Error Details: {website_data['error']} 

This error message can help diagnose the specific issue with the website.

Action Required: Please investigate and resolve the website issue.

"""

    body += """Thanks,
IT Department - DATA C
"""
    message.attach(MIMEText(body, "plain"))

    # Attach logo (optional)
    # You'll need to replace 'logo.png' with the actual logo file path
    with open("logo.png", "rb") as f :  # Open the logo in binary mode
        logo_attachment = email.mime.image.MIMEImage(f.read(), _subtype="png")
        logo_attachment.add_header("Content-Disposition", "attachment; filename=logo.png")
        message.attach(logo_attachment)

    # Send email using a secure SMTP connection with TLS
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_list, message.as_string())
        print(f"Email sent successfully to {', '.join(recipient_list)} for {website_data['url']}.")


if __name__ == "__main__":
    websites = ['https://macro.care', 'https://datac.com', 'https://lovlov.com', 'https://pikaboom.gg/',
                'https://www.lightlogistics-eg.com' , 'https://uspa.datac.com', 'https://admin.pikaboom.gg',
                'https://dev.healsy.care', 'https://app.dolicense.com', 'https://admin.dolicense.com/']  # Update with your website list
    recipient_list = ["hammad.ibrahim21994@gmail.com", "abonessma43@gmail.com", ""]  # Recipient list

    for website in websites:
        website_data = check_website_status(website)
        send_email_notification(website_data, recipient_list)
