from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime
import hashlib


import model_helper as mh
import cassandra_helper as ch


MODEL_FILE_PATH = r"./model_saved"
DATABASE_FILE_PATH = ""
OUTPUT_PATH =""

app = Flask(__name__)
model = mh.load_model(MODEL_FILE_PATH)


@app.route("/")
def index():
    return render_template('index.html', title='Sumbit Page')


@app.route("/view_classifier")
def classifier():
    comments = ['''Every once in a while a movie comes, that truly makes an impact. Joaquin's performance and scenography in all it's brilliance. Grotesque, 
    haunting and cringy. Hard to watch at times,... but so mesmerizing, you won't blink an eye watching it. Tragic, but with seriously funny moments. 
    Emotional rollercoaster - sometimes, with multiple emotions popping-up at the same time. 
    this is far from a typical action-riddled predictable super-hero movie - it's a proper psychological thriller/drama, with the single best character development I have ever seen.''']
    input_tensor = mh.Text_to_Tensor_converter(comments)
    predict_result = model.predict(input_tensor)
    result = mh.result_converter(predict_result)
    result_dict = {}
    for text in comments:
        sha1hash = hashlib.sha1()
        sha1hash.update((text.encode("utf-8")))
        result_dict[sha1hash.hexdigest()] = {"comment" : text ,"class" : result}
    return jsonify(result_dict)


@app.route("/classify", methods=['POST'])
def classifier_comment():
    print('Hi')
    if request.method == 'POST':
        comment = request.form['Comment']
        comments = [comment]
        input_tensor = mh.Text_to_Tensor_converter(comments)
        predict_result = model.predict(input_tensor)
        result = mh.result_converter(predict_result)
        result_dict = {}
        sha1hash = hashlib.sha1()
        sha1hash.update((comment.encode("utf-8")))
        hashvalue = sha1hash.hexdigest()
        currenttime = datetime.now()
        result_dict = {"hashvalue" : hashvalue, "comment" : comment ,"class" : result, "time" : currenttime}
     
        ch.Insert(hashvalue, comment, result, currenttime, "predicted_comment_table")

    return render_template('classify.html', hashvalue=result_dict['hashvalue'], comment=result_dict['comment'], Class=result_dict['class'], submit_time=result_dict['time'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)