import markovify
import spacy

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

model_combo = markovify.combine([text_model_luther, text_model_insults, text_model_shakespeare], [1.5, 1, 1.2])

print(model_combo.make_sentence(tries=10000))