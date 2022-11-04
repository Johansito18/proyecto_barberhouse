# Generated by Django 4.0.6 on 2022-10-28 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barberhouse', '0007_alter_rol_nombre_rol_alter_usuarios_rol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citas',
            name='empleado',
        ),
        migrations.RemoveField(
            model_name='citas',
            name='servicio',
        ),
        migrations.AddField(
            model_name='citas',
            name='usuarioCliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='usuarioCliente', to='barberhouse.usuarios'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='citas',
            name='usuarioEmpleado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='usuarioEmpleado', to='barberhouse.usuarios'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ServiciosCitas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='barberhouse.citas')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='barberhouse.servicios')),
            ],
        ),
    ]
