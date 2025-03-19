from flask import Flask, render_template, jsonify
from lerxml import enviadictufporFaturamento

painelF = Flask(__name__)

@painelF.route('/')
def index():
    # Renderiza o template HTML
     return render_template('index.html', dados=enviadictufporFaturamento())

if __name__ == '__main__':
    painelF.run(debug=True)

   