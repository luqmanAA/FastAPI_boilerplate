from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from jinja2 import Environment, FileSystemLoader

from ..config import SENDGRID_API_KEY


def render_template(template_name, **context):
    template_loader = FileSystemLoader(searchpath="src/management/html_templates")
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)

    return template.render(context)


def send_email(to_email, subject, content, from_email=None):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content,
    )

    sg = SendGridAPIClient(SENDGRID_API_KEY)

    try:
        response = sg.send(message)
        print(f"Email sent. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


def send_forgot_password(email, activation_code, username, from_email=None):
    context = {"username": username, "activation_code": activation_code}
    content = render_template("forgot_password.html", **context)

    send_email(
        to_email=email,
        subject="Password Reset",
        content=content,
        from_email=from_email,
    )


def send_new_account(
    email: str, username: str, password: str, company_name: str, from_email: str = None
):
    context = {
        "username": username,
        "temporary_password": password,
        "YOUR_COMPANY_NAME": company_name,
    }
    content = render_template("account_creation.html", **context)
    send_email(
        to_email=email,
        subject="Account Created",
        content=content,
        from_email=from_email,
    )
