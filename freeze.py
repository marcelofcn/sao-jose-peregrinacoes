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

# Garante que a pasta estática seja incluída no build
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

freezer = Freezer(app)

@freezer.register_generator
def roteiro_detalhe():
    for rid in ROTEIROS_DB.keys():
        yield {'roteiro_id': int(rid)}

if __name__ == '__main__':
    print("\n🚀 Gerando...\n")
    freezer.freeze()
    with open('docs/.nojekyll', 'w') as f:
        pass
    print("✅ Pronto!\n")
