from flask import Flask, jsonify, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'SmartFarmer REST API - Redirected to Main Backend',
        'main_backend': 'http://localhost:8000',
        'status': 'Use main backend for all API calls'
    })

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def redirect_to_main_backend(path):
    """Redirect all API calls to main backend"""
    return jsonify({
        'redirect': f'http://localhost:8000/{path}',
        'message': 'Please use the main backend at localhost:8000 for all API endpoints'
    }), 302

@app.route(
    "/api/productivity/event",
    methods=["POST"]
)
def submit_productivity_event():

    data = (
        request
        .get_json(
            silent=True
        )
        or {}
    )

    try:

        result = (
            blockchain_service
            .submit_productivity_event(
                data
            )
        )

        return jsonify({
            "cod": 201,
            "success": True,
            "result": result
        }), 201

    except ValueError as error:

        return jsonify({
            "cod": 400,
            "success": False,
            "detail": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "cod": 500,
            "success": False,
            "detail":
                "Internal blockchain error",
            "error": str(error)
        }), 500

@app.route(
    "/api/blockchain",
    methods=["GET"]
)
def get_blockchain():

    chain = (
        blockchain_service
        .get_chain()
    )

    return jsonify({
        "cod": 200,
        "length": len(chain),
        "chain": chain
    })


@app.route(
    "/api/blockchain/block/<int:index>",
    methods=["GET"]
)
def get_block(index):

    block = (
        blockchain_service
        .get_block(index)
    )

    if block is None:

        return jsonify({
            "cod": 404,
            "detail": "Block not found"
        }), 404

    return jsonify({
        "cod": 200,
        "block": block
    })


@app.route(
    "/api/blockchain/validate",
    methods=["GET"]
)
def validate_blockchain():

    valid = (
        blockchain_service
        .validate_chain()
    )

    return jsonify({
        "cod": 200,
        "valid": valid
    })

@app.route("/api/productivity/event", methods=["POST"])
def submit_productivity_event():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "producer_id",
        "activity",
        "crop",
        "quantity",
        "unit"
    ]

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:

        return jsonify({
            "cod": 400,
            "detail": "Missing required fields",
            "missing": missing
        }), 400

    try:

        quantity = float(
            data["quantity"]
        )

        if quantity <= 0:
            raise ValueError

    except (TypeError, ValueError):

        return jsonify({
            "cod": 400,
            "detail": (
                "quantity must be "
                "a positive number"
            )
        }), 400

    event = {
        "producer_id":
            str(data["producer_id"]),

        "activity":
            str(data["activity"]),

        "crop":
            str(data["crop"]).lower(),

        "quantity":
            quantity,

        "unit":
            str(data["unit"]),

        "metadata":
            data.get("metadata", {})
    }

    try:

        result = (
            blockchain_service
            .submit_productivity_event(
                event
            )
        )

        return jsonify({
            "cod": 201,
            "message":
                "Productivity event recorded",
            "result": result
        }), 201

    except ValueError as error:

        return jsonify({
            "cod": 400,
            "detail": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "cod": 500,
            "detail":
                "Unable to process productivity event",
            "error": str(error)
        }), 500
if __name__ == '__main__':
    app.run(host='localhost', port=8001, debug=True)  # Different port to avoid conflict
