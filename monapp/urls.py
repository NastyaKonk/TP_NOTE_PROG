from django.urls import path
from .import views

urlpatterns = [
   path("product/list",views.ProductListView.as_view(), name="product-list"),
   path("product/<pk>",views.ProductDetailView.as_view(), name="product-detail"),
   path("product/<pk>/update/",views.ProductUpdateView.as_view(), name="product-update"),
   path("product/add/", views.ProductCreateView.as_view(), name = "product-add"),
   path("product/<pk>/delete/",views.ProductDeleteView.as_view(), name="product-delete"),

   path("attribute/list",views.ProductAttributeListView.as_view(), name="attribute-list"),
   path("attribute/<pk>",views.ProductAttributeDetailView.as_view(), name="attribute-detail"),
   path("attribute/<pk>/update/",views.ProductAttributeUpdateView.as_view(), name="attribute-update"),
   path("attribute/add/", views.ProductAttributeCreateView.as_view(), name = "attribute-add"),
   path("attribute/<pk>/delete/",views.ProductAttributeDeleteView.as_view(), name="attribute-delete"),

   path("item/list",views.ProductItemListView.as_view(), name="item-list"),
   path("item/<pk>",views.ProductItemDetailView.as_view(), name="item-detail"),
   path("item/<pk>/update/",views.ProductItemUpdateView.as_view(), name="item-update"),
   path("item/add/", views.ProductItemCreateView.as_view(), name = "item-add"),
   path("item/<pk>/delete/",views.ProductItemDeleteView.as_view(), name="item-delete"),

   path("attribute/value/list",views.ProductAttributeValueListView.as_view(), name="attributeValue-list"),
   path("attribute/value/<pk>",views.ProductAttributeValueDetailView.as_view(), name="attributeValue-detail"),
   path("attribute/value/<pk>/update/",views.ProductAttributeValueUpdateView.as_view(), name="attributeValue-update"),
   path("attribute/value/add/", views.ProductAttributeValueCreateView.as_view(), name = "attributeValue-add"),
   path("attribute/value/<pk>/delete/",views.ProductAttributeValueDeleteView.as_view(), name="attributeValue-delete"),

   path("fournisseur/list",views.FournisseurListView.as_view(), name="fournisseur-list"),
   path("fournisseur/<pk>",views.FournisseurDetailView.as_view(), name="fournisseur-detail"),
   path("fournisseur/<pk>/update/",views.FournisseurUpdateView.as_view(), name="fournisseur-update"),
   path("fournisseur/add/", views.FournisseurCreate, name = "fournisseur-add"),
   path("fournisseur/<pk>/delete/",views.FournisseurDeleteView.as_view(), name="fournisseur-delete"),
   
   path("order/list",views.OrderListView.as_view(), name="order-list"),
   path("order/<pk>",views.OrderDetailView.as_view(), name="order-detail"),
   path("order/<pk>/update/",views.OrderUpdateView.as_view(), name="order-update"),
   path("order/add/", views.OrderCreateView.as_view(), name = "order-add"),
   path("order/<pk>/delete/",views.OrderDeleteView.as_view(), name="order-delete"),


   #path("home", views.home, name="home"),
   path("contact", views.ContactView, name="contact"),
   path("about", views.AboutView.as_view(), name="about"),
   path("home/<param>",views.accueil ,name='accueil'),
   path("home", views.HomeView.as_view(), name='home'),
   path('login/', views.ConnectView.as_view(), name='login'),
   path('register/', views.RegisterView.as_view(), name='register'),
   path('logout/', views.DisconnectView.as_view(), name='logout'),
   path('confirmation', views.ConfirmationView.as_view(), name='confirmation'),
] 
