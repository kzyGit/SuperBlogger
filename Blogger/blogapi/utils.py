from django.core.mail import EmailMessage
from rest_framework.exceptions import (
    ValidationError, PermissionDenied, NotFound)


def send_email(subject, body, email):
    msg = EmailMessage(subject, body, 'kezzy.angiro@andela.com',
                       ['kezzyangiro@gmail.com'])
    msg.content_subtype = "html"
    return msg.send()


def CheckSlug(slug, model, item, action):
    if slug:
        try:
            return model.objects.get(slug=slug)
        except Exception:
            raise NotFound({'message': 'No {} with that slug'.format(item)})
    else:
        raise ValidationError({
            'message': 'Indicate the slug of the article to be {}'
            .format(action)})


def IsOwner(request, article):
    if (request.user == article.user):
        return True
    else:
        raise PermissionDenied(
            {'message': 'You have no article with that slug'})
