# Generated by Django 5.1.1 on 2024-09-24 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('description', models.CharField(blank=True, max_length=2048, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Show this category in search results and catalogue listings.')),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='OptionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Option Group',
                'verbose_name_plural': 'Option Groups',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('type', models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('float', 'Float'), ('option', 'Option'), ('multi_option', 'Multi Option')], default='text', max_length=16)),
                ('required', models.BooleanField(default=False)),
                ('option_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.optiongroup')),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Option',
            },
        ),
        migrations.CreateModel(
            name='OptionGroupValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.optiongroup')),
            ],
            options={
                'verbose_name': 'Option Group Value',
                'verbose_name_plural': 'Option Group Values',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('meta_title', models.CharField(blank=True, max_length=128, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('is_discountable', models.BooleanField(default=True, help_text='This flag indicates if this product can be used in an offer or not', verbose_name='Is discountable?')),
                ('is_active', models.BooleanField(default=True, help_text='Show this product in search results.')),
                ('categories', models.ManyToManyField(related_name='categories', to='products.category')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.product')),
                ('product_options', models.ManyToManyField(blank=True, help_text='Options are values that can be associated with a item something like a personalised message to be printed on a T-shirt.', to='products.option')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('type', models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('float', 'Float'), ('option', 'Option'), ('multi_option', 'Multi Option')], default='text', max_length=16)),
                ('required', models.BooleanField(default=False)),
                ('option_group', models.ForeignKey(blank=True, help_text='Select an option group if using type "Option" or "Multi Option"', null=True, on_delete=django.db.models.deletion.PROTECT, to='products.optiongroup')),
            ],
            options={
                'verbose_name': 'Product Attribute',
                'verbose_name_plural': 'Product Attributes',
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.TextField(blank=True, null=True)),
                ('value_integer', models.IntegerField(blank=True, null=True)),
                ('value_float', models.FloatField(blank=True, null=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productattribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('value_multi_option', models.ManyToManyField(blank=True, related_name='multi_valued_attribute_value', to='products.optiongroupvalue')),
                ('value_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.optiongroupvalue')),
            ],
            options={
                'verbose_name': 'Attribute Value',
                'verbose_name_plural': 'Attribute Values',
                'unique_together': {('product', 'attribute')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(help_text='A product attribute defines a feature the product may have, like size...', through='products.ProductAttributeValue', to='products.productattribute'),
        ),
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('description', models.CharField(blank=True, max_length=2048, null=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('track_stock', models.BooleanField(default=True)),
                ('require_shipping', models.BooleanField(default=True)),
                ('options', models.ManyToManyField(blank=True, to='products.option')),
            ],
            options={
                'verbose_name': 'Product Class',
                'verbose_name_plural': 'Product Classes',
            },
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='products.productclass'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.productclass'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(height_field='height', upload_to='images/', width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'ordering': ('display_order',),
            },
        ),
        migrations.CreateModel(
            name='ProductRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveSmallIntegerField(default=0)),
                ('primary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_recommendation', to='products.product')),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'ordering': ('primary', '-rank'),
                'unique_together': {('primary', 'recommendation')},
            },
        ),
    ]