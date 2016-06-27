from django.contrib.auth.decorators import user_passes_test
from itertools import chain

import logging

logger = logging.getLogger(__name__)

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            groups = list(chain.from_iterable(group_names))
            if bool(u.groups.filter(name__in=groups)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='/')


