from flask import Flask, render_template, request, jsonify
from Main_Processing import FinBot
import pickle
import os
app = Flask(__name__)

bot = FinBot()

details_check = False
acc_no_check = False

@app.route("/")
def index_get():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    global details_check
    global acc_no_check
    data = request.get_json().get("message").lower()
    if acc_no_check:
        try:
            acc_no=data
            if acc_no:
                response = bot.analyze_transaction_density(int(acc_no))
                acc_no_check=False 
                return jsonify({'answer': response})
        except ValueError:
                return jsonify({"answer": "Please provide the proper account number or your account number doesnt exists in our system"})
        
    if details_check:
        try:
            acc_no,yr = data.split(",")
            acc_no = acc_no.strip()
            yr = yr.strip()
            if acc_no and yr:
                response = bot.predict_balance(acc_no, yr)
                details_check = False  
                return jsonify({"answer": response})
            else:
                return jsonify({"answer": "Please provide both account number and year"})
        except ValueError:
            return jsonify({"answer": "Please provide the input in 'account number,year' format"})
    current_dir = os.path.dirname(__file__)
    file_path_vectorizer = os.path.join(current_dir, 'Models','vectorizer.sav')
    file_path_txt_analyzer = os.path.join(current_dir, 'Models', 'inp_checker.sav')
    vectorizer = pickle.load(open(file_path_vectorizer, "rb"))
    txt_analyzer = pickle.load(open(file_path_txt_analyzer, "rb"))
    inp = vectorizer.transform([data])
    prediction = "".join(txt_analyzer.predict(inp))

    if prediction == "greet":
        response = bot.greet()
    elif prediction == "exit":
        response = bot.exit_pro()
    elif prediction == "balance evolution":
        response = bot.balance_evolution()
    elif prediction == "transaction density":
        acc_no_check = True
        response = "Please provide the account number"
        
    elif prediction == "predict balance":
        details_check = True
        response = "Please provide the account number and year separated by ','"
    elif prediction == "random":
        response = bot.no_match()
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)

