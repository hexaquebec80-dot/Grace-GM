from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import logout_user
from django.views.generic import RedirectView

urlpatterns = [

    # =========================================================
    # ACCUEIL ET PRODUIT
    # =========================================================

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "product/<int:id>/",
        views.product_detail,
        name="product_detail",
    ),

    path(
        "search/",
        views.search,
        name="search",
    ),


    # =========================================================
    # CONNEXION ET INSCRIPTION
    # =========================================================

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "logout/",
        logout_user,
        name="logout",
    ),


    # =========================================================
    # RÉINITIALISATION DU MOT DE PASSE
    # =========================================================

    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),

    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),


    # =========================================================
    # PANIER PRINCIPAL
    # =========================================================

    path(
        "cart/",
        views.cart,
        name="cart",
    ),

    path(
    "add-to-cart/<int:product_id>/",
    views.add_to_cart,
    name="add_to_cart",
    ),

    

    path(
        "cart/remove/<int:id>/",
        views.remove_quantity,
        name="remove_quantity",
    ),

    path(
        "remove-cart-item/<int:id>/",
        views.remove_cart_item,
        name="remove_cart_item",
    ),


    # =========================================================
    # ANCIEN SYSTÈME DE PANIER
    # NOMS DIFFÉRENTS POUR ÉVITER LES CONFLITS
    # =========================================================

    path(
        "panier/",
        views.cart,
        name="panier",
    ),

    path(
        "panier/ajouter/<int:product_id>/",
        views.add_to_cart,
        name="panier_add",
    ),

    path(
        "panier/modifier/<int:product_id>/",
        views.update_cart,
        name="update_cart",
    ),

    path(
        "panier/supprimer/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),


    # =========================================================
    # CHECKOUT ET STRIPE
    # =========================================================

    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),

    path(
        "stripe/success/",
        views.stripe_success,
        name="stripe_success",
    ),

    path(
    "stripe/cancel/",
    RedirectView.as_view(pattern_name="cart", permanent=False),
    name="stripe_cancel",
    ),


    # =========================================================
    # MODE
    # =========================================================

    path(
        "mode/",
        views.mode_page,
        name="mode",
    ),

    path(
        "mode/<str:type>/",
        views.mode_page,
        name="mode_type",
    ),

    path(
        "add-mode-to-cart/<int:id>/",
        views.add_mode_to_cart,
        name="add_mode_to_cart",
    ),


    # =========================================================
    # BEAUTÉ
    # =========================================================

    path(
        "beaute/",
        views.beaute_page,
        name="beaute",
    ),

    path(
        "beaute/<str:type>/",
        views.beaute_type,
        name="beaute_type",
    ),

    path(
        "add-beaute-to-cart/<int:product_id>/",
        views.add_beaute_to_cart,
        name="add_beaute_to_cart",
    ),


    # =========================================================
    # HYGIÈNE
    # =========================================================

    path(
        "hygiene/",
        views.hygiene_page,
        name="hygiene",
    ),

    path(
        "hygiene/<str:type_name>/",
        views.hygiene_type,
        name="hygiene_type",
    ),

    path(
        "add-hygiene-to-cart/<int:id>/",
        views.add_hygiene_to_cart,
        name="add_hygiene_to_cart",
    ),


    # =========================================================
    # BOUTIQUE BLOQUÉE
    # =========================================================

    path(
        "boutique-bloquee/",
        views.boutique_bloquee,
        name="boutique_bloquee",
    ),


    # =========================================================
    # AVIS ET J’AIME
    # =========================================================

    path(
        "produit/<int:product_id>/aimer/",
        views.aimer_produit,
        name="aimer_produit",
    ),

    path(
        "produit/<int:product_id>/avis/",
        views.ajouter_avis,
        name="ajouter_avis",
    ),


    # =========================================================
    # TABLEAU DE BORD ADMINISTRATIF
    # =========================================================

    path(
        "administration/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),

    path(
        "administration/products/",
        views.admin_products,
        name="admin_products",
    ),

    path(
        "administration/orders/",
        views.admin_orders,
        name="admin_orders",
    ),

    path(
        "administration/payments/",
        views.admin_payments,
        name="admin_payments",
    ),


    # =========================================================
    # GESTION DES PRODUITS
    # =========================================================

    path(
        "administration/add-product/",
        views.add_product,
        name="add_product",
    ),

    path(
        "administration/edit-product/<int:id>/",
        views.edit_product,
        name="edit_product",
    ),

    path(
        "administration/delete-product/<int:id>/",
        views.delete_product,
        name="delete_product",
    ),


    # =========================================================
    # GESTION MODE
    # =========================================================

    path(
        "administration/mode/<str:type>/",
        views.admin_mode_type,
        name="admin_mode_type",
    ),

    path(
        "administration/mode/modifier/<int:id>/",
        views.modifier_mode,
        name="modifier_mode",
    ),

    path(
        "administration/edit-mode/<int:id>/",
        views.edit_mode,
        name="edit_mode",
    ),


    # =========================================================
    # GESTION BEAUTÉ
    # =========================================================

    path(
        "administration/beaute/<str:type>/",
        views.admin_beaute_type,
        name="admin_beaute_type",
    ),

    path(
        "administration/edit-beaute/<int:id>/",
        views.edit_beaute,
        name="edit_beaute",
    ),


    # =========================================================
    # GESTION HYGIÈNE
    # =========================================================

    path(
        "administration/hygiene/<str:type_name>/",
        views.admin_hygiene_type,
        name="admin_hygiene_type",
    ),

    path(
        "administration/edit-hygiene/<int:id>/",
        views.edit_hygiene,
        name="edit_hygiene",
    ),


    # =========================================================
    # GESTION DES COMMANDES
    # =========================================================

    path(
        "administration/order/<int:order_id>/",
        views.admin_order_detail,
        name="admin_order_detail",
    ),

    path(
        "administration/delete-order/<int:id>/",
        views.delete_order,
        name="delete_order",
    ),

    path(
        "administration/facture/<int:order_id>/",
        views.download_invoice,
        name="download_invoice",
    ),

    path(
        "administration/expedier-commande/<int:order_id>/",
        views.expedier_commande,
        name="expedier_commande",
    ),

    path(
        "administration/marquer-payee/<int:order_id>/",
        views.marquer_payee,
        name="marquer_payee",
    ),
    path(
    "administration/commandes/<int:order_id>/rappel/",
    views.rappel_commande,
    name="rappel_commande",
    ),
    path("diam-ia/chat/", views.diam_ia_chat, name="diam_ia_chat"),

    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
  
    path("cart/",views.cart,name="cart",),
  
]