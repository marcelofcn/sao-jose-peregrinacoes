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
app.config['FREEZER_RELATIVE_URLS'] = False
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/sao-jose-peregrinacoes'

freezer = Freezer(app)

if not os.path.exists('docs'):
    os.makedirs('docs')


# 🔧 Garante inclusão dos arquivos estáticos
@freezer.register_generator
def detalhe_roteiro():
    from app import ROTEIROS_DB
    for r in ROTEIROS_DB.values():
        yield f"/roteiro/{r['id']}/"


if __name__ == '__main__':
    print("🚀 Gerando site estático...")
    freezer.freeze()
    print("✅ Site estático gerado em /docs")
