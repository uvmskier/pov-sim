from flask import Flask, jsonify
from flasgger import Swagger
from utils import get_random_int

from opentelemetry import trace

app = Flask(__name__)
Swagger(app)

#adding tracing
tracer = trace.get_tracer("custom_flight.tracer")

AIRLINES = ["AA", "UA", "DL"]

@app.route("/")
def home():
    """No-op home endpoint
    ---
    responses:
      200:
        description: Returns ok
    """
    return jsonify({"message": "ok"})


@app.route("/airlines/<err>")
def get_airlines(err=None):
    """Get airlines endpoint. Set err to "raise" to trigger an exception.
    ---
    parameters:
      - name: err
        in: path
        type: string
        enum: ["raise"]
        required: false
    responses:
      200:
        description: Returns a list of airlines
    """
    if err == "raise":
        raise Exception("Raise test exception")
    return jsonify({"airlines": AIRLINES})

@app.route("/flights/<airline>/<err>")
def get_flights(airline, err=None):
    """Get flights endpoint. Set err to "raise" to trigger an exception.
    ---
    parameters:
      - name: airline
        in: path
        type: string
        enum: ["AA", "UA", "DL"]
        required: true
      - name: err
        in: path
        type: string
        enum: ["raise"]
        required: false
    responses:
      200:
        description: Returns a list of flights for the selected airline
    """
    if err == "raise":
        raise Exception("Raise test exception")
    
    #custom span for step 1.1
    with tracer.start_as_current_span("generate_random_int_for_flight_number") as span:
        random_int = get_random_int(100, 999)
        span.set_attribute("random_int", random_int)
        span.set_attribute("airline",airline)
    return jsonify({airline: [random_int]})
if __name__ == "__main__":
    app.run(debug=True)
