# Generated by Django 5.0.2 on 2025-03-10 19:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leave', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='leavebalance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_balances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_leave_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='leave_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to='leave.leavetype'),
        ),
        migrations.AddField(
            model_name='leavepolicy',
            name='leave_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='leave.leavetype'),
        ),
        migrations.AddField(
            model_name='leavebalance',
            name='leave_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_balances', to='leave.leavetype'),
        ),
        migrations.AlterUniqueTogether(
            name='leavebalance',
            unique_together={('employee', 'leave_type', 'year')},
        ),
    ]
