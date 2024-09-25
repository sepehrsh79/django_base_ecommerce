from django.db import models
from treebeard.mp_tree import MP_Node, MP_NodeQuerySet

from libs.db.models import AuditableModel


class CategoryQuerySet(MP_NodeQuerySet):
    """
    Excludes non-active categories
    """
    def public(self):
        return self.filter(is_active=True)


# Create your models here.
class Category(MP_Node):
    """
    A product category used for navigation
    """
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    is_active = models.BooleanField(help_text="Show this category in search results and catalogue listings.",
                                                default=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(AuditableModel):
    """
    The base product object
    E.g. asus TUF, acer Nitro, ...
    """
    title = models.CharField(max_length=128, null=True, blank=True)
    slug = models.SlugField(unique=True)

    meta_title = models.CharField(max_length=128, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    product_class = models.ForeignKey('ProductClass', on_delete=models.PROTECT, null=True, blank=True,
                                      related_name='products')

    attributes = models.ManyToManyField(
        'ProductAttribute',
            through='ProductAttributeValue',
            help_text = "A product attribute defines a feature the product may have, like size..."
    )
    product_options = models.ManyToManyField(
        "Option",
        blank=True,
        help_text=
            "Options are values that can be associated with a item "
            "something like a personalised message to be printed on "
            "a T-shirt."
        ,
    )

    # recommended_products = models.ManyToManyField('Product', through='ProductRecommendation', blank=True)
    categories = models.ManyToManyField(Category, related_name='categories')
    is_discountable = models.BooleanField("Is discountable?", default=True,
                                          help_text="This flag indicates if this product can be used in an offer or not"
    )
    is_active = models.BooleanField(default=True,
                                    help_text="Show this product in search results.",
    )

    @property
    def main_image(self):
        if self.images.exists():
            return self.images.first()
        else:
            return None


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductClass(models.Model):
    """
    E.g. Books, DVDs and Toys. A product can only belong to one product class.
    """
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    #: Digital products generally don't require their stock levels to be tracked and don't require shipping.
    track_stock = models.BooleanField(default=True)
    require_shipping = models.BooleanField(default=True)

    options = models.ManyToManyField('Option', blank=True)

    @property
    def has_attribute(self):
        return self.attributes.exists()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Class"
        verbose_name_plural = "Product Classes"


class ProductAttribute(models.Model):
    class AttributeTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    product_class = models.ForeignKey('ProductClass', on_delete=models.CASCADE, null=True, related_name='attributes')
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=AttributeTypeChoice.choices, default=AttributeTypeChoice.text)
    option_group = models.ForeignKey(
        'OptionGroup',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='Select an option group if using type "Option" or "Multi Option"',

    )
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class Option(models.Model):
    """
        An option that can be selected for an item when the product is added to the cart.

        For example,a personalised message to print on a T-shirt.
    """
    class OptionTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=OptionTypeChoice.choices, default=OptionTypeChoice.text)
    option_group = models.ForeignKey('OptionGroup', on_delete=models.PROTECT, null=True, blank=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Option"


class OptionGroup(models.Model):
    """
    Defines a group of options that collectively may be used as an
    attribute type

    For example, Language
    """
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group"
        verbose_name_plural = "Option Groups"


class OptionGroupValue(models.Model):
    """
        Provides an option within an option group for an attribute type
        Examples: In a Language group, English, Greek, French
    """
    title = models.CharField(max_length=255, db_index=True)
    group = models.ForeignKey('OptionGroup', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group Value"
        verbose_name_plural = "Option Group Values"


class ProductAttributeValue(models.Model):
    """
        m2m relationship between Product and ProductAttribute. This specifies the value of the attribute for
        a particular product
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey('ProductAttribute', on_delete=models.CASCADE)

    value_text = models.TextField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_option = models.ForeignKey('OptionGroupValue', on_delete=models.PROTECT, null=True, blank=True)
    value_multi_option = models.ManyToManyField('OptionGroupValue', blank=True,
                                                related_name='multi_valued_attribute_value')

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
        unique_together = ('product', 'attribute')


class ProductRecommendation(models.Model):
    primary = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='primary_recommendation')
    recommendation = models.ForeignKey('Product', on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('primary', 'recommendation')
        ordering = ('primary', '-rank')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(width_field="width", height_field="height", upload_to="images/")

    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('display_order',)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        for index, image in enumerate(self.product.images.all()):
            image.display_order = index
            image.save()
