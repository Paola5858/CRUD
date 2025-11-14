"""
Particionamento automático da tabela DadosSensor por ano.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sensores', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            # Criar particionamento por ano
            """
            ALTER TABLE sensores_dadossensor 
            PARTITION BY RANGE (YEAR(data_hora)) (
                PARTITION p2024 VALUES LESS THAN (2025),
                PARTITION p2025 VALUES LESS THAN (2026),
                PARTITION p2026 VALUES LESS THAN (2027),
                PARTITION p2027 VALUES LESS THAN (2028),
                PARTITION p_future VALUES LESS THAN MAXVALUE
            );
            """,
            # Reverter particionamento
            """
            ALTER TABLE sensores_dadossensor REMOVE PARTITIONING;
            """
        ),
    ]