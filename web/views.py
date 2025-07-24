from django.shortcuts import render, get_object_or_404,redirect

from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from .models import Category, Entry, MasterConfig, BankCard, BankAccount
from .forms import MasterLoginForm, EntryForm, CategoryForm, BankCardForm, BankAccountForm
from django.utils.decorators import method_decorator
from .decorators import master_required
from django.contrib import messages
from .models import MasterConfig
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def master_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_master_authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@csrf_exempt
def login_view(request):

    master_password_override = getattr(settings, "MASTER_PASSWORD_LOCAL", None)
    print(master_password_override)

    mc = MasterConfig.load()
    next_url = (
        request.POST.get('next')
        or request.GET.get('next')
        or reverse('entry_list')
    )

    if request.method == 'POST':
        entered = request.POST.get('password', '')

        if settings.DEBUG and master_password_override:
            if entered == master_password_override:
                request.session['is_master_authenticated'] = True
                return redirect(next_url)
        else:
            if mc.check_password(entered):
                request.session['is_master_authenticated'] = True
                return redirect(next_url)

        messages.error(request, 'Wrong master-password.')

    return render(request, 'web/login.html', {'next': next_url})

@csrf_exempt
def logout_view(request):
    request.session.flush()
    return redirect('login')

@csrf_exempt
@master_required
def index(request):
    return render(request, 'web/index.html')
    
@csrf_exempt
@master_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'web/category_list.html', {'categories': categories})
    
@csrf_exempt
@master_required
def category_form(request, pk=None):
    category = get_object_or_404(Category, pk=pk) if pk else None
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'web/category_form.html', {'form': form})
    
@csrf_exempt
@master_required
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.delete()
        return redirect('category_list')
    return render(request, 'web/category_confirm_delete.html', {'category': cat})
    
@csrf_exempt
@master_required
def entry_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        entries = Entry.objects.filter(category=category).order_by('-id')
    else:
        category = None
        entries = Entry.objects.select_related('category').all().order_by('-id')

    return render(request, 'web/entry_list.html', {
        'categories': categories,
        'entries': entries,
        'selected_category': category,
    })
@csrf_exempt
@master_required
def entry_form(request, pk=None):
    entry = get_object_or_404(Entry, pk=pk) if pk else None
    form = EntryForm(request.POST or None, instance=entry)
    if form.is_valid():
        form.save()
        return redirect('entry_list')
    return render(request, 'web/entry_form.html', {'form': form})
@csrf_exempt
@master_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
    return render(request, 'web/entry_confirm_delete.html', {'entry': entry})
    
@csrf_exempt
@master_required
def change_password(request):
    mc = MasterConfig.load()

    if request.method == 'POST':
        new1 = request.POST.get('new_password1', '')
        new2 = request.POST.get('new_password2', '')

        if new1 != new2:
            messages.error(request, 'Пароли не совпадают.')
        else:
            mc.set_password(new1)
            mc.save()
            messages.success(request, 'Мастер-пароль успешно изменён.')
            return redirect('category_list')

    return render(request, 'web/change_password.html')

@csrf_exempt
@master_required
def card_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        cards = BankCard.objects.filter(category=category).order_by('-id')
    else:
        category = None
        cards = BankCard.objects.select_related('category').all().order_by('-id')

    return render(request, 'web/card_list.html', {
        'categories': categories,
        'cards': cards,
        'selected_category': category,
    })

@csrf_exempt
@master_required
def card_form(request, pk=None):
    card = get_object_or_404(BankCard, pk=pk) if pk else None
    form = BankCardForm(request.POST or None, instance=card)
    if form.is_valid():
        form.save()
        return redirect('card_list')
    return render(request, 'web/card_form.html', {'form': form})

@csrf_exempt
@master_required
def card_delete(request, pk):
    card = get_object_or_404(BankCard, pk=pk)
    if request.method == 'POST':
        card.delete()
        return redirect('card_list')
    return render(request, 'web/card_confirm_delete.html', {'card': card})

@csrf_exempt
@master_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    entries = Entry.objects.filter(category=category).order_by('-id')
    cards = BankCard.objects.filter(category=category).order_by('-id')
    accounts = BankAccount.objects.filter(category=category).order_by('-id')

    return render(request, 'web/category_detail.html', {
        'selected_category': category,
        'entries': entries,
        'cards': cards,
        'accounts': accounts,
        'categories': Category.objects.all(),
    })

@csrf_exempt
@master_required
def account_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        accounts = BankAccount.objects.filter(category=category).order_by('-id')
    else:
        category = None
        accounts = BankAccount.objects.select_related('category').all().order_by('-id')

    return render(request, 'web/account_list.html', {
        'categories': categories,
        'accounts': accounts,
        'selected_category': category,
    })


@csrf_exempt
@master_required
def account_form(request, pk=None):
    account = get_object_or_404(BankAccount, pk=pk) if pk else None
    form = BankAccountForm(request.POST or None, instance=account)
    if form.is_valid():
        form.save()
        return redirect('account_list')
    return render(request, 'web/account_form.html', {'form': form})


@csrf_exempt
@master_required
def account_delete(request, pk):
    account = get_object_or_404(BankAccount, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('account_list')
    return render(request, 'web/account_confirm_delete.html', {'account': account})