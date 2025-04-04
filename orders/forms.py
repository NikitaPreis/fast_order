from django import forms
from django.forms import ModelForm

from orders.models import Item, Order
from orders.validators import validate_period_of_dates


class OrderForm(ModelForm):
    """Form for displaying a list of orders."""
    items = forms.ModelMultipleChoiceField(
        widget=forms.widgets.CheckboxSelectMultiple,
        queryset=Item.objects.all(),
        label='Позиции в заказе'
    )

    class Meta:
        model = Order
        fields = ('table_number', 'status', 'items')


class SearchForm(forms.Form):
    """Form for search."""
    search = forms.CharField()


class OrderCreateForm(forms.Form):
    """Form for creating orders."""
    table_number = forms.IntegerField()


class OrderUpdateForm(ModelForm):
    """Form for updating orders."""
    class Meta:
        model = Order
        fields = ('status',)


class OrderDeleteForm(forms.ModelForm):
    """Form for order deletion."""
    class Meta:
        model = Order
        fields = ('id', 'table_number', 'status')


class SalesRevenuesForm(forms.Form):
    """Form for calculating revenue from sales of orders."""
    from_period = forms.DateField(
        label='Период C',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    to_period = forms.DateField(
        label='Период ПО',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean(self):
        """Validate received dates."""
        cleaned_data = super().clean()
        validate_period_of_dates(
            from_date=cleaned_data.get('from_period'),
            to_date=cleaned_data.get('to_period')
        )
