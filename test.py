import numpy as np
import tensorflow as tf

from keras.models import load_model

from conversation import conversation


Tokenizer = tf.keras.preprocessing.text.Tokenizer

pad_sequences = tf.keras.preprocessing.sequence.pad_sequences

tokenizer = Tokenizer(char_level=True, lower=True)
tokenizer.fit_on_texts(conversation)

# evaluation and generating sample text 
def generate_text(seed_text, model, tokenizer, sequence_length, num_chars_to_generate):
    generated_text = ''
    for _ in range(num_chars_to_generate):
        token_list = tokenizer.texts_to_sequences([seed_text])
        token_list = pad_sequences(token_list, maxlen=sequence_length, padding="pre")
        predicted_probs = model.predict(token_list, verbose=0)
        predicted_token = np.argmax(predicted_probs, axis=-1)[0]  

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_token:
                output_word = word
                break
        seed_text = seed_text + output_word
        generated_text += output_word

    return generated_text

modelF = load_model('model.h5')
seed_text = "Question: How can I find electric potential at a point?"
generated_text = generate_text(seed_text, modelF, tokenizer, 80, num_chars_to_generate=300)
print(generated_text)