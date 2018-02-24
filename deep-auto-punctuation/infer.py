"""
Perform inference on inputted text.
"""
import utils
import torch
from termcolor import cprint, colored as c
import model
import data

# get an edgt object
def get_edgt():
    input_chars = list(" \nabcdefghijklmnopqrstuvwxyz01234567890")
    output_chars = ["<nop>", "<cap>"] + list(".,;:?!\"'$")

    # torch.set_num_threads(8)
    batch_size = 128

    char2vec = utils.Char2Vec(chars=input_chars, add_unknown=True)
    output_char2vec = utils.Char2Vec(chars = output_chars)
    input_size = char2vec.size
    output_size = output_char2vec.size

    cprint("input_size is: " + c(input_size, 'green') + "; ouput_size is: " + c(output_size, 'green'))
    hidden_size = input_size
    layers = 1

    rnn = model.GruRNN(input_size, hidden_size, output_size, batch_size=batch_size, layers=layers, bi=True)
    egdt = model.Engadget(rnn, char2vec, output_char2vec)
    egdt.load('./data/Gru_Engadget_epch-24.tar')
    return egdt


def predict_next(source, in_edgt, gen_length=None, temperature=0.05):
    input_chars = list(" \nabcdefghijklmnopqrstuvwxyz01234567890")
    output_chars = ["<nop>", "<cap>"] + list(".,;:?!\"'$")
    input_text, punc_target = data.extract_punc(source, input_chars, output_chars)
    egdt = in_edgt
    egdt.model.batch_size = 1
    egdt.init_hidden_()
    egdt.next_([input_text])
    punc_output = egdt.output_chars(temperature=temperature)[0]
    result = data.apply_punc(input_text, punc_output)
    # capitalize letters after periods
    for char in result:
        if char == '.':


    print("\n" + result)


predict_next("In the next video in this series I'll be covering the benefits and drawbacks of scikit-learn as well as my recommended way to set up Python for machine learning In the meantime I'd love to hear from you in the YouTube comments if you have a question about machine learning or if you just have a cool example of machine learning that you'd like to share Please do subscribe on YouTube if you'd like to hear the moment my next video comes out Thanks for watching and I'll see you soon", get_edgt())