from typing import Any
from django.shortcuts import render, redirect
from .models import Product, ProductItem, ProductAttribute, ProductAttributeValue, PrixProduct, Fournisseur
from .forms import ContactUsForm, ProductForm, ProductItemForm, ProductAttributeForm, ProductAttributeValueForm, FournisseurForm
# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.forms import BaseModelForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

################      PRODUCT        ################

def ListProducts(request):
  prdcts = Product.objects.all()
  return render(request, 'monapp/list_products.html',{'prdcts': prdcts})

class ProductDetailView(DetailView):
  model = Product
  template_name = "monapp/detail_product.html"
  context_object_name = "product"

  def get_context_data(self, **kwargs):
    context = super(ProductDetailView, self).get_context_data(**kwargs)
    context['titremenu'] = "Détail produit"
    print(PrixProduct.objects.select_related('fournisseur_id').filter(product_id=self.object.id).values())
    context['referencementFournisseur'] = PrixProduct.objects.select_related('fournisseur_id').filter(product_id=self.object.id)
    return context

class ProductListView(ListView):
  model = Product
  template_name = "monapp/list_products.html"
  context_object_name = "products"

  def get_queryset(self ):
    # Surcouche pour filtrer les résultats en fonction de la recherche
    # Récupérer le terme de recherche depuis la requête GET
    query = self.request.GET.get('search')
    if query:
      # Filtre les produits par nom (insensible à la casse)
      return Product.objects.filter(name__icontains=query)
    
    # Si aucun terme de recherche, retourner tous les produits
    return Product.objects.all()

  def get_context_data(self, **kwargs):
    context = super(ProductListView, self).get_context_data(**kwargs)
    context['titremenu'] = "Liste des produits"
    return context

class ProductItemListView(ListView):
  model = Product
  template_name = "monapp/list_productItems.html"
  context_object_name = "products"

  def get_context_data(self, **kwargs):
    context = super(ProductListView, self).get_context_data(**kwargs)
    context['titremenu'] = "Liste des déclinaison Produit"
    return context

#class ContactView(TemplateView):
#  template_name = "monapp/home.html"

#  def get_context_data(self, **kwargs):
#    context = super(ContactView, self).get_context_data(**kwargs)
#    context['titreh1'] = "Contact us..."
#    return context
  
#  def post(self, request, **kwargs):
#    return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
  model = Product
  form_class = ProductForm
  template_name = "monapp/new_product.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    product = form.save()
    return redirect('product-detail', product.id)

def ProductUpdate(request, id):
  prdct = Product.objects.get(id=id)
  if request.method == 'POST':
    form = ProductForm(request.POST, instance=prdct)
  if form.is_valid():
    # mettre à jour le produit existant dans la base de données
    form.save()
    # rediriger vers la page détaillée du produit que nous venons de mettre à jour
    return redirect('product-detail', prdct.id)
  else:
    form = ProductForm(instance=prdct)
    return render(request,'monapp/product-update.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
  model = Product
  form_class = ProductForm
  template_name = "monapp/update_product.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    product = form.save()
    return redirect('product-detail', product.id)

def band_delete(request, id):
  prdct = Product.objects.get(id=id) # nécessaire pour GET et pour POST
  
  if request.method == 'POST':
    # supprimer le produit de la base de données
    prdct.delete()
    # rediriger vers la liste des produit
    return redirect('product-list')
  
  # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
  return render(request, 'monapp/prodcut-delete.html', {'object': prdct})

@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
  model = Product
  template_name = "monapp/delete_product.html"
  success_url = reverse_lazy('product-list')


################      PRODUCT ITEM       ################

@method_decorator(login_required, name='dispatch')
class ProductItemCreateView(CreateView):
  model = ProductItem
  form_class = ProductItemForm
  template_name = "monapp/new_productItem.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    product = form.save()
    return redirect('item-detail', product.id)

@method_decorator(login_required, name='dispatch')
class ProductItemDeleteView(DeleteView):
  model = ProductItem
  template_name = "monapp/delete_productitem.html"
  success_url = reverse_lazy('product-list')

class ProductItemListView(ListView):
  model = ProductItem
  template_name = "monapp/list_items.html"
  context_object_name = "productitems"

  def get_queryset(self ):
    # Surcouche pour filtrer les résultats en fonction de la recherche
    # Récupérer le terme de recherche depuis la requête GET
    query = self.request.GET.get('search')
    if query:
      # Filtre les produits par nom (insensible à la casse)
      return ProductItem.objects.filter(name__icontains=query)
    
    # Si aucun terme de recherche, retourner tous les produits
    return ProductItem.objects.all().select_related('product').prefetch_related('attributes')
  
  def get_context_data(self, **kwargs):
    context = super(ProductItemListView, self).get_context_data(**kwargs)
    context['titremenu'] = "Liste des déclinaisons"
    return context

class ProductItemDetailView(DetailView):
  model = ProductItem
  template_name = "monapp/detail_item.html"
  context_object_name = "productitem"
  def get_context_data(self, **kwargs):
    context = super(ProductItemDetailView, self).get_context_data(**kwargs)
    context['titremenu'] = "Détail déclinaison"
    # Récupérer les attributs associés à cette déclinaison
    context['attributes'] = self.object.attributes.all()
    return context
  
@method_decorator(login_required, name='dispatch')  
class ProductItemUpdateView(UpdateView):
  model = ProductItem
  form_class = ProductItemForm
  template_name = "monapp/update_item.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    product = form.save()
    return redirect('item-detail', product.id)


################      PRODUCT ATTRIBUTE       ################

@method_decorator(login_required, name='dispatch')
class ProductAttributeCreateView(CreateView):
  model = ProductAttribute
  form_class = ProductAttributeForm
  template_name = "monapp/new_productAttribute.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    product = form.save()
    return redirect('product-detail', product.id)
  

class ProductAttributeListView(ListView):
  model = ProductAttribute
  template_name = "monapp/list_attributes.html"
  context_object_name = "productattributes"

  def get_queryset(self ):
    # Surcouche pour filtrer les résultats en fonction de la recherche
    # Récupérer le terme de recherche depuis la requête GET
    query = self.request.GET.get('search')
    if query:
      # Filtre les produits par nom (insensible à la casse)
      return ProductAttribute.objects.filter(name__icontains=query)
    
    # Si aucun terme de recherche, retourner tous les produits
    return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')
  
  def get_context_data(self, **kwargs):
    context = super(ProductAttributeListView, self).get_context_data(**kwargs)
    context['titremenu'] = "Liste des attributs"
    return context


class ProductAttributeDetailView(DetailView):
  model = ProductAttribute
  template_name = "monapp/detail_attribute.html"
  context_object_name = "productattribute"

  def get_context_data(self, **kwargs):
    context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
    context['titremenu'] = "Détail attribut"
    context['values']=ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
    return context

@method_decorator(login_required, name='dispatch')
class ProductAttributeDeleteView(DeleteView):
  model = ProductAttribute
  template_name = "monapp/delete_attribute.html"
  success_url = reverse_lazy('attribute-list')

@method_decorator(login_required, name='dispatch')
class ProductAttributeUpdateView(UpdateView):
  model = ProductAttribute
  form_class = ProductAttributeForm
  template_name = "monapp/update_attribute.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    product = form.save()
    return redirect('attribute-detail', product.id)
  
################      PRODUCT ATTRIBUTE  VALUE     ################

@method_decorator(login_required, name='dispatch')
class ProductAttributeValueCreateView(CreateView):
  model = ProductAttributeValue
  form_class = ProductAttributeValueForm
  template_name = "monapp/new_productAttributeValue.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    product = form.save()
    return redirect('attributeValue-detail', product.id)
  

class ProductAttributeValueListView(ListView):
  model = ProductAttributeValue
  template_name = "monapp/list_attributeValues.html"
  context_object_name = "productattributevalues"

  def get_queryset(self ):
    # Surcouche pour filtrer les résultats en fonction de la recherche
    # Récupérer le terme de recherche depuis la requête GET
    query = self.request.GET.get('search')
    if query:
      # Filtre les produits par nom (insensible à la casse)
      return ProductAttributeValue.objects.filter(name__icontains=query)
    
    # Si aucun terme de recherche, retourner tous les produits
    return ProductAttributeValue.objects.all()
  
  def get_context_data(self, **kwargs):
    context = super(ProductAttributeValueListView, self).get_context_data(**kwargs)
    context['titremenu'] = "Liste des attribut values"
    return context


class ProductAttributeValueDetailView(DetailView):
  model = ProductAttributeValue
  template_name = "monapp/detail_attributeValues.html"
  context_object_name = "productattributevalue"

  def get_context_data(self, **kwargs):
    context = super(ProductAttributeValueDetailView, self).get_context_data(**kwargs)
    context['titremenu'] = "Détail attribut value"
    context['values']=ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
    return context

@method_decorator(login_required, name='dispatch')
class ProductAttributeValueDeleteView(DeleteView):
  model = ProductAttributeValue
  template_name = "monapp/delete_attributeValue.html"
  success_url = reverse_lazy('attributeValue-list')

@method_decorator(login_required, name='dispatch')
class ProductAttributeValueUpdateView(UpdateView):
  model = ProductAttributeValue
  form_class = ProductAttributeValueForm
  template_name = "monapp/update_attributeValue.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    product = form.save()
    return redirect('attributeValue-detail', product.id)


################      FOURNISSEUR        ################

class FournisseurDetailView(DetailView):
  model = Fournisseur
  template_name = "monapp/detail_fournisseur.html"
  context_object_name = "fournisseur"

  def get_context_data(self, **kwargs):
    context = super(FournisseurDetailView, self).get_context_data(**kwargs)
    context['titremenu'] = "Détail fournisseur"
    return context

class FournisseurListView(ListView):
  model = Fournisseur
  template_name = "monapp/list_fournisseurs.html"
  context_object_name = "fournisseurs"

  def get_queryset(self ):
    # Surcouche pour filtrer les résultats en fonction de la recherche
    # Récupérer le terme de recherche depuis la requête GET
    query = self.request.GET.get('search')
    if query:
      # Filtre les produits par nom (insensible à la casse)
      return Fournisseur.objects.filter(name__icontains=query)
    
    # Si aucun terme de recherche, retourner tous les produits
    return Fournisseur.objects.all()

  def get_context_data(self, **kwargs):
    context = super(FournisseurListView, self).get_context_data(**kwargs)
    context['titremenu'] = "Liste des fournisseurs"
    return context

@method_decorator(login_required, name='dispatch')
class FournisseurCreateView(CreateView):
  model = Fournisseur
  form_class = FournisseurForm
  template_name = "monapp/new_fournisseur.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    fournisseur = form.save()
    return redirect('fournisseur-detail', fournisseur.id)

def FournisseurCreate(request):
  if request.method == 'POST':
    form = FournisseurForm(request.POST)
    if form.is_valid():
      fournisseur = form.save()
      return redirect('fournisseur-detail', fournisseur.id)
  else:
    form = FournisseurForm()

  return render(request, "monapp/new_fournisseur.html", {'form': form})

@method_decorator(login_required, name='dispatch')
class FournisseurUpdateView(UpdateView):
  model = Fournisseur
  form_class = FournisseurForm
  template_name = "monapp/update_fournisseur.html"
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    fournisseur = form.save()
    return redirect('fournisseur-detail', fournisseur.id)

@method_decorator(login_required, name='dispatch')
class FournisseurDeleteView(DeleteView):
  model = Fournisseur
  template_name = "monapp/delete_fournisseur.html"
  success_url = reverse_lazy('fournisseur-list')


def ContactView(request):
  titreh1 = "Contact us !"

  if request.method=='POST':
    form = ContactUsForm(request.POST)
    if form.is_valid():
      send_mail(
      subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
      message=form.cleaned_data['message'],
      from_email=form.cleaned_data['email'],
      recipient_list=['admin@monprojet.com'],
      )
      return redirect('confirmation')
  else:
    form = ContactUsForm()

  return render(request, "monapp/contact.html",{'titreh1':titreh1, 'form':form})

def accueil(request,param):
  return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")

class HomeView(TemplateView):
  template_name = "monapp/home.html"
  def get_context_data(self, **kwargs):
    context = super(HomeView, self).get_context_data(**kwargs)
    context['titreh1'] = "Hello DJANGO"
    return context
  def post(self, request, **kwargs):
    return render(request, self.template_name)

class AboutView(TemplateView):
  template_name = "monapp/home.html"
  def get_context_data(self, **kwargs):
    context = super(AboutView, self).get_context_data(**kwargs)
    context['titreh1'] = "About us..."
    return context
  def post(self, request, **kwargs):
    return render(request, self.template_name)

class ConnectView(LoginView):
  template_name = 'monapp/login.html'

  def post(self, request, **kwargs):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
      login(request, user)
      return render(request, 'monapp/home.html')
    else:
      return render(request, 'monapp/register.html')

class RegisterView(TemplateView):
  template_name = 'monapp/register.html'

  def post(self, request, **kwargs):
    username = request.POST.get('username', False)
    mail = request.POST.get('mail', False)
    password = request.POST.get('password', False)
    user = User.objects.create_user(username, mail, password)
    user.save()
    if user is not None and user.is_active:
      return render(request, 'monapp/login.html')
    else:
      return render(request, 'monapp/register.html')

class DisconnectView(TemplateView):
  template_name = 'monapp/logout.html'
  def get(self, request, **kwargs):
    logout(request)
    return render(request, self.template_name)

class ConfirmationView(TemplateView):
  template_name = "monapp/home.html"
  def get_context_data(self, **kwargs):
    context = super(ConfirmationView, self).get_context_data(**kwargs)
    context['titreh1'] = "Your message has been sent successfully !"
    return context
  def post(self, request, **kwargs):
    return render(request, self.template_name)

def ProductCreate(request):
  if request.method == 'POST':
    form = ProductForm(request.POST)
    if form.is_valid():
      product = form.save()
      return redirect('product-detail', product.id)
  else:
    form = ProductForm()

  return render(request, "monapp/new_product.html", {'form': form})