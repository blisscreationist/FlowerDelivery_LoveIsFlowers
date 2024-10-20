# reviews/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from catalog.models import Product
from .forms import ReviewForm
from django.contrib import messages


def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        # Создание отзыва
        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            review_text=review_text
        )

        messages.success(request, 'Ваш отзыв был успешно оставлен!')
        return redirect('product_list', category_id=product.category.id)

    messages.error(request, 'Не удалось оставить отзыв. Попробуйте снова.')
    return redirect('product_list', category_id=product.category.id)