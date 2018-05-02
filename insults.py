import markovify
import spacy
from flask import Flask, jsonify, Blueprint
from flask_restful import Resource, Api

nlp = spacy.load("en_core_web_sm")


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


with open("luther.txt") as f:
    luther = f.read()

with open("insults.txt") as f:
    insults = f.read()

with open("shakespeare.txt") as f:
    shakespeare = f.read()

text_model_luther = markovify.Text(luther, state_size=3)
text_model_insults = markovify.Text(insults, state_size=3)
text_model_shakespeare = markovify.Text(shakespeare, state_size=3)

model_combo = markovify.combine([text_model_luther, text_model_insults, text_model_shakespeare],
                                [1.5, 1, 1.2])

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


class Insult(Resource):
    @staticmethod
    def get():
        return jsonify(insult=model_combo.make_short_sentence(140, tries=25))


class Insults(Resource):
    @staticmethod
    def get():
        return jsonify(insult1=model_combo.make_short_sentence(140, tries=25),
                       insult2=model_combo.make_short_sentence(140, tries=25),
                       insult3=model_combo.make_short_sentence(140, tries=25),
                       insult4=model_combo.make_short_sentence(140, tries=25),
                       insult5=model_combo.make_short_sentence(140, tries=25))


api.add_resource(Insult, '/insult')
api.add_resource(Insults, '/insults')
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(port=5432, debug=True)
