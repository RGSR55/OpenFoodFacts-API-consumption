from flask import Flask, render_template, redirect, url_for, request
from models import *
import json, requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pap_database.db'
db.init_app(app)

def obter_produtos():
    list_product_id = ['5055534339985','5901330054679','5600380894401','7503023641944','0860006506810','5055936830394' ]
    produtos = []

    for product_id in list_product_id:
        url = f'https://world.openfoodfacts.org/api/v3/product/{product_id}.json'
        response = requests.get(url)
        produto_dict = response.json()

        categorias = produto_dict.get('product', {}).get('categories_tags', [])
        nome = produto_dict.get('product', {}).get('product_name', 'Produto sem nome')
        imagem = produto_dict.get('product', {}).get('image_front_url', '')
        score = produto_dict.get('product', {}).get('nutriscore', {}).get('2023', {}).get('score', 'N/A')
        grade = produto_dict.get('product', {}).get('nutriscore', {}).get('2023', {}).get('grade', 'N/A')

        produto = {
            'id' : product_id,
            'categorias': categorias,
            'nome': nome,
            'imagem': imagem,
            'score': score,
            'grade' : grade,
            'url': url
        }
        
        produtos.append(produto)
    return produtos


@app.route('/')
def index():
    produtos = obter_produtos()
    return render_template('index.html', produtos=produtos)


@app.route('/produtos')
def produtos():
    produtos = obter_produtos()
    return render_template('produtos.html', produtos=produtos)


@app.route('/produto/<string:product_id>')
def detalhe_produto(product_id):
    
    url = f'https://world.openfoodfacts.org/api/v3/product/{product_id}.json'
    response = requests.get(url)
    produto_dict = response.json().get('product', {})

    
    nome = produto_dict.get('product_name', 'Produto sem nome')
    imagem_grande = produto_dict.get('image_url', '')
    ingredientes = produto_dict.get('ingredients_text', 'Ingredientes não disponíveis')
    nutricao = produto_dict.get('nutriments', {})
    categoria = produto_dict.get('categories_tags', [])
    nutri_score = produto_dict.get('nutriscore', {}).get('2023', {}).get('score', 'N/A')

    
    produto = {
        'nome': nome,
        'imagem_grande': imagem_grande,
        'ingredientes': ingredientes,
        'calorias': nutricao.get('energy-kcal_100g', 'N/A'),
        'gorduras': nutricao.get('fat_100g', 'N/A'),
        'proteinas': nutricao.get('proteins_100g', 'N/A'),
        'carboidratos': nutricao.get('carbohydrates_100g', 'N/A'),
        'nutri_score': nutri_score,
        'categoria': categoria,
        'url' : url
    }
    
    return render_template('detalhe_produto.html', produto=produto)


@app.route('/api')
def api():
    #dict_user = {
        #'email':'rui3@gmail.com',
        #'password':'pass1'
    #}

        db_users = User.query.all()
        print(db_users)
        return json.dumps(db_users)
    

    #return json.dumps(dict_user)
    #return render_template('index.html')
   

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')



@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_handler', methods=['POST'])
def login_handler():
    user_email = request.form['login-form-email']
    user_password = request.form['login-form-password']
    print(user_email,user_password)
    user = User.query.filter_by(email=user_email, password=user_password).first()
    if user:
        return render_template('profile.html', html_user = user)
    else:
        return render_template('login.html', msg='Credenciais Incorretas')
    

@app.route('/registar')
def registar():
    return render_template('registar.html')


@app.route('/register_handler', methods=['POST'])
def register_handler():
    first_name = request.form['register-form-name']
    email = request.form['register-form-email']
    password = request.form['register-form-password']
    repassword = request.form['register-form-repassword']
    print(first_name,email,password)
    if password!=repassword:
        return render_template('registar.html', msg='Passwords não coincidem')
    else:
        user = User(firstname=first_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/forgot_handler', methods=['POST'])
def forgot_handler():
    user_email = request.form['forgot-form-email']
    
    user = User.query.filter_by(email=user_email).first()
    if user:   
        return render_template('login.html',msg='Credenciais enviadas para o email' )
    else:
        return render_template('forgot.html', msg='Email não registado')


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)