---
title: PNA Graph Neural Networks
description: A practical introduction to Principal Neighbourhood Aggregation and why multiple aggregators help graph neural networks learn richer structural signals.
---

# PNA graph neural networks: learning more from every neighbourhood

*25 October 2026 · 8 min read*

Graph neural networks learn by passing information between connected entities. In a molecular graph, atoms exchange information with bonded neighbours. In a protein interaction network, proteins collect signals from their interaction partners. The central operation seems simple: gather messages from a node's neighbourhood and combine them into a new representation.

That combination step is also a bottleneck. If a model compresses an entire neighbourhood with a single statistic, useful structure can disappear. Principal Neighbourhood Aggregation, usually shortened to PNA, addresses this limitation by combining several aggregators and adjusting their outputs according to node degree. The result is a graph neural network layer that can retain a richer description of local structure.

## The limits of a single aggregator

Most message-passing graph neural networks follow the same pattern. Each neighbour produces a message, the messages are aggregated, and the result updates the central node. Different architectures often distinguish themselves through the aggregation function they choose.

A mean aggregator describes the average message but ignores neighbourhood size. Two nodes can therefore receive the same mean even when one has two neighbours and the other has twenty. A sum preserves information about scale and multiplicity, but it can mix together neighbourhoods with different distributions. A maximum highlights the strongest signal while discarding almost everything else.

None of these operations is universally wrong. Each simply answers a different question. The mean describes a centre, the maximum and minimum describe extremes, and the standard deviation describes spread. PNA begins with the observation that a graph layer should not have to choose only one of them.

## The core idea behind PNA

PNA was introduced by Gabriele Corso, Luca Cavalleri, Dominique Beaini, Pietro Liò, and Petar Veličković at NeurIPS 2020. Their analysis extends questions about GNN expressivity to continuous node features and motivates the use of multiple aggregation functions.

For every node, a PNA layer first computes messages from its neighbours. It then summarizes those messages in several ways, commonly using the mean, maximum, minimum, and standard deviation. These summaries are concatenated rather than collapsed into one statistic.

In compact form, the operation can be viewed as:

**neighbour messages → multiple aggregators → degree scalers → learned transformation**

The combined representation tells the next stage of the network more than any individual aggregator could. It captures the typical signal, its variability, and its range. A learned transformation then decides which parts matter for the task.

## Why node degree matters

Aggregation is affected by the number of neighbours a node has. A sum usually grows with node degree, while a mean deliberately removes that information. Real graphs, however, often contain both sparsely connected and highly connected nodes, and degree can itself be meaningful.

PNA uses degree scalers to amplify, preserve, or attenuate aggregated signals according to neighbourhood size. The original formulation includes identity, amplification, and attenuation scalers based on a logarithmic degree transformation normalized by the average degree in the training data.

This mechanism gives the model several views of the same aggregated signal. One view is unchanged. Another emphasizes high-degree neighbourhoods. A third reduces their relative magnitude. Instead of imposing a single treatment of degree, PNA gives the network options and lets training determine how to use them.

The degree distribution used for normalization must come from the training graphs. This is an important implementation detail: using validation or test data would leak information, while using a poorly matched distribution can make the scalers less useful.

## A molecular example

Consider two carbon atoms in different molecular environments. Both may have neighbouring atoms whose learned features have the same average value. A mean-based GNN could produce identical aggregated messages for them, even if one carbon is attached to a tightly clustered set of similar atoms and the other has chemically diverse neighbours.

PNA can separate these cases. The standard deviation records diversity in the neighbourhood, the minimum and maximum capture extremes, and degree scaling preserves information related to coordination. These signals do not replace chemically meaningful atom and bond features, but they give the model a more expressive way to combine them.

This is one reason PNA is attractive for molecular property prediction. Molecular graphs are irregular, local structure matters, and small differences in bonding context can influence the property being predicted. The original paper reported particularly strong results on the ZINC molecular benchmark, while gains were smaller on image-derived graphs with regular neighbourhood structure.

The distinction is instructive. PNA is most valuable when neighbourhood statistics and degree variation carry useful information. It is not automatically the best choice for every graph-shaped dataset.

## Expressivity comes with a cost

PNA produces multiple aggregator–scaler combinations. If four aggregators are paired with three scalers, the layer creates twelve neighbourhood summaries before the learned mixing step. This increases feature width, memory use, and computation compared with a simple mean or sum layer.

That trade-off is often worthwhile when local graph structure is complex, but it should be measured rather than assumed. A sensible experiment compares PNA against a strong, simpler baseline under the same parameter budget and training protocol. Ablations can then reveal whether multiple aggregators, degree scalers, or both are responsible for an improvement.

PNA also remains a local message-passing architecture. Multiple aggregators make each local summary richer, but they do not eliminate familiar GNN challenges such as over-smoothing in deep networks, over-squashing across bottlenecks, or limited access to long-range dependencies.

## Practical design choices

A robust PNA model starts with reliable input features and a training-set degree histogram. Edge features should be included in message construction when relationships carry information, as chemical bonds do. Residual connections, normalization, dropout, and a task-appropriate graph readout can be as important as the convolution itself.

The default combination of mean, minimum, maximum, and standard deviation is a good starting point. More aggregators are not necessarily better: redundant statistics increase cost and may encourage overfitting. The same caution applies to depth. Begin with a modest number of layers, validate carefully, and expand only when the task benefits.

Evaluation should respect the data-generating process. For molecular datasets, scaffold-aware or otherwise domain-appropriate splits often provide a more realistic estimate of generalization than an unconstrained random split. Report variability across runs and compare models with similar capacity whenever possible.

## When should you use PNA?

PNA is a strong candidate when graphs have heterogeneous degrees, when the distribution of neighbouring features matters, and when subtle local structural differences drive the target. Molecular graphs, interaction networks, knowledge graphs, and physical systems can all fit this profile.

A simpler convolution may be preferable when graph topology is highly regular, compute is constrained, or a baseline already captures the relevant signal. The best reason to choose PNA is not that it is more elaborate; it is that the task benefits from preserving several complementary views of each neighbourhood.

## The broader lesson

PNA makes a useful point about graph learning: aggregation is not merely a technical detail between message construction and node updates. It determines what information survives as a neighbourhood is compressed into a fixed-size vector.

By combining measures of centre, spread, and extremes with degree-aware scaling, PNA gives graph neural networks a fuller local vocabulary. For life-science applications, where small structural changes can have large biological consequences, that richer vocabulary can be especially valuable.

Read the original paper: [Principal Neighbourhood Aggregation for Graph Nets](https://papers.neurips.cc/paper_files/paper/2020/hash/99cad265a1768cc2dd013f0e740300ae-Abstract.html).
