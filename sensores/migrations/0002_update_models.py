# Generated manually to fix model schema

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensores', '0001_initial'),
    ]

    operations = [
        # Update Motor model
        migrations.RemoveField(
            model_name='motor',
            name='tipo',
        ),
        migrations.AlterField(
            model_name='motor',
            name='potencia',
            field=models.DecimalField(decimal_places=2, help_text='Potência do motor em watts', max_digits=10),
        ),
        migrations.AlterField(
            model_name='motor',
            name='nome',
            field=models.CharField(help_text='Nome do motor', max_length=100),
        ),
        migrations.AlterField(
            model_name='motor',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, help_text='Data de criação'),
        ),
        
        # Update Sensor model
        migrations.RemoveField(
            model_name='sensor',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='unidade',
        ),
        migrations.AddField(
            model_name='sensor',
            name='precisao',
            field=models.DecimalField(decimal_places=2, help_text='Precisão do sensor', max_digits=5, default=0.01),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sensor',
            name='tipo',
            field=models.CharField(help_text='Tipo do sensor (ex: temperatura, pressão)', max_length=50),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, help_text='Data de criação'),
        ),
        
        # Rename Dados to DadosSensor and update fields
        migrations.RenameModel(
            old_name='Dados',
            new_name='DadosSensor',
        ),
        migrations.RenameField(
            model_name='dadossensor',
            old_name='timestamp',
            new_name='data_hora',
        ),
        migrations.AlterField(
            model_name='dadossensor',
            name='data_hora',
            field=models.DateTimeField(auto_now=True, help_text='Data e hora da coleta'),
        ),
        migrations.AlterField(
            model_name='dadossensor',
            name='motor',
            field=models.ForeignKey(help_text='Motor relacionado', on_delete=django.db.models.deletion.CASCADE, to='sensores.motor'),
        ),
        migrations.AlterField(
            model_name='dadossensor',
            name='sensor',
            field=models.ForeignKey(help_text='Sensor que coletou o dado', on_delete=django.db.models.deletion.CASCADE, to='sensores.sensor'),
        ),
        migrations.AlterField(
            model_name='dadossensor',
            name='valor',
            field=models.FloatField(help_text='Valor coletado pelo sensor'),
        ),
        
        # Create SensorMotor model
        migrations.CreateModel(
            name='SensorMotor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motor', models.ForeignKey(help_text='Motor associado', on_delete=django.db.models.deletion.CASCADE, to='sensores.motor')),
                ('sensor', models.ForeignKey(help_text='Sensor associado', on_delete=django.db.models.deletion.CASCADE, to='sensores.sensor')),
            ],
            options={
                'verbose_name': 'Sensor do Motor',
                'verbose_name_plural': 'Sensores dos Motores',
            },
        ),
    ]