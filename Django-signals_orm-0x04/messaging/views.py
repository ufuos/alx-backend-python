
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect
from django.http import HttpResponse

User = get_user_model()

@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their own account.
    """
    user = request.user
    user.delete()   # This will trigger post_delete signal
    logout(request)
    return HttpResponse("Your account and all related data have been deleted successfully.")
