# webapp.py
from flask import Flask, render_template, abort
import os, json

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-aqui-2025'

# Carregar base de dados
with open("roteiros.json", "r", encoding="utf-8") as f:
    ROTEIROS_DB = json.load(f)

# Configuração para GitHub Pages
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_BASE_URL'] = os.environ.get('FREEZER_BASE_URL', 'http://localhost:5000/')

# ==================== ROTAS ====================

@app.route('/')
def home():
    hero_texts = [
        "Roteiros de Espiritualidade",
        "Roteiros Turísticos com Fé",
        "Experiências que transformam"
    ]

    roteiros_espirituais = [
        {
            "id": r["id"],
            "img": r["img"],
            "title": r["title"],
            "date": f"{r['start']} a {r['end']}",
            "url": f"/roteiro/{r['id']}/"
        }
        for r in ROTEIROS_DB.values()
        if r["categoria"] == "espiritualidade"
    ][:4]

    roteiros_turisticos = [
        {
            "id": r["id"],
            "img": r["img"],
            "title": r["title"],
            "date": f"{r['start']} a {r['end']}",
            "url": f"/roteiro/{r['id']}/"
        }
        for r in ROTEIROS_DB.values()
        if r["categoria"] == "turistico"
    ][:4]

    return render_template("home.html",
                           hero_texts=hero_texts,
                           roteiros_espirituais=roteiros_espirituais,
                           roteiros_turisticos=roteiros_turisticos)


@app.route('/roteiros/espiritualidade/sao-jose/')
def roteiros_sao_jose():
    roteiros = [r for r in ROTEIROS_DB.values()
                if r["categoria"] == "espiritualidade" and r["empresa"] == "sao-jose"]
    return render_template("lista_roteiros.html",
                           titulo="São José Viagens",
                           roteiros=roteiros)


@app.route('/roteiros/espiritualidade/cancaonova/')
def roteiros_cancaonova():
    roteiros = [r for r in ROTEIROS_DB.values()
                if r["categoria"] == "espiritualidade" and r["empresa"] == "cancaonova"]
    return render_template("lista_roteiros.html",
                           titulo="Comunidade Canção Nova",
                           roteiros=roteiros)


@app.route('/roteiros/turisticos/')
def roteiros_turisticos():
    roteiros = [r for r in ROTEIROS_DB.values()
                if r["categoria"] == "turistico"]
    return render_template("lista_roteiros.html",
                           titulo="Roteiros Turísticos",
                           roteiros=roteiros)


@app.route('/roteiro/<int:roteiro_id>/')
def roteiro_detalhe(roteiro_id):
    roteiro = ROTEIROS_DB.get(str(roteiro_id))
    if not roteiro:
        abort(404)
    return render_template("detalhe.html", roteiro=roteiro)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)