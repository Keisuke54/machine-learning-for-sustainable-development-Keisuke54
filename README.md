# PhysiGPT

## Background
In recent days, many large language models (LLMs) are being published, but a lot of forefront models are with subscription. There is a growing concern that the financial accesibility to those potential learning materialw will bring a huge inequality in education. Hence, this project aims to achieve a cost-free (+ open source) model that specializes in AP Physics C to support people's learning. 

### SDG's goal: **Quality Educaiton**

# File description
 `DataGeneration.py` contains training data generation through amplifying initial questions and answering to them via Cohere API
 `conversation.py` is the original ouput from running `DataGeneration.py`
 `conversation2.py` is the inspected version of `conversation.py` which removed conversations that seemed to cause inaccuracy
 `LLM.py` contains the architecture and training of the main language model 
 `test.py` contains testing attempts of the language model from `LLM.py` 
 `PhysiGPT.py` contains the final system for this project 

## System details
The system included in this repository is speech to text (voice recognition), the main language model about AP Physics C, and text to speech to achieve Q&A expereince for physics concepts. 

* ### What it does
You speak out your AP Physics C question to the model. The model understands the speech and responds to your question by speeaking out. 

* ### How it works
The model recognizes speech via OpenAI's Whisper speech recognition model and outputs text 
The converted text is passed through the langauge model and get the response
The response is then converted into speech via Google's Text-to-Speech model 

* ### How to install it + How to use it
Given the limitation in time to work, there is no real time Q&A app to downlod yet. You first download the trained model 'model.h5', and save your recording in mp3 file (or other file formats Whisper accepts). Run 'PhysiGPT.py' file in this repository to get the output speech. 

## Model Details
The main large language model is built with karas sequential model consisting of Embedding, two LSTM, and Dense layers. The first layer is an embedding layer that takes the input sequence and maps each word to a 32-dimensional vector. The second and third layers are LSTM (Long Short-Term Memory) layers that models long-term dependencies in a sequence by selectively retaining from previous time steps. The fourth layer is a dense layer that outputs a probability distribution over the vocabulary of the model.

The idea of this sequantial model was inspired by the [work by Franz Geffke](https://f-a.nz/dev/develop-your-own-llm-like-chatgpt-with-tensorflow-and-keras/).

The input sequence is a collection of lists that contains numbers that each corresponds to each character from one index in a text to a certain distance. the The ouput sequence is a collection of numbers that each corresponds to the next character to each input data, as shown below.
```
"Apple" --> input = [Ap, pp, pl], output = [p, l, e]
input_sequence = [[2, 1], [1, 1], [1, 3]], output_sequence = [1, 3, 4]
```
Each character is converted into sequence using tokenizer. 

## Data sources used for training
As shown in 'DataGeneration.py' file, the training data was generated by first amplifying the initial prompts a certain number times by passing them to `command-nightly` model from Cohere using API, and then answering all the original and amplified questions by passing them to `command-nightly` model from Cohere using API again. After the conversations were generated, I roughly inspected the file and removed the conversations that seemed to be irrelevent or cause inaccuracy. 

## Design process + Stages of development
The initial idea was to train the language model with a single conversation and train with new conversations on top of the previous model. However, all the trials seemed to get trained only for the last datum/conversation, or the training time was not logical for the accuray achieved. Hence I merged the sequences for all the data/conversations to one arrary to train the model in a single time. 

Setting random seed when training the model to make it reproducable was not the right idea. It made the model respond the same thing no matter what the prompts is, so the seed blocked randomness in the model's response too. 

## Model performance
The language model trained specific for AP Physics C returns complete sentences in most trials, but it can sometimes be a broken repitiion of words. Also, although the sentences are compelte, the content of the responses are far away from the exact answer, as shown below.
```
Prompt: How can I calculate torque? 
Response: at a simple harmonic motion pendulum are the initial angle of displacement from a reference point being directly proportional area
c is the coil's length
and would be perpendicular to the surface.
gous at the roltage, and it acts along the line joining the two objects.
whic enertric field intensity around a closed surface is equal to the net electric charge inside the surface. gauss' law for ligh
```
This is mainly beacause of the lack of training data, but it seems that it's not always the case. When the model was trained with more dataset, the accuracy did not improve. The ouput began with more reasonable starting words but the following characters/words became worse, such as repeating the same words infinitely. 

In addition, when generating a response, the model does not recognize when to complete the sentence from a given number of characters to generate. This causes the response to be cut in the middle, start generating unnecessary content, or repeating the same words. 

## Future work
* Exploring the tradeoff between the logical starting words and the accuracy of the model when changing the number of training data
* Exploring different model architecture
* Exploring how to complete sentence with a given number of character to generate
* Making an app for PhisiGPT for real time Q&A experience 