# Generated by Django 3.0.10 on 2020-09-06 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="category",
            field=models.CharField(
                choices=[("SH", "Shirt"), ("SW", "Sport Wear"), ("OW", "Out Wear")],
                default="SH",
                max_length=2,
                verbose_name="Category",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="description",
            field=models.CharField(
                blank=True, max_length=300, null=True, verbose_name="Description"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="label",
            field=models.CharField(
                choices=[("PR", "primary"), ("SE", "secondary"), ("DA", "danger")],
                default="PR",
                max_length=2,
                verbose_name="Label",
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="ordered",
            field=models.BooleanField(default=False, verbose_name="Ordered"),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(
                blank=True, default=1, null=True, verbose_name="Quantity"
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="amount",
            field=models.IntegerField(verbose_name="Amount"),
        ),
        migrations.AlterField(
            model_name="item",
            name="price",
            field=models.FloatField(verbose_name="Price"),
        ),
        migrations.AlterField(
            model_name="item",
            name="title",
            field=models.CharField(max_length=100, verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="order",
            name="ordered",
            field=models.BooleanField(default=False, verbose_name="Ordered"),
        ),
        migrations.AlterField(
            model_name="order",
            name="ordered_date",
            field=models.DateField(verbose_name="Ordered Date"),
        ),
        migrations.AlterField(
            model_name="order",
            name="start_data",
            field=models.DateField(auto_now_add=True, verbose_name="Start Date"),
        ),
    ]
