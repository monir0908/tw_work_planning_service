import logging
from typing import Union

from django.conf import settings

import jwt

from user.models import User

logger = logging.getLogger('django')


def authentication(token: str) -> Union[User, object]:
    try:
        decode = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, verify=True)
        try:
            user = User.objects.get(email__exact=decode['email'])
            if user.is_active:
                return user
            return
        except User.DoesNotExist:
            return
    except Exception as err:
        logger.error('token decode error', err)
        return
