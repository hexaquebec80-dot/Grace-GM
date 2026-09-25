from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.conf import settings


from django.db import models

class Product(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    image = models.ImageField(upload_to='products/')
    # 🔥 NOUVEAU (IMAGES SUPPLEMENTAIRES)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)

    # 🔥 VIDEO
    video = models.FileField(upload_to='products/videos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 produits similaires manuels (admin)
    similar_products = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="related_to"  
    )

    def __str__(self):
        return self.nom

    # ✅ prix final propre
    def get_price(self):
        if self.prix_promo and self.prix_promo > 0:
            return self.prix_promo
        return self.prix

# PANIER
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    mode = models.ForeignKey(
        "Mode",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    beaute = models.ForeignKey(
        "Beaute",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    hygiene = models.ForeignKey(
        "Hygiene",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantity = models.IntegerField(default=1)

# COMMANDE
from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):

    # =========================================================
    # STATUT DE LA COMMANDE
    # =========================================================

    STATUS_CHOICES = (
        ("PENDING", "En attente"),
        ("PAID", "Payée"),
        ("PROCESSING", "En traitement"),
        ("SHIPPED", "Expédiée"),
        ("DELIVERED", "Livrée"),
        ("CANCELLED", "Annulée"),
    )

    # =========================================================
    # STATUT DU PAIEMENT
    # =========================================================

    PAYMENT_CHOICES = (
        ("UNPAID", "Non payé"),
        ("PENDING", "Paiement en attente"),
        ("PAID", "Payé"),
        ("FAILED", "Paiement échoué"),
        ("REFUNDED", "Remboursé"),
    )

    # =========================================================
    # SERVICE DE LIVRAISON
    # =========================================================

    SHIPPING_SERVICE_CHOICES = (
        ("CANADA_POST", "Postes Canada"),
        ("PUROLATOR", "Purolator"),
        ("FEDEX", "FedEx"),
        ("UPS", "UPS"),
        ("DHL", "DHL"),
        ("LOCAL", "Livraison locale"),
        ("PICKUP", "Récupération sur place"),
        ("OTHER", "Autre"),
    )

    # =========================================================
    # STATUT DE LIVRAISON
    # =========================================================

    DELIVERY_STATUS_CHOICES = (
        ("NOT_SHIPPED", "Non expédiée"),
        ("PREPARING", "En préparation"),
        ("SHIPPED", "Expédiée"),
        ("IN_TRANSIT", "En transit"),
        ("DELIVERED", "Livrée"),
        ("RETURNED", "Retournée"),
        ("CANCELLED", "Livraison annulée"),
    )

    # =========================================================
    # CLIENT
    # =========================================================

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Cliente ou client",
    )

    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
    )

    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
    )

    email = models.EmailField(
        verbose_name="Adresse courriel",
    )

    indicatif = models.CharField(
        max_length=10,
        default="+1",
        verbose_name="Indicatif",
    )

    telephone = models.CharField(
        max_length=30,
        verbose_name="Téléphone",
    )

    pays = models.CharField(
        max_length=100,
        default="Canada",
        verbose_name="Pays",
    )

    adresse = models.TextField(
        verbose_name="Adresse de livraison",
    )

    # =========================================================
    # MONTANT
    # =========================================================

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total",
    )

    # =========================================================
    # COMMANDE ET PAIEMENT
    # =========================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
        verbose_name="Statut de la commande",
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="UNPAID",
        verbose_name="Statut du paiement",
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Identifiant Stripe",
    )

    # =========================================================
    # LIVRAISON
    # =========================================================

    shipping_service = models.CharField(
        max_length=30,
        choices=SHIPPING_SERVICE_CHOICES,
        blank=True,
        default="",
        verbose_name="Service de livraison",
    )

    tracking_number = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Numéro de suivi",
    )

    delivery_status = models.CharField(
        max_length=30,
        choices=DELIVERY_STATUS_CHOICES,
        default="NOT_SHIPPED",
        verbose_name="Statut de livraison",
    )

    delivery_note = models.TextField(
        blank=True,
        default="",
        verbose_name="Note de livraison",
    )

    shipped_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d’expédition",
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de livraison",
    )

    # =========================================================
    # RAPPEL ADMINISTRATIF
    # =========================================================

    order_reminder = models.BooleanField(
        default=False,
        verbose_name="Rappel activé",
    )

    reminder_note = models.TextField(
        blank=True,
        default="",
        verbose_name="Note de rappel",
    )

    # =========================================================
    # DATES
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de commande",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification",
    )

    # =========================================================
    # PROPRIÉTÉS
    # =========================================================

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}".strip()

    @property
    def est_payee(self):
        return self.payment_status == "PAID"

    @property
    def est_expediee(self):
        return self.delivery_status in [
            "SHIPPED",
            "IN_TRANSIT",
            "DELIVERED",
        ]

    @property
    def est_livree(self):
        return self.delivery_status == "DELIVERED"

    @property
    def a_un_numero_suivi(self):
        return bool(self.tracking_number)

    # =========================================================
    # CONFIGURATION
    # =========================================================

    class Meta:
        ordering = [
            "-created_at",
        ]

        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return (
            f"Commande #{self.id} - "
            f"{self.prenom} {self.nom}"
        )

# =========================
# ORDER ITEM
# =========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.product.nom
    

    
# PAIEMENT
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)






class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    


from django.db import models

class Mode(models.Model):

    TYPE_CHOICES = [
        ('homme', 'Hommes'),
        ('femme', 'Femmes'),
        ('enfant', 'Enfants'),
    ]

    nom = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    prix = models.DecimalField(max_digits=10, decimal_places=2)

    prix_promo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    image = models.ImageField(upload_to='modes/', blank=True, null=True)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    stock = models.PositiveIntegerField(default=0)  # ✅ ajouté

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    # ✅ prix final (important)
    def get_price(self):
        if self.prix_promo and self.prix_promo < self.prix:
            return self.prix_promo
        return self.prix

    # 🔥 POURCENTAGE DE REDUCTION
    def reduction(self):
        if self.prix_promo and self.prix_promo < self.prix:
            reduction = ((self.prix - self.prix_promo) / self.prix) * 100
            return round(reduction)
        return 0
    




class Beaute(models.Model):

    TYPE_CHOICES = [
        ('cosmetique', 'Cosmétiques'),
        ('soin', 'Soins'),
    ]

    nom = models.CharField(max_length=200)
    description = models.TextField()

    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    image = models.ImageField(upload_to='beaute/')

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    # ✅ PRIX FINAL (UTILISÉ PARTOUT)
    def get_price(self):
        if self.prix_promo and self.prix_promo < self.prix:
            return self.prix_promo
        return self.prix

    # 🔥 POURCENTAGE DE RÉDUCTION
    def reduction(self):
        if self.prix_promo and self.prix_promo < self.prix:
            reduction = ((self.prix - self.prix_promo) / self.prix) * 100
            return round(reduction)
        return 0
    




class Hygiene(models.Model):
    TYPE_CHOICES = [
        ('corps', 'Corps'),
        ('sante', 'Santé'),
    ]

    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix = models.FloatField()
    prix_promo = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='hygiene/')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.nom

    def get_price(self):
        if self.prix_promo and self.prix_promo < self.prix:
            return self.prix_promo
        return self.prix

    def reduction(self):
        if self.prix_promo and self.prix_promo < self.prix:
            return round(((self.prix - self.prix_promo) / self.prix) * 100)
        return 0




class Boutique(models.Model):
    nom = models.CharField(max_length=200)

    is_blocked = models.BooleanField(default=False)

    raison_blocage = models.TextField(
        blank=True,
        null=True
    )






class PreuveCliente(models.Model):
    image = models.ImageField(upload_to="preuves_clientes/")
    nom_affiche = models.CharField(max_length=100, blank=True)
    temoignage = models.TextField(blank=True)
    consentement_obtenu = models.BooleanField(default=False)
    publie = models.BooleanField(default=False)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordre", "-id"]

    def __str__(self):
        return self.nom_affiche or f"Photo cliente #{self.pk}"






class AvisProduit(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="avis_clients",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    note = models.PositiveSmallIntegerField()
    commentaire = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"],
                name="un_avis_par_client_et_produit",
            )
        ]

    def __str__(self):
        return f"{self.product} — {self.note}/5"


class JaimeProduit(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="jaimes",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"],
                name="un_jaime_par_client_et_produit",
            )
        ]



from django.contrib import admin

from .models import AvisProduit, JaimeProduit


@admin.register(AvisProduit)
class AvisProduitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
        "note",
        "created_at",
    )
    list_filter = (
        "note",
        "created_at",
    )
    search_fields = (
        "product__nom",
        "user__username",
        "commentaire",
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(JaimeProduit)
class JaimeProduitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
    )
    search_fields = (
        "product__nom",
        "user__username",
    )



