from datetime import datetime

from flask import Flask, request, jsonify
from database import db
from models.meal import Diet
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diet.db'

db.init_app(app)

@app.route('/diet', methods=['POST'])
def create_diet():
    data = request.json
    name = data.get ("name")
    description = data.get("description")
    is_on_diet = data.get("is_on_diet")
    meal_datetime = datetime.strptime(data.get("meal_datetime"),"%Y-%m-%d %H:%M")

    if name and description and is_on_diet is not None:
        meal = Diet(name=name, 
                    description=description,
                    meal_datetime=meal_datetime,
                    is_on_diet=is_on_diet)
        
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Dieta criada com sucesso"}), 201

    return jsonify ({"message": "todos os campos são obrigatórios"}), 400



if __name__ == '__main__':
    app.run(debug=True)


