def mlmodel_add_permission(request):
    if request.user:
        user = request.user
        if user.is_authenticated:
            if user.has_perm('app.add_mlmodel'):
                return True
    return False


def application_view_permission(request):
    if request.user:
        user = request.user
        if user.is_authenticated:
            if user.has_perm('app.view_application'):
                return True
    return False


def job_view_permission(request):
    if request.user:
        user = request.user
        if user.is_authenticated:
            if user.has_perm('app.view_job'):
                return True
    return False
