from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

app = Flask(__name__)

# 1. Έναρξη Spark Session μέσα στο API
spark = SparkSession.builder.appName("TelecomAPI").getOrCreate()

# 2. Φόρτωση του αποθηκευμένου Pipeline
# Το PipelineModel περιλαμβάνει αυτόματα τους Indexers και τον Assembler
model = PipelineModel.load("model/models/monthly_charges_model")

@app.route('/predict', methods=['POST'])
def predict():
    # 3. Λήψη δεδομένων (JSON) από το Streamlit
    data = request.json
    
    # 4. Μετατροπή των δεδομένων σε Spark DataFrame
    # Προσοχή: Τα ονόματα των κλειδιών πρέπει να είναι ίδια με τις στήλες του μοντέλου
    input_df = spark.createDataFrame([data])
    
    # 5. Πρόβλεψη μέσω του Pipeline
    prediction_df = model.transform(input_df)
    
    # 6. Εξαγωγή της τιμής
    result = prediction_df.select("prediction").collect()[0][0]
    
    return jsonify({"predicted_charges": round(float(result), 2)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)