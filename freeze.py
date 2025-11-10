#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask_frozen  import Freezer

try:
    from app import app, ROTEIROS_DB
    print(f"✅ {len(ROTEIROS_DB)} roteiros")
except Exception as e:
    print(f"❌ {e}")
    sys.exit(1)

# Configurações do freezer
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/sao-jose-peregrinacoes'

freezer = Freezer(app)

if not os.path.exists('docs'):
    os.makedirs('docs')


# 🔧 Garante inclusão dos arquivos estáticos
@freezer.register_generator
def static_files():
    """Força o Frozen-Flask a incluir os arquivos estáticos."""
    static_folder = os.path.join(app.root_path, 'static')
    for dirpath, _, filenames in os.walk(static_folder):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), app.root_path)
            yield f'/{rel_path}'

if __name__ == '__main__':
    print("🚀 Gerando site estático...")
    freezer.freeze()
    print("✅ Site estático gerado em /docs")
