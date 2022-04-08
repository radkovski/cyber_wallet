import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from cyber_wallet_application.forms import OperationForm, ReportForm, NoteForm, LocalConfigurationForm, NewUserForm
from cyber_wallet_application.models import Operation, Report, Note, LocalConfiguration

LOGIN_URL = "/accounts/login/"


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def index(request):
    """
    Zwraca główną stronę aplikacji
    @param request: Żądanie przekazywane przez Django
    @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    operations = (Operation.objects
                      .filter(user=request.user)
                      .order_by("-execution_moment")[:10])
    notes = Note.objects.filter(user=request.user)
    today = datetime.date.today()
    week_begin = today - datetime.timedelta(today.weekday())
    week_end = week_begin + datetime.timedelta(7)
    weekly_operations = (Operation.objects
                         .filter(user=request.user)
                         .filter(execution_moment__range=[week_begin, week_end]))
    weekly_report = [0, 0, 0, 0, 0, 0, 0]
    for operation in weekly_operations:
        weekly_report[operation.execution_moment.date().weekday()] += operation.amount
    return render(request, "index.htm", {
        "operations": operations,
        "weekly_report": weekly_report,
        "notes": notes
    })


####### OPERATION

@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET", "POST"])
def create_operation(request):
    """
        Zwraca stronę z formularzem tworzenia operacji
        @param request: Żądanie przekazywane przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    if request.method == "GET":
        has_object_added = False
    else:
        form = OperationForm(request.POST)
        if form.is_valid():
            Operation.objects.create(
                user=request.user,
                execution_moment=form.data["execution_moment"],
                accounting_moment=form.data["execution_moment"],
                description=form.data["description"],
                amount=form.data["amount"]
            )
            has_object_added = True
    form = OperationForm()
    return render(request, "create_operation.htm", {
        "form": form,
        "has_object_added": has_object_added
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def read_operations(request):
    """
        Zwraca stronę z operacjami (tabela)
        @param request: Żądanie przekazywane przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    operations = (Operation.objects
                  .filter(user=request.user)
                  .order_by("-execution_moment"))
    return render(request, "read_operations.htm", {
        "operations": operations
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET", "POST"])
def update_operation(request, pk):
    """
        Zwraca stronę z formularzem edycji operacji
        @param request: Żądanie przekazywane przez Django
        @param pk: Klucz przekazywany przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    operation = get_object_or_404(Operation, pk=pk, user=request.user)
    if request.method == "GET":
        has_object_updated = False
        form = OperationForm(instance=operation)
    else:
        form = OperationForm(request.POST)
        if form.is_valid():
            operation.execution_moment = form.data["execution_moment"]
            operation.description = form.data["description"]
            operation.amount = form.data["amount"]
            operation.save()
            has_object_updated = True
    return render(request, "update_operation.htm", {
        "form": form,
        "has_object_updated": has_object_updated
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def delete_operation(request, pk):
    """
        Zwraca stronę umożliwiającą usunięcie operacji
        @param request: Żądanie przekazywane przez Django
        @param pk: Klucz przekazywany przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    operation = get_object_or_404(Operation, pk=pk, user=request.user)
    operation.delete()
    return render(request, "delete_operation.htm")


####### REPORT #######

@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET", "POST"])
def create_report(request):
    """
        Zwraca stronę z formularzem tworzenia raportu
        @param request: Żądanie przekazywane przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    if request.method == "GET":
        has_object_added = False
    else:
        form = ReportForm(request.POST)
        if form.is_valid():
            Report.objects.create(
                user=request.user,
                from_moment=form.data["from_moment"],
                to_moment=form.data["to_moment"]
            )
            has_object_added = True
    form = ReportForm()
    return render(request, "create_report.htm", {
        "form": form,
        "has_object_added": has_object_added
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def read_report(request, pk):
    """
        Zwraca stronę z wykresem pojedynczego raportu
        @param request: Żądanie przekazywane przez Django
        @param pk: Klucz przekazywany przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    report = get_object_or_404(Report, pk=pk, user=request.user)
    operations = (Operation.objects.values("execution_moment__date")
                  .filter(user=request.user) # po userze filtruje raport, żeby się wyświtlały tylko danego usera.
                  .order_by("execution_moment__date")
                  .annotate(total=Sum("amount")))
    return render(request, "read_report.htm", {
        "report": report,
        "operations": operations
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def read_reports(request):
    """
        Zwraca stronę z raportami (tabela)
        @param request: Żądanie przekazywane przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    reports = (Report.objects
               .filter(user=request.user)
               .order_by("-from_moment"))
    return render(request, "read_reports.htm", {
        "reports": reports
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def delete_report(request, pk):
    """
        Zwraca stronę pozwalającą usunąć raport
        @param request: Żądanie przekazywane przez Django
        @param pk: Klucz przekazywany przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    report = get_object_or_404(Report, pk=pk, user=request.user)
    report.delete()
    return render(request, "delete_report.htm")


####### NOTE #######

@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET", "POST"])
def create_note(request):
    """
        Zwraca stronę z formularzem tworzenia notatki
        @param request: Żądanie przekazywane przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    if request.method == "GET":
        has_object_added = False
    else:
        form = NoteForm(request.POST)
        if form.is_valid():
            Note.objects.create(
                user=request.user,
                from_moment=form.data["from_moment"],
                to_moment=form.data["to_moment"],
                text=form.data["text"]
            )
            has_object_added = True
    form = NoteForm()
    return render(request, "create_note.htm", {
        "form": form,
        "has_object_added": has_object_added
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET", "POST"])
def update_note(request, pk):
    """
        Zwraca stronę z formularzem edycji notatki
        @param request: Żądanie przekazywane przez Django
        @param pk: Klucz przekazywany przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "GET":
        has_object_updated = False
        form = NoteForm(instance=note)
    else:
        form = NoteForm(request.POST)
        if form.is_valid():
            note.from_moment = form.data["from_moment"]
            note.to_moment = form.data["to_moment"]
            note.text = form.data["text"]
            note.save()
            has_object_updated = True
    return render(request, "update_note.htm", {
        "form": form,
        "has_object_updated": has_object_updated
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def read_notes(request):
    """
        Zwraca stronę z notatkami (tabela)
        @param request: Żądanie przekazywane przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    notes = (Note.objects
             .filter(user=request.user)
             .order_by("-from_moment"))
    return render(request, "read_notes.htm", {
        "notes": notes
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def delete_note(request, pk):
    """
        Zwraca stronę pozwalającą usunąć notatkę
        @param request: Żądanie przekazywane przez Django
        @param pk: Klucz przekazywany przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    return render(request, "delete_note.htm")


####### OTHER #######

@require_http_methods(["GET"])
def info(request):
    """
        Zwraca stronę informacyjną
        @param request: Żądanie przekazywane przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    return render(request, "info.htm")


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET"])
def settings(request):
    """
        Zwraca stronę z ustawieniami
        @param request: Żądanie przekazywane przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    configurations = (LocalConfiguration.objects
                      .filter(user=request.user)
                      .order_by("key"))
    return render(request, "settings.htm", {
        "configurations": configurations
    })


@login_required(login_url=LOGIN_URL)
@require_http_methods(["GET", "POST"])
def update_configuration(request, pk):
    """
        Zwraca stronę pozwalającą zmienić ustawienia
        @param request: Żądanie przekazywane przez Django
        @param pk: Klucz przekazywany przez Django
        @return: Odpowiedź w formie odpowiedniego kodu HTML
    """
    configuration = get_object_or_404(LocalConfiguration, pk=pk, user=request.user)
    has_object_updated = False
    if request.method == "GET":
        form = LocalConfigurationForm(instance=configuration)
    else:
        form = LocalConfigurationForm(request.POST)
        if form.is_valid():
            configuration.value = form.data["value"]
            configuration.save()
            has_object_updated = True
    return render(request, "update_note.htm", {
        "form": form,
        "has_object_updated": has_object_updated
    })


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            LocalConfiguration.objects.create(
                user=user,
                key="THEME",
                value="Light"
            )
            login(request, user)
            messages.success(request, "Zarejestrowano poprawnie.")
            return redirect("/")
        messages.error(request, "Rejestracja nie powiodła się.")
    form = NewUserForm()
    return render(request, "register.htm", {
        "register_form": form
    })
