from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from docapp.models import TicketUser, TicketItem
from docapp.forms import TicketAddForm, LoginForm
from docapp.forms import CustomUserCreationForm


def index(request):
    user = TicketUser.objects.all()
    ticket = TicketItem.objects.all()
    return render(
        request, 'index.html', {"user_data": user, "ticket_data": ticket}
    )


def loginview(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data["username"],
                password=data["password"]
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, 'user_form.html', {'form': form})


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def user_details(request, id):
    user = TicketUser.objects.get(id=id)
    ticket_data = TicketItem.objects.all()
    return render(
        request, "user_details.html",
        {"user": user, "ticket_data": ticket_data}
    )


@login_required
def user_add_views(request):
    html = "user_form.html"
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tix_user = TicketUser.objects.create_user(
                username=data['username'],
                password=data['password1']
            )
            tix_user.save()
            return HttpResponseRedirect(reverse('homepage'))

    form = CustomUserCreationForm()

    return render(request, html, {'form': form})


# TICKETS

@login_required
def ticket_details(request, id):
    ticket = TicketItem.objects.get(id=id)
    return render(request, "ticket_details.html", {"ticket": ticket})


@login_required
def ticket_add_views(request):
    html = "ticket_form.html"

    # POST request
    if request.method == "POST":
        form = TicketAddForm(request.POST)
        if form.is_valid():                 # MUST DO before every POST request
            data = form.cleaned_data
            TicketItem.objects.create(
                title=data['title'],
                date=data['date'],
                time=data['time'],
                description=data['description'],
                filed_user=data['filed_user'],
                assigned_user=data['assigned_user'],
                completed_user=data['completed_user'],
                status=data['status']
            )
            return HttpResponseRedirect(reverse("homepage"))

    # GET request
    form = TicketAddForm()

    return render(request, html, {'form': form})


def ticket_edit_views(request, id):
    html = "ticket_form.html"
    ticket = TicketItem.objects.get(id=id)
    if request.method == "POST":
        form = TicketAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data['title']
            ticket.description = data['description']
            ticket.filed_user = data['filed_user']
            ticket.assigned_user = data['assigned_user']
            ticket.completed_user = data['completed_user']
            ticket.status = data['status']
            ticket.save()
            return HttpResponseRedirect(reverse('ticket_details', args=(id,)))

    form = TicketAddForm(initial={
        'title': ticket.title,
        'description': ticket.description,
        'filed_user': ticket.filed_user,
        'assigned_user': ticket.assigned_user,
        'completed_user': ticket.completed_user,
        'status': ticket.status
    })
    return render(request, html, {'form': form})


@login_required
def ticket_edit_invalid(request, id):
    ticket = TicketItem.objects.get(id=id)
    ticket.status = "INVALID"
    ticket.assigned_user = None
    ticket.completed_user = None

    ticket.save()

    return HttpResponseRedirect(request.GET.get("next", reverse()))


@login_required
def ticket_edit_finished(request, id):
    # grab current user to mark ticket finsihed_by {user}
    user = TicketUser.objects.get(username=request.user.username)
    ticket = TicketItem.objects.get(id=id)
    if ticket.status == "INVALID":
        ticket.assigned_user = user
    if ticket.assigned_user is None:
        ticket.assigned_user = user
    ticket.status = "FINSIHED"
    ticket.completed_user = ticket.assigned_user

    ticket.save()

    return HttpResponseRedirect(request.GET.get("next", reverse('ticket_details', args=(id,))))


@login_required
def ticket_edit_in_progress(request, id):
    ticket = TicketItem.objects.get(id=id)
    ticket.completed_user = None
    ticket.assigned_user = request.user
    ticket.status = "IN_PROGRESS"

    ticket.save()

    return HttpResponseRedirect(request.GET.get("next", reverse('ticket_details', args=(id,))))
