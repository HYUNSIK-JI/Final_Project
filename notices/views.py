from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoticesForm
from django.contrib.auth.decorators import login_required
from .models import Notices
from accounts.models import User
from datetime import date, datetime, timedelta

# from .models import Notices

# Create your views here.
def index(request):
    notices = Notices.objects.order_by("-pk")
    context = {"notices": notices}
    return render(request, "notices/index.html", context)


@login_required
def create(request):
    if request.user.is_superuser:
        form = NoticesForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            notices = form.save(commit=False)
            notices.user = request.user
            notices.save()
            return redirect("notices:index")
        return render(request, "notices/create.html", {"form": form})


@login_required
def detail(request, notices_pk):
    notices = Notices.objects.get(pk=notices_pk)
    context = {
        "notices": notices,
    }
    response = render(request, "notices/detail.html", context)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookievalue = request.COOKIES.get("hitnotices", "")

    if f"{notices_pk}" not in cookievalue:
        cookievalue += f"{notices_pk}"
        response.set_cookie(
            "hitnotices", value=cookievalue, max_age=max_age, httponly=True
        )
        notices.hits += 1
        notices.save()
    return response


@login_required
def delete(request, notices_pk):
    notices = Notices.objects.get(pk=notices_pk)
    notices.delete()
    return redirect("notices:index")


@login_required
def update(request, notices_pk):
    notices = Notices.objects.get(pk=notices_pk)
    if request.method == "POST":
        form = NoticesForm(request.POST, request.FILES, instance=notices)
        if form.is_valid():
            notices.check = True
            form.save()
            return redirect("notices:detail", notices.pk)
    else:
        form = NoticesForm(instance=notices)
    context = {"form": form}

    return render(request, "notices/update.html", context)
