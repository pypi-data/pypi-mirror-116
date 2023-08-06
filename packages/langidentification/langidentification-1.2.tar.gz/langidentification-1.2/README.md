# langidentification: Language identification using fastText for Romanized South Asian and Arabic Scripts

This package is a language detector built using fastText with the objective of identifying languages written in 
non-native romanized scripts. There are two models supported in this package: `original` and `augmented`. 

The `original` model was trained on freely 
available data found on the [Tatoeba website](https://tatoeba.org/en/downloads). It is trained for 105 languages 
for which at least 100 sample sentences were present in the data.

The `augmented` model was trained on all the data used for the `original` model with the addition of three more datasets:
* The [Dakshina Dataset (romanized sentences)](https://github.com/google-research-datasets/dakshina), with Wikipedia 
  sentence data representing 12 South Asian languages: Bengali (`bn`), Gujarati (`gu`), Kannada (`kn`), 
  Malayalam (`ml`), Sinhala (`si`), Tamil (`ta`), Telugu (`te`), Hindi (`hi`), Marathi (`mr`), Punjabi (`pa`), 
  Urdu (`ur`) and Sindhi (`sd`)
* The [Tunisian Arabizi Dialectal Dataset](https://aclanthology.org/2021.wanlp-1.25.pdf), representing Tunisian 
  Arabic, which displays frequent use of French loanwords
* The [Arabizi Identification in Twitter Data dataset](https://aclanthology.org/P16-3008.pdf), representing Egyptian 
  and Lebanese Arabic, which have some use of English and French loanwords

Although built using fastText, these models **are not comparable** to the official 
[fastText models](https://fasttext.cc/docs/en/language-identification.html), which are built on more data than the 
Tatoeba dataset. These models are however capable of identifying romanized South Asian language and Arabic (`ar`) text 
with the suffix `-rom`.

## Model Performance

|Model|Precision|Recall|F1 score|
|---|---|---|---|
|**original**|0.79|0.65|0.65|
|**augmented**|0.75|0.66|0.66|

## Installation

```
pip install langidentification
```

## Usage
Valid `model_type`s are `original` and `augmented`. The `augmented` model is capable of making romanized language 
predictions.

Both models are hosted on [GitHub releases](https://github.com/absu5530/langidentification/releases) and are downloaded 
at runtime if not found.

```
>>> from langidentification import LangIdentification
>>> model = LangIdentification(model_type='augmented')
INFO:root:Model langdetect_augmented.ftz was not found. Checking for models directory and creating if not available...

INFO:root:Downloading langdetect_augmented.ftz...

100% [......................................................................] 276567331 / 276567331INFO:root:Loading model langdetect_augmented.ftz...

>>> model.predict_lang('ithu velai seyyuma?')
(('__label__ta-rom',), array([0.87046105]))
```

## What is fastText and how were these models built?

fastText is the implementation of a text embedding method presented in 
[Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) by Bojanowski et al. 

This method is an enhancement of the Word2vec skipgram model which attempts to learn a vector representation for every 
word by training it to predict other words that appear in the context of the given word. The objective of the skipgram 
model is to find a set of parameters, i.e. word vectors, such that the likelihood of observing a certain context word 
given a certain target word is maximized.

fastText builds on the skipgram model by representing words as a sum of the vector representations of their constituent 
character n-grams and training with the goal of independently predicting the presence of context words. "Positive" 
examples, being the actual context words, and "negative" examples, being other words randomly drawn from the vocabulary, 
are used to train on.

For example, in the sentence `She is a pretty cat.`, if the target word is `pretty`, over the course of training, the 
vector representation for `pretty` should evolve to be closer to the representations for the words `a` and `cat` and 
further from other randomly sampled words, such as `computer` or `dirt`. As the word vector for `pretty` is adjusted 
during this process, so are the constituent character n-gram vectors, e.g. for `pre`, `etty` and `rett`.

The intuition here is that training subword representations helps to more accurately capture nuances in word morphology.

The character n-grams used for the models in this package are between two and four characters long. The vector 
representations learned are in 50 dimensions.

The models were quantized to make them smaller and faster at inference time. 

## What is quantization?

Quantization ([relevant SciPy modules](https://docs.scipy.org/doc/scipy/reference/cluster.vq.html)) is a process by which the embedding vectors (n vectors x 
d dimensions) are split into m distinct subvectors (n vectors x d/m dimensions), and then a k-means clustering algorithm 
is run on each of those subvectors. In doing so, a set of centroids (k clusters x d/m dimensions) is identified for each 
subvector.

This set of centroids acts as the encoding with which to transform the original word vectors (n vectors x d dimensions) 
into quantized vectors (n vectors x m dimensions). For each one of m subvectors, each of the original word vectors 
is classified with the cluster number or centroid index of the centroid closest to it. In this way, each word gets 
assigned m values, producing a final matrix of n vectors x m dimensions.
