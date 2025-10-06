#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, text

engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'usuario'
        ORDER BY ordinal_position;
    """))
    print('COLUMNAS DE TABLA USUARIO:')
    for row in result:
        print(f'{row[0]} | {row[1]}')