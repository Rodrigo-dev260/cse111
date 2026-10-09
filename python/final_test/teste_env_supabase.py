
import os
import psycopg
from dotenv import load_dotenv

# Carrega as configurações do arquivo .env
load_dotenv()

print("TESTANDO CONEXÃO COM SUPABASE")
print("-" * 35)

try:
    with psycopg.connect(
        host=os.getenv("SUPABASE_HOST"),
        port=int(os.getenv("SUPABASE_PORT", "5432")),
        dbname=os.getenv("SUPABASE_DB"),
        user=os.getenv("SUPABASE_USER"),
        password=os.getenv("SUPABASE_PASSWORD"),
        sslmode="require",
        connect_timeout=10
    ) as conexao:

        print("Conexão realizada com sucesso!")

        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name IN ('produtos', 'movimentacoes')
                ORDER BY table_name
            """)

            tabelas = cursor.fetchall()

            print("\nTabelas encontradas:")

            for tabela in tabelas:
                print("-", tabela[0])

except (psycopg.Error, ValueError, TypeError) as erro:
    print("Não foi possível conectar ao Supabase.")
    print("Tipo de erro:", type(erro).__name__)
    print("Verifique as configurações do arquivo .env.")
