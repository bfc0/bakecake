
def user_context(request):
    user = None
    if request.user.is_authenticated:
        user = {
            "phone_number": str(request.user.phone_number),
            "email": request.user.email if request.user.email else "",
            "name": request.user.name if request.user.name else "Customer",
        }

    return {"user": user}
