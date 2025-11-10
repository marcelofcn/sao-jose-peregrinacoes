#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

# Garante que o diretório atual esteja no path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask_frozen import Freezer

# ------------------------------------------------------
# Importa o app Flask e o banco de roteiros
# ------------------------------------------------------
try:
    from app import app, ROTEIROS_DB
    print(f"✅ {len(ROTEIROS_DB)} roteiros carregados")
except Exception as e:
    print(f"❌ Erro ao importar app: {e}")
    sys.exit(1)

# ------------------------------------------------------
# Configurações do Freezer
# ------------------------------------------------------
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = False
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/sao-jose-peregrinacoes'

freezer = Freezer(app)

# Garante que a pasta docs exista
os.makedirs('docs', exist_ok=True)

# ------------------------------------------------------
# Gera as rotas dinâmicas dos roteiros
# ------------------------------------------------------
@freezer.register_generator
def detalhe_roteiro():
    """Gera páginas de detalhe para cada roteiro."""
    for r in ROTEIROS_DB.values():
        yield f"/roteiro/{r['id']}/"


# ------------------------------------------------------
# Gera arquivos estáticos (CSS, imagens, etc.)
# ------------------------------------------------------
@freezer.register_generator
def static_files():
    """Inclui manualmente os arquivos da pasta static."""
    static_folder = os.path.join(app.root_path, 'static')
    for dirpath, _, filenames in os.walk(static_folder):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), app.root_path)
            yield f'/{rel_path}'


# ------------------------------------------------------
# Execução principal
# ------------------------------------------------------
if __name__ == '__main__':
    print("🚀 Gerando site estático...")
    freezer.freeze()
    print("✅ Site estático gerado em /docs")
