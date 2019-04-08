from django.core.mail import EmailMessage


def send_email(subject, body, email):
    msg = EmailMessage(subject, body, 'kezzy.angiro@andela.com',
                       ['kezzyangiro@gmail.com'])
    msg.content_subtype = "html"
    return msg.send()
