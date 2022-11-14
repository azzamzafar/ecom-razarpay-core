from django.shortcuts import redirect, render
from django.db.models import Sum
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.list import MultipleObjectMixin

from store.forms import ItemsForm
from store.models import Cart, Invoice, Item, Order, Product
from customers_auth.models import Customer

# Create your views here.
class ProductListView(MultipleObjectMixin, FormView):
    queryset = Product.objects.order_by("amount")
    object_list = queryset
    # context_object_name = "Product_list"
    paginate_by: int = 9
    template_name = "store/home.html"
    form_class = ItemsForm

    def get_success_url(self):
        if self.request.POST.get('action')=='item':
            return redirect(self.request.path_info)
        elif self.request.POST.get('action')=='order':
            return reverse('invoice')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ItemsForm()
        # context['order_formset']  = OrdersFormSet(prefix='order_form')
        return context

    def post(self, request, *args, **kwargs):
        form = ItemsForm(request.POST)
        print(request.user)
        # order_form = get_form(request,OrdersFormSet,"order_form")
        
        if form.is_valid():
            
            if form.cleaned_data.get("action") == "item":
                user = Customer.objects.filter(email = request.user)[0]
                cart_obj = Cart.objects.get_or_create(customer=user)
                product_id = form.cleaned_data.get("product")
                prod_obj = Product.objects.filter(id=product_id)[0]
                price = Product.objects.filter(id=product_id)[0].price
                item_obj = Item.objects.create(
                    product=prod_obj,
                    price=price,
                    Qty=form.cleaned_data.get("Qty"),
                    cart=cart_obj,
                )
                item_obj.save()
                return redirect('home')
            elif form.cleaned_data.get("action")== "order":
                user = Customer.objects.filter(email = request.user)[0]
                if request.user.is_anonymous:
                    redirect("login")
                elif not user.address1:
                    redirect("profile")
                invoice_obj = Invoice.objects.get_or_create(customer=user)
                product_id = form.cleaned_data.get("product")
                prod_obj = Product.objects.filter(id=product_id)[0]
                price = Product.objects.filter(id=product_id)[0].price
                order_obj = Order.objects.create(
                    product=prod_obj,
                    price=price,
                    Qty=form.cleaned_data.get("Qty"),
                    invoice=invoice_obj,
                )
                order_obj.save()

                redirect("/invoice/")


class ProductDetailView(DetailView):
    model = Product
    template_name: str = "store/product-detail.html"


def cartview(request):
    my_cart = Cart.objects.filter(customer=request.user)[0]
    my_items = Item.objects.filter(cart=my_cart)
    cart_total = (
        Item.objects.filter(cart=my_cart)
        .aggregate(Sum("order_amount"))
        .get("order_amount__sum")
    )
    cart_Qty = Item.objects.filter(cart=my_cart).aggregate(Sum("Qty")).get("Qty__sum")
    return render(
        request,
        "store/cart.html",
        {"total": cart_total, "Qty": cart_Qty, "my_items": my_items},
    )


# def cart(request):

#     return render(request)
# Function List View with Pagination
# def home(request):

#     Products = Product.objects.all()
#     # print(Products.values_list('name',flat=True)[0])
#     paginator = Paginator(Products,9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'store/home.html',{'page_obj':page_obj})
