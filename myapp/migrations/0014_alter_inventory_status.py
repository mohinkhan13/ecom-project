# Generated by Django 5.1 on 2024-09-05 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_inventory_status_alter_orderitem_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='status',
            field=models.CharField(choices=[('In_Stock', 'In Stock'), ('Out_of_Stock', 'Out of Stock')], default='In_Stock', max_length=20),
        ),
    ]
