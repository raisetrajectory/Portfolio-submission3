# Generated by Django 4.2.11 on 2024-07-10 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_alter_users_managers_users_introduction_and_more"),
        ("boards", "0003_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="comments",
            name="counselor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="accounts.counselor",
            ),
        ),
        migrations.AddField(
            model_name="themes",
            name="counselor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="themes",
                to="accounts.counselor",
            ),
        ),
    ]
