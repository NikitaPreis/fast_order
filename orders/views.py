from django.http import HttpRequest
from django.shortcuts import redirect, render

from orders.forms import (OrderDeleteForm, OrderForm, OrderUpdateForm,
                          SalesRevenuesForm, SearchForm)
from orders.models import Order
from orders.paginator import get_page_obj
from services import orders as order_service


def orders_list(request: HttpRequest):
    """View for displaying orders."""
    template_name = 'orders/list.html'

    form = SearchForm()
    search_query = None

    if request.GET.get('search'):
        form = SearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search']
            orders = order_service.search_orders(search_query=search_query)
    else:
        orders = order_service.get_orders_with_items()

    page_obj = get_page_obj(
        queryset=orders, page_number=request.GET.get('page')
    )
    context = {
        'form': form,
        'query': search_query,
        'page_obj': page_obj
    }
    return render(request, template_name, context)


def create_order(request: HttpRequest):
    """View for creating orders."""
    template_name = 'orders/create.html'

    form = OrderForm(request.POST or None)

    context = {
        'form': form,
    }

    if form.is_valid():
        item_ids = form.data.getlist('items')
        total_price = order_service.get_orders_total_price(
            item_ids=item_ids
        )
        order: Order = form.save(commit=False)
        order.total_price = total_price
        context['total_price'] = total_price
        form.save(commit=True)

    return render(request, template_name, context)


def delete_order(request: HttpRequest, order_id: int):
    """View for deleting orders."""
    template_name = 'orders/delete.html'
    order = order_service.get_order_or_404(order_id=order_id)

    form = OrderDeleteForm(instance=order)

    context = {'form': form}

    if request.method == 'POST':
        order.delete()
        return redirect('orders:list')
    return render(request, template_name, context)


def update_order_status(request: HttpRequest, order_id: int):
    """View for updating orders."""
    template_name = 'orders/update_status.html'
    order = order_service.get_order_or_404(order_id=order_id)
    form = OrderUpdateForm(request.POST or None, instance=order)

    context = {'form': form}

    if form.is_valid():
        form.save()
    return render(request, template_name, context)


def sales_revenues(request: HttpRequest):
    """View for calculating revenue from sales of orders."""
    template_name = 'orders/sales_revenues.html'
    form = SalesRevenuesForm(request.POST or None)

    context = {'form': form}

    if form.is_valid():
        sales_revenue = order_service.get_sales_revenue(
            from_period=form.data['from_period'],
            to_period=form.data['to_period']
        )
        context['sales_revenue'] = sales_revenue
    return render(request, template_name, context=context)
