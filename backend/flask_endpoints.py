from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='wlAc2vR1ms5fBaPtvIM0',
    host='localhost',
    port='5434'
)
cursor = conn.cursor()

@app.route('/pets', methods=['GET'])
def get_all_pets():
    cursor.execute('SELECT * FROM pets')
    pets = cursor.fetchall()
    pets_data = [{'id': pet[0], 'name': pet[1], 'breed': pet[2], 'age': pet[3], 'available': pet[4]} for pet in pets]
    return jsonify(pets_data)


@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    cursor.execute('SELECT * FROM pets WHERE id = %s', (pet_id,))
    pet = cursor.fetchone()
    if pet:
        pet_data = {'id': pet[0], 'name': pet[1], 'breed': pet[2], 'age': pet[3], 'available': pet[4]}
        return jsonify(pet_data)
    else:
        return jsonify({'error': 'Pet not found'}), 404


@app.route('/pets', methods=['POST'])
def add_pet():
    pet_data = request.json
    name = pet_data.get('name')
    breed = pet_data.get('breed')
    age = pet_data.get('age')
    available = pet_data.get('available')

    cursor.execute('INSERT INTO pets (name, breed, age, available) VALUES (%s, %s, %s, %s) RETURNING id',
                   (name, breed, age, available))
    new_pet_id = cursor.fetchone()[0]
    conn.commit()

    return jsonify({'id': new_pet_id, 'name': name, 'breed': breed, 'age': age, 'available': available}), 201


@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    pet_data = request.json
    name = pet_data.get('name')
    breed = pet_data.get('breed')
    age = pet_data.get('age')
    available = pet_data.get('available')

    cursor.execute('UPDATE pets SET name=%s, breed=%s, age=%s, available=%s WHERE id=%s',
                   (name, breed, age, available, pet_id))
    conn.commit()

    return jsonify({'id': pet_id, 'name': name, 'breed': breed, 'age': age, 'available': available})


@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    cursor.execute('DELETE FROM pets WHERE id=%s', (pet_id,))
    conn.commit()
    return jsonify({'message': 'Pet deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)