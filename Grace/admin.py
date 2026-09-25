from django.contrib import admin
from .models import Product, Order, Payment, OrderItem, Cart, CartItem
from django.utils.html import format_html



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('nom', 'prix','prix_promo', 'stock', 'created_at', 'preview')
    search_fields = ('nom',)
    list_filter = ('created_at',)
    filter_horizontal = ('similar_products',)

    # 🔥 ORGANISATION PRO
    fieldsets = (
        ("Infos produit", {
            'fields': ('nom', 'description', 'prix','prix_promo', 'stock')
        }),

        ("Images", {
            'fields': ('image', 'image2', 'image3', 'image4')
        }),

        ("Vidéo", {
            'fields': ('video',)
        }),

        ("Produits similaires", {
            'fields': ('similar_products',)
        }),
    )

    # 🔥 PREVIEW IMAGE DANS ADMIN
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.image.url)
        return "-"
    
    preview.short_description = "Image"


# 🔹 ORDER ITEM INLINE (afficher produits dans commande)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0

    readonly_fields = (
        'product',
        'quantity',
        'price',
    )
# =========================
# ORDER ITEM INLINE
# =========================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# =========================
# ORDER ADMIN
# =========================
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # =========================================================
    # LISTE DES COMMANDES
    # =========================================================

    list_display = (
        "id",
        "client_complet",
        "email",
        "telephone",
        "total_formate",
        "statut_paiement_colore",
        "statut_commande_colore",
        "statut_livraison_colore",
        "shipping_service",
        "tracking_number",
        "order_reminder",
        "created_at",
    )

    # =========================================================
    # FILTRES
    # =========================================================

    list_filter = (
        "payment_status",
        "status",
        "delivery_status",
        "shipping_service",
        "order_reminder",
        "pays",
        "created_at",
        "shipped_at",
        "delivered_at",
    )

    # =========================================================
    # RECHERCHE
    # =========================================================

    search_fields = (
        "=id",
        "prenom",
        "nom",
        "email",
        "telephone",
        "adresse",
        "tracking_number",
        "transaction_id",
        "user__username",
        "user__email",
    )

    # =========================================================
    # CHAMPS EN LECTURE SEULE
    # =========================================================

    readonly_fields = (
        "created_at",
        "updated_at",
        "transaction_id",
        "date_expedition_affichee",
        "date_livraison_affichee",
    )

    # =========================================================
    # ORGANISATION DU FORMULAIRE
    # =========================================================

    fieldsets = (

        (
            "Commande",
            {
                "fields": (
                    "user",
                    "status",
                    "payment_status",
                    "total",
                    "transaction_id",
                )
            },
        ),

        (
            "Informations de la cliente ou du client",
            {
                "fields": (
                    "prenom",
                    "nom",
                    "email",
                    "indicatif",
                    "telephone",
                )
            },
        ),

        (
            "Adresse de livraison",
            {
                "fields": (
                    "pays",
                    "adresse",
                )
            },
        ),

        (
            "Gestion de la livraison",
            {
                "fields": (
                    "shipping_service",
                    "tracking_number",
                    "delivery_status",
                    "delivery_note",
                    "date_expedition_affichee",
                    "date_livraison_affichee",
                )
            },
        ),

        (
            "Rappel administratif",
            {
                "fields": (
                    "order_reminder",
                    "reminder_note",
                )
            },
        ),

        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

    # =========================================================
    # ARTICLES DE LA COMMANDE
    # =========================================================

    inlines = [
        OrderItemInline,
    ]

    # =========================================================
    # ACTIONS GROUPÉES
    # =========================================================

    actions = (
        "marquer_payees",
        "marquer_en_traitement",
        "marquer_en_preparation",
        "marquer_expediees",
        "marquer_en_transit",
        "marquer_livrees",
        "activer_rappel",
        "desactiver_rappel",
    )

    # =========================================================
    # OPTIONS
    # =========================================================

    list_per_page = 25

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
    )

    save_on_top = True

    preserve_filters = True

    # =========================================================
    # AFFICHAGE DU CLIENT
    # =========================================================

    @admin.display(
        description="Cliente ou client",
        ordering="prenom",
    )
    def client_complet(self, obj):

        return f"{obj.prenom} {obj.nom}".strip()

    # =========================================================
    # AFFICHAGE DU TOTAL
    # =========================================================

    @admin.display(
        description="Total",
        ordering="total",
    )
    def total_formate(self, obj):

        return format_html(
            "<strong>{} $ CA</strong>",
            f"{obj.total:.2f}",
        )

    # =========================================================
    # STATUT DU PAIEMENT
    # =========================================================

    @admin.display(
        description="Paiement",
        ordering="payment_status",
    )
    def statut_paiement_colore(self, obj):

        couleurs = {
            "PAID": (
                "#e8f7ec",
                "#176b36",
                "Payé",
            ),
            "PENDING": (
                "#fff4d7",
                "#956300",
                "En attente",
            ),
            "FAILED": (
                "#ffe8eb",
                "#a11f2e",
                "Échoué",
            ),
            "REFUNDED": (
                "#e9f1ff",
                "#2457a7",
                "Remboursé",
            ),
            "UNPAID": (
                "#f1f3f5",
                "#5f6872",
                "Non payé",
            ),
        }

        background, color, label = couleurs.get(
            obj.payment_status,
            (
                "#f1f3f5",
                "#5f6872",
                obj.get_payment_status_display(),
            )
        )

        return format_html(
            """
            <span style="
                display:inline-block;
                padding:6px 11px;
                border-radius:50px;
                background:{};
                color:{};
                font-size:11px;
                font-weight:800;
            ">
                {}
            </span>
            """,
            background,
            color,
            label,
        )

    # =========================================================
    # STATUT DE LA COMMANDE
    # =========================================================

    @admin.display(
        description="Commande",
        ordering="status",
    )
    def statut_commande_colore(self, obj):

        couleurs = {
            "PENDING": (
                "#fff4d7",
                "#956300",
            ),
            "PAID": (
                "#e8f7ec",
                "#176b36",
            ),
            "PROCESSING": (
                "#e9f1ff",
                "#2457a7",
            ),
            "SHIPPED": (
                "#eee9ff",
                "#6543a5",
            ),
            "DELIVERED": (
                "#e1f7ed",
                "#087443",
            ),
            "CANCELLED": (
                "#ffe8eb",
                "#a11f2e",
            ),
        }

        background, color = couleurs.get(
            obj.status,
            (
                "#f1f3f5",
                "#5f6872",
            )
        )

        return format_html(
            """
            <span style="
                display:inline-block;
                padding:6px 11px;
                border-radius:50px;
                background:{};
                color:{};
                font-size:11px;
                font-weight:800;
            ">
                {}
            </span>
            """,
            background,
            color,
            obj.get_status_display(),
        )

    # =========================================================
    # STATUT DE LIVRAISON
    # =========================================================

    @admin.display(
        description="Livraison",
        ordering="delivery_status",
    )
    def statut_livraison_colore(self, obj):

        couleurs = {
            "NOT_SHIPPED": (
                "#f1f3f5",
                "#5f6872",
            ),
            "PREPARING": (
                "#fff4d7",
                "#956300",
            ),
            "SHIPPED": (
                "#eee9ff",
                "#6543a5",
            ),
            "IN_TRANSIT": (
                "#e9f1ff",
                "#2457a7",
            ),
            "DELIVERED": (
                "#e1f7ed",
                "#087443",
            ),
            "RETURNED": (
                "#fff0e6",
                "#a54b00",
            ),
            "CANCELLED": (
                "#ffe8eb",
                "#a11f2e",
            ),
        }

        background, color = couleurs.get(
            obj.delivery_status,
            (
                "#f1f3f5",
                "#5f6872",
            )
        )

        return format_html(
            """
            <span style="
                display:inline-block;
                padding:6px 11px;
                border-radius:50px;
                background:{};
                color:{};
                font-size:11px;
                font-weight:800;
            ">
                {}
            </span>
            """,
            background,
            color,
            obj.get_delivery_status_display(),
        )

    # =========================================================
    # DATES DE LIVRAISON
    # =========================================================

    @admin.display(
        description="Date d’expédition",
    )
    def date_expedition_affichee(self, obj):

        if not obj.shipped_at:
            return "Non expédiée"

        return timezone.localtime(
            obj.shipped_at
        ).strftime(
            "%d/%m/%Y à %H:%M"
        )

    @admin.display(
        description="Date de livraison",
    )
    def date_livraison_affichee(self, obj):

        if not obj.delivered_at:
            return "Non livrée"

        return timezone.localtime(
            obj.delivered_at
        ).strftime(
            "%d/%m/%Y à %H:%M"
        )

    # =========================================================
    # ACTION : MARQUER COMME PAYÉE
    # =========================================================

    @admin.action(
        description="Marquer les commandes sélectionnées comme payées"
    )
    def marquer_payees(self, request, queryset):

        nombre = queryset.update(
            payment_status="PAID",
            status="PAID",
        )

        self.message_user(
            request,
            f"{nombre} commande(s) marquée(s) comme payée(s).",
        )

    # =========================================================
    # ACTION : EN TRAITEMENT
    # =========================================================

    @admin.action(
        description="Mettre les commandes sélectionnées en traitement"
    )
    def marquer_en_traitement(self, request, queryset):

        nombre = queryset.update(
            status="PROCESSING",
        )

        self.message_user(
            request,
            f"{nombre} commande(s) mise(s) en traitement.",
        )

    # =========================================================
    # ACTION : EN PRÉPARATION
    # =========================================================

    @admin.action(
        description="Mettre les livraisons sélectionnées en préparation"
    )
    def marquer_en_preparation(self, request, queryset):

        nombre = queryset.update(
            status="PROCESSING",
            delivery_status="PREPARING",
        )

        self.message_user(
            request,
            f"{nombre} livraison(s) mise(s) en préparation.",
        )

    # =========================================================
    # ACTION : EXPÉDIÉE
    # =========================================================

    @admin.action(
        description="Marquer les commandes sélectionnées comme expédiées"
    )
    def marquer_expediees(self, request, queryset):

        maintenant = timezone.now()

        nombre = queryset.update(
            status="SHIPPED",
            delivery_status="SHIPPED",
            shipped_at=maintenant,
        )

        self.message_user(
            request,
            f"{nombre} commande(s) marquée(s) comme expédiée(s).",
        )

    # =========================================================
    # ACTION : EN TRANSIT
    # =========================================================

    @admin.action(
        description="Marquer les livraisons sélectionnées comme en transit"
    )
    def marquer_en_transit(self, request, queryset):

        nombre = queryset.update(
            status="SHIPPED",
            delivery_status="IN_TRANSIT",
        )

        self.message_user(
            request,
            f"{nombre} livraison(s) marquée(s) comme en transit.",
        )

    # =========================================================
    # ACTION : LIVRÉE
    # =========================================================

    @admin.action(
        description="Marquer les commandes sélectionnées comme livrées"
    )
    def marquer_livrees(self, request, queryset):

        maintenant = timezone.now()

        nombre = queryset.update(
            status="DELIVERED",
            delivery_status="DELIVERED",
            delivered_at=maintenant,
            order_reminder=False,
        )

        self.message_user(
            request,
            f"{nombre} commande(s) marquée(s) comme livrée(s).",
        )

    # =========================================================
    # ACTION : ACTIVER LE RAPPEL
    # =========================================================

    @admin.action(
        description="Activer un rappel pour les commandes sélectionnées"
    )
    def activer_rappel(self, request, queryset):

        nombre = queryset.update(
            order_reminder=True,
        )

        self.message_user(
            request,
            f"Rappel activé pour {nombre} commande(s).",
        )

    # =========================================================
    # ACTION : DÉSACTIVER LE RAPPEL
    # =========================================================

    @admin.action(
        description="Désactiver le rappel des commandes sélectionnées"
    )
    def desactiver_rappel(self, request, queryset):

        nombre = queryset.update(
            order_reminder=False,
            reminder_note="",
        )

        self.message_user(
            request,
            f"Rappel retiré de {nombre} commande(s).",
        )

# =========================
# ORDER ITEM ADMIN
# =========================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
        'total_price',
    )

    search_fields = (
        'product__nom',
    )
# 🔹 PAIEMENT
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'transaction_id', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('transaction_id',)


# 🔹 PANIER
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'cart',
        'product',
        'mode',
        'beaute',
        'hygiene',
        'quantity'
    )




from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'prenom',
        'nom',
        'email',
        'telephone',
    )

    search_fields = (
        'user__username',
        'prenom',
        'nom',
        'email',
        'telephone',
    )

    list_filter = (
        'prenom',
        'nom',
    )

    ordering = ('nom',)

    fieldsets = (
        ('Compte utilisateur', {
            'fields': ('user',)
        }),
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'email', 'telephone', 'adresse')
        }),
    )

admin.site.register(Profile, ProfileAdmin)



from django.contrib import admin
from .models import Mode


@admin.register(Mode)
class ModeAdmin(admin.ModelAdmin):

    # 🔥 colonnes affichées dans admin
    list_display = ('nom', 'type', 'prix', 'prix_promo', 'stock', 'image_preview')

    # 🔍 filtres à droite
    list_filter = ('type',)

    # 🔎 recherche
    search_fields = ('nom', 'description')

    # 📝 champs éditables directement
    list_editable = ('prix', 'prix_promo', 'stock')

    # 📄 pagination
    list_per_page = 20

    # 🖼️ aperçu image
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" style="border-radius:5px;" />'
        return "-"
    
    image_preview.allow_tags = True
    image_preview.short_description = "Image"






from .models import Beaute


@admin.register(Beaute)
class BeauteAdmin(admin.ModelAdmin):

    # ✅ Colonnes affichées
    list_display = (
        'nom',
        'type',
        'prix',
        'prix_promo',
        'prix_final',
        'reduction_percent',
        'created_at'
    )

    # ✅ Filtres à droite
    list_filter = ('type', 'created_at')

    # ✅ Barre de recherche
    search_fields = ('nom', 'description')

    # ✅ Tri par défaut
    ordering = ('-created_at',)

    # ✅ Champs éditables directement
    list_editable = ('prix', 'prix_promo')

    # ✅ Pagination
    list_per_page = 20

    # ✅ GROUPES (UI propre)
    fieldsets = (
        ("Informations produit", {
            'fields': ('nom', 'description', 'type')
        }),
        ("Prix", {
            'fields': ('prix', 'prix_promo')
        }),
        ("Image", {
            'fields': ('image',)
        }),
    )

    # ✅ AFFICHAGE PRIX FINAL
    def prix_final(self, obj):
        return f"{obj.get_price()} CAD"
    prix_final.short_description = "Prix final"

    # 🔥 AFFICHAGE REDUCTION %
    def reduction_percent(self, obj):
        if obj.reduction() > 0:
            return f"-{obj.reduction()}%"
        return "—"
    reduction_percent.short_description = "Promo"




    from django.contrib import admin
from .models import Hygiene

@admin.register(Hygiene)
class HygieneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'prix', 'prix_promo', 'created_at')
    list_filter = ('type',)
    search_fields = ('nom',)




from django.contrib import admin
from .models import Boutique

admin.site.register(Boutique)





from .models import PreuveCliente

@admin.register(PreuveCliente)
class PreuveClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nom_affiche", "consentement_obtenu", "publie", "ordre")
    list_editable = ("publie", "ordre")