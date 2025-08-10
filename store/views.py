from django.shortcuts import render

from . models import Category, Product, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.db import models


def store(request):

    all_products = Product.objects.all()

    context = {'my_products':all_products}

    return render(request, 'store/store.html', context)



def categories(request):

    all_categories = Category.objects.all()

    return {'all_categories': all_categories}



def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)


    return render(request, 'store/list-category.html', {'category':category, 'products':products})



def search(request):

    if request.method == 'POST':

        searched = request.POST['searched']

        # Enhanced search: title, brand, description
        products = Product.objects.filter(
            models.Q(title__icontains=searched) |
            models.Q(brand__icontains=searched) |
            models.Q(description__icontains=searched)
        )

        return render(request, 'store/search.html', {'searched':searched, 'products':products})

    else:

        return render(request, 'store/search.html', {})


@login_required
def product_info(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)
    reviews = product.reviews.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            rating = int(request.POST.get('rating', 0))
            review_text = request.POST.get('review', '').strip()
            if 1 <= rating <= 5 and review_text:
                Review.objects.create(product=product, user=request.user, rating=rating, review=review_text)
                messages.success(request, 'Your review has been submitted!')
            else:
                messages.error(request, 'Please provide a valid rating and review text.')
        else:
            messages.error(request, 'You must be logged in to submit a review.')
    context = {'product': product, 'reviews': reviews}

    return render(request, 'store/product-info.html', context)







