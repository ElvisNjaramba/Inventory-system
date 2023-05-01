from django.shortcuts import render, get_object_or_404, redirect
from base.models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm
from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json

@login_required
# Create your views here.
def inventory_list(request):
    inventories = Inventory.objects.all()
    context = {
        "inventories":inventories
    }
    return render(request, 'base/inventory_list.html', context)

@login_required
def per_product(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory':inventory
    }
    return render(request, 'base/per_product.html', context)
@login_required
def add_product(request):
    if request.method == "POST":
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            new_inventory.sales = float(add_form.data['cost_per_item']) * float(add_form.data['quantity_sold'])
            new_inventory.save()
            return redirect("/inventory/")
        else:
            add_form = AddInventoryForm()
        return render(request, "base/inventory_add.html", {"form":add_form})

def dashboard(request):
    inventories = Inventory.objects.all()
    df = read_frame(inventories)
    
    sales_graph = df.groupby(by="last_sales_date", as_index= False, sort= False)['sales'].sum()
    sales_graph = px.line(sales_graph, x= sales_graph.last_sales_date, y= sales_graph.sales, title="Sales Trend")
    sales_graph = json.dumps(sales_graph, cls= plotly.utils.PlotlyJSONEncoder)
    
    best_perfoming_product = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    best_perfoming_product = px.bar(best_perfoming_product, x=best_perfoming_product.index, y=best_perfoming_product.quantity_sold, title="Best Performing Product")
    best_perfoming_product = json.dumps(best_perfoming_product, cls= plotly.utils.PlotlyJSONEncoder)
    
    product_in_stock = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    product_in_stock = px.pie(product_in_stock, names=product_in_stock.index, values=product_in_stock.quantity_in_stock, title="Best Performing Product")
    product_in_stock = json.dumps(product_in_stock, cls= plotly.utils.PlotlyJSONEncoder)

    
    
    context = {
        "sales_graph":sales_graph,
        "best_perfoming_product":best_perfoming_product,
        "product_in_stock":product_in_stock
    }
    return render(request, "base/dashboard.html", context)
    