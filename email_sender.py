import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

def send_email(videos):
    msg = EmailMessage()

    date_str = datetime.now().strftime("%b %d, %Y")

    msg['Subject'] = f'Your Daily YouTube Digest - {date_str}'

    msg['From'] = os.environ.get('FROM_EMAIL')
    msg['To'] = os.environ.get('TO_EMAIL')

    if not videos:
        html_content = """
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>No new videos today!</h2>
                <p>Catch up on your backlog or enjoy the quiet.</p>
            </body>
        </html>
        """
    else:
        html_content = '<html><body style="font-family: Arial, sans-serif; padding: 20px;">'
        html_content += '<h2>Your Latest YouTube Videos</h2>'
        
        for v in videos:
            html_content += f"""
            <div style="margin-bottom: 30px; display: flex; align-items: flex-start;">
                <a href="{v['link']}">
                    <img src="{v['thumbnail']}" width="200" style="border-radius: 8px; margin-right: 15px;" alt="thumbnail">
                </a>
                <div>
                    <h3 style="margin: 0 0 5px 0;"><a href="{v['link']}" style="color: #000; text-decoration: none;">{v['title']}</a></h3>
                    <p style="margin: 0; color: #555;"><strong>{v['author']}</strong></p>
                </div>
            </div>
            """
        html_content += '</body></html>'

    msg.set_content("Please enable HTML to view this email.")
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP(os.environ.get('SMTP_SERVER'), int(os.environ.get('SMTP_PORT', 587))) as server:
        server.starttls()
        server.login(os.environ.get('SMTP_USERNAME'), os.environ.get('SMTP_PASSWORD'))
        server.send_message(msg)
