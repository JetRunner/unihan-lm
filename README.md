# unihan-lm
The official repository for "UnihanLM: Coarse-to-Fine Chinese-Japanese Language Model Pretraining with the Unihan Database", AACL-IJCNLP 2020

## Pretrained Model
The pretrained model is available at 🤗 Hugging Face Model Hub: https://huggingface.co/microsoft/unihanlm-base

## Unihan Clusters
We have made the code to find the Unihan clusters and the cached cluster IDs available [here](https://github.com/JetRunner/unihan-lm/tree/master/unihan).

## Training Code
Please follow our paper and use the training code from [facebookresearch/XLM](https://github.com/facebookresearch/XLM). 

1. Preprocess your corpus by replacing all characters with the first character in each [cluster](https://github.com/JetRunner/unihan-lm/blob/master/unihan/cached_clusters.py).
2. After cluster-level pretraining, copy the embedding of the first characters in each cluster for other characters in the same cluster.
```python
for cluster in clusters:
    for chracter_id in cluster[1:]:
        embedding.weight[chracter_id] = embedding.weight[cluster[0]].detach()
```
3. Re-preprocess the corpus by a standard procedure.
4. Restart training on the new corpus.

Note: XLM is released under a CC BY-NC 4.0 licence.
