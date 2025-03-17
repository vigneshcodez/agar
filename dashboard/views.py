from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from app.models import Business
from .forms import BusinessForm

def index(request):
    return render(request,'dashboard/pages/index.html')

def business_list(request):
    if request.user.is_anonymous:
        return redirect('login')
    elif request.user.is_superuser:
        business = Business.objects.all()
        paginator = Paginator(business, 4)  # 8 business per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'dashboard/pages/list_business.html', {'business': page_obj})
    else:
        business = Business.objects.filter(user=request.user)
        paginator = Paginator(business, 4)  # 8 business per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'dashboard/pages/list_business.html', {'business': page_obj})

def business_create(request):
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            business = form.save(commit=False)  # Don't save yet
            business.user = request.user  # Assign logged-in user
            business.save()  # Now save the object
            form.save()
            return redirect('business_list')
    else:
        form = BusinessForm()
    return render(request, 'dashboard/pages/create_business.html', {'form': form})

def business_edit(request, id):
    business = get_object_or_404(Business, id=id)
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business_list')
    else:
        form = BusinessForm(instance=business)
    return render(request, 'dashboard/pages/edit_business.html', {'form': form})

def delete_business(request, id):
    business = get_object_or_404(Business, id=id)
    if request.method == "POST":
        business.delete()
        return redirect('business_list')
    return redirect('business_list')
