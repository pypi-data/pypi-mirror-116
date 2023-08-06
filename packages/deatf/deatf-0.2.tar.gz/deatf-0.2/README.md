# DEATF

[![Python](https://img.shields.io/badge/Python-3.6-blue)]
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.5-green)](https://www.tensorflow.org/)
[![DEAP](https://img.shields.io/badge/DEAP-1.0-brightgreen)](https://deap.readthedocs.io/en/master/)

Distributed Evolutionary Algorithms in TensorFlow (DEATF) is a framework where networks generated with <a href="https://www.tensorflow.org/">TensorFlow</a> [[1]](#1) are evolved via <a href="deap.readthedocs.org/">DEAP</a> [[2]](#2). DEATF is a framework directly based in <a href="https://github.com/unaigarciarena/EvoFlow">EvoFlow</a> [[3]](#3) framework created by Unai Garciarena.

<p align="left">
<a href="https://github.com/deap/deap"><img src="https://repository-images.githubusercontent.com/20035587/2559bd00-9a75-11e9-9686-0697d18522cf" height=250 align="right" /></a>
<a href="https://www.tensorflow.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/2/2d/Tensorflow_logo.svg" height=250 align="left" /></a>
</p>

## Installation

DEATF has available an easy installation with pip.

```bash
pip install deap
```

## Requirements

TensorFlow
DEAP
NumPy
Tensorflow-database
ScikitLearn
Pandas

## Example

The easiest example of this library (taken from <a href="https://github.com/IvanHCenalmor/deatf/blob/main/examples/simple.py">simple.py</a> in the examples folder), where every used parameter is predifined is the following one:

```
import numpy as np

from deatf.auxiliary_functions import load_fashion
from deatf.network import MLPDescriptor
from deatf.evolution import Evolving

from sklearn.preprocessing import OneHotEncoder

x_train, y_train, x_test, y_test, x_val, y_val = load_fashion()

OHEnc = OneHotEncoder()

y_train = OHEnc.fit_transform(np.reshape(y_train, (-1, 1))).toarray()
y_test = OHEnc.fit_transform(np.reshape(y_test, (-1, 1))).toarray()
y_val = OHEnc.fit_transform(np.reshape(y_val, (-1, 1))).toarray()

e = Evolving(evaluation="XEntropy", desc_list=[MLPDescriptor], compl=False,
         x_trains=[x_train], y_trains=[y_train], x_tests=[x_val], y_tests=[y_val], 
         n_inputs=[[28, 28]], n_outputs=[[10]], batch_size=150, iters=10, 
         population=15, generations=10, max_num_layers=10, max_num_neurons=20,
         seed=0, dropout=False, batch_norm=False, evol_alg='mu_plus_lambda',
         evol_kwargs={'mu':10, 'lambda_':15, 'cxpb':0., "mutpb": 1.},
         sel = 'best')

a = e.evolve()
```

## References
<a id="1">[1]</a> 
Abadi, M., Agarwal, A., Barham, P., Brevdo, E., Chen, Z., Citro, C., ... & Ghemawat, S. (2016). Tensorflow: Large-scale machine learning on heterogeneous distributed systems. arXiv preprint arXiv:1603.04467.

<a id="2">[2]</a> 
Fortin, F. A., Rainville, F. M. D., Gardner, M. A., Parizeau, M., & Gagné, C. (2012). DEAP: Evolutionary algorithms made easy. Journal of Machine Learning Research, 13(Jul), 2171-2175.

<a id="3">[3]</a> 
Garciarena, U., Santana, R., & Mendiburu, A. (2018, July). Evolved GANs for generating Pareto set approximations. In Proceedings of the Genetic and Evolutionary Computation Conference (pp. 434-441). ACM.
