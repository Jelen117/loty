# Generated by Django 2.0.3 on 2018-05-12 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loty2', '0004_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_tickets', models.IntegerField(default=0)),
                ('flight', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flight', to='loty2.Flight')),
                ('passenger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passenger', to='loty2.Passenger')),
            ],
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='flight',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='passenger',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]