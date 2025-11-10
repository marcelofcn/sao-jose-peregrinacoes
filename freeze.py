#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Frozen-Flask  import Freezer

try:
    from app import app, ROTEIROS_DB
    print(f"✅ {len(ROTEIROS_DB)} roteiros")
except Exception as e:
    print(f"❌ {e}")
    sys.exit(1)

app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = False
app.config['FREEZER_BASE_URL'] = 'https://marcelofcn.github.io/sao-jose-peregrinacoes/'

freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    for rid in ROTEIROS_DB.keys():
        yield {'roteiro_id': int(rid)}

if __name__ == '__main__':
    print("\n🚀 Gerando...\n")
    freezer.freeze()
    with open('build/.nojekyll', 'w') as f:
        pass
    print("✅ Pronto!\n")
