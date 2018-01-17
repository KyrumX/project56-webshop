# Generated by Django 2.0.1 on 2018-01-16 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_auto_20180116_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=1500)),
                ('rating', models.IntegerField()),
                ('customerID', models.ForeignKey(db_column='customerID', on_delete=django.db.models.deletion.CASCADE, to='store.UserVisits')),
                ('prodNum', models.ForeignKey(db_column='prodNum', on_delete=django.db.models.deletion.CASCADE, to='store.Products')),
            ],
            options={
                'verbose_name_plural': 'Product Reviews',
            },
        ),
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together={('prodNum', 'customerID')},
        ),
    ]
