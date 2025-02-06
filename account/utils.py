from django.core.mail import EmailMessage, BadHeaderError
import environ


env = environ.Env()
environ.Env.read_env()


def send_password_reset_email(data):
    try:
        email = EmailMessage(
            subject=data.get("subject"),
            body=data.get("body"),
            to=[data.get("to_email")],
            from_email=env("EMAIL_FROM"),
        )
        email.send()
    except BadHeaderError:
        pass
