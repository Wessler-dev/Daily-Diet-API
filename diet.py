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

@app.route('/diet', methods=['GET'])
def get_diets():
    diets = Diet.query.all()
    diet_list = []
    for diet in diets:
        diet_list.append({
            "id": diet.id,
            "name": diet.name,
            "description": diet.description,
            "meal_datetime": diet.meal_datetime.strftime("%Y-%m-%d %H:%M"),
            "is_on_diet": diet.is_on_diet
        })
    return jsonify(diet_list)
    
@app.route('/diet/<int:meal_id>', methods=['PUT'])
def update_diet(meal_id):
    meal = Diet.query.get(meal_id)
    if meal:
        data = request.json
        meal.name = data.get("name", meal.name)
        meal.description = data.get("description", meal.description)
        meal.is_on_diet = data.get("is_on_diet", meal.is_on_diet)
        meal_datetime_str = data.get("meal_datetime")
        if meal_datetime_str:
            meal.meal_datetime = datetime.strptime(meal_datetime_str, "%Y-%m-%d %H:%M")
            db.session.commit()

            return jsonify({"message": f"Refeição {meal_id} atualizada com sucesso"})
        
        return jsonify({"message":" Refeição não encontrada"}), 404
        

@app.route('/diet/<int:meal_id>', methods=['DELETE'])
def delete_diet(meal_id):
    meal = Diet.query.get(meal_id)
    if meal:
        db.session.delete(meal)
        db.session.commit()

        return jsonify({"message": "Refeição deletada com sucesso"})

    return jsonify({"message": "Refeição não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)


