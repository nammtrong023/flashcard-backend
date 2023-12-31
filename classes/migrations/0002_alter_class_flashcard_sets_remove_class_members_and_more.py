# Generated by Django 4.0.10 on 2023-12-28 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flashcards', '0002_alter_flashcardsetviewer_question_types'),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='flashcard_sets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flashcard_sets', to='flashcards.flashcardset'),
        ),
        migrations.RemoveField(
            model_name='class',
            name='members',
        ),
        migrations.AddField(
            model_name='class',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
