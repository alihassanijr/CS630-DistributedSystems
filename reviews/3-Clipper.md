# CS630 - Distributed Systems
## Clipper review

### Summary
This paper proposes a framework for deploying and serving ML models, aimed specifically to allow for a wide variety of ML
frameworks and at the same time attempting to increase efficiency and allow for creating model ensembles.
The proposed approach, dubbed Clipper, employs techniques such as output caching and adaptive batching to maximize ML inference
throughput. It also can be binded to multiple ML frameworks, such as Spark, TensorFlow, and Scikit-Learn with minimal effort.
ML models underneath are run in their own separate containers to handle dependency management, and are called via remote
procedure calls.
Clipper is evaluated from multiple aspects, including the effect of their proposed adaptive batching on latency, and accuracy
improvements from their model ensembles. Clipper is also compared to TensorFlow's existing serving component in terms of peak
throughput and mean latency.

### Opinion
My opinion may be slightly biased due to the fact that this paper is from 2017, and ML as a field in general, and ML platforms
and frameworks, are very different now compared to then.
That said, I take issue with a few claims in the paper.

The first and foremost is the claim to improved accuracy. The language in the paper suggests that Clipper is responsible for
improved accuracy in ML models, which is certainly not true. Model ensembling is a widely-used technique in general, and
accuracy improvements are, from my understanding, and expectation and not a guaranteed outcome.

The second is that while caching is claimed to be among the major contributions of this paper, it does not seem to be evaluated
as the rest of the components such as adaptive batching are.

In general, while the paper itself is well organized and well written, it is difficult to see significance in its contributions
or impact as an ML deployment platform, and there's limited detail on distributed systems aspect of it.

### Strengths and Weaknesses

#### Strengths
The motivation behind this paper is one that exists even today: deployment and serving of ML models in distributed set ups.
The differences between training and inference, and the fact that sometimes training is done in a research environment, leads to
the necessity for frameworks such as Clipper.

Abstraction of models, and ensuring different models are run in containerized environments is an approach still used today when
serving a variety of different models in a single platform.
Caching, while done at a very high level, is an interesting concept.
It reminds me of checkpointing, which is done in deep learning frameworks as a means to allow for model sharding across 
different devices, or in order to preserve main memory on a single device. Depending on whether or not the ML model in question
is a causal model, it can also be useful in that scenario.

#### Weaknesses
The most apparent issue to me is the domain in which the experiments were conducted.
For starters, the paper makes claims towards real-time ML applications such as recommendation systems, but such benchmarks are
not part of the experiments. Most experiments appear to be limited to image classification (referred to as object recognition
in the paper), which even at the time of publication was a relatively straightforward ML task. The second category is speech
recognition, but the experiments done in that direction are limited compared to the rest.
It might have been a better idea to study either vision in more depth, or a wider range of tasks with less detail but more
evidence highlighting the method's advantages.

Another is the motivation behind and experimentation regarding caching.
It is noted that caching frequent queries can effectively reduce latency, but there are no examples of such cases occurring,
specifically in the benchmarks presented in the paper.
It is simply unclear how useful Clipper's caching mechanism is going to be, given that repeated queries, at least to my
knowledge, are not very frequent in most ML platforms, and even so, the prediction caching is only going to be useful under very
specific assumptions (i.e. the same client submitting the same query repeatedly.)

Finally, experiments regarding dynamic batching are not very informative, given that batched inputs are not always going to
provide a higher throughput compared to non-batched inputs. That only happens to be the case when one can make assumptions about
the model, the input, type of hardware acceleration, and even software.
Not all ML/Linear Algebra routines are implemented alike, especially when considering different types of hardware, and their 
respective programming models.

### Conclusion

One of the major limitations discussed in the paper is treating models as black-box components, which means the execution of any
component considered a "model" will not be optimized. 
Although it is difficult to say whether or not frameworks such as Clipper are the appropriate layer in the stack where such
optimizations should take place.
A very recent and currently trending field of work is improving AI/ML models by creating better infrastructure, one that is
capable to minimize latency by both reducing the overhead that interfaces bear, as well as constructing better computational
graphs.

As for the experiments and results, they do not seem to conclude that Clipper offers any advantage over TensorFlow's API, other
than the fact that it is not limited to TensorFlow models alone. However, I don't find that this is necessarily an issue to be
taken with Clipper as a concept, rather with the presentation of the paper.
A common framework providing a serving interface for multiple ML frameworks is a valuable tool (HuggingFace is a good example of
that.)

## Author
[Ali Hassani](https://alihassanijr.com)
