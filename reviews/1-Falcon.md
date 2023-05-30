# CS630 - Distributed Systems
## FALCON review

### Summary
This paper proposes a new reliable failure detection scheme, that unlike previous approaches, aims to achieve all three of the
desirable properties in failure detection methods: reliability, speed, and minimal resource usage and overhead.
The approach consists of plugging in "spy" programs into different layers of the system, specifically applications, operating
system, virtual machine monitor (VMM), and network switches.
Said spy programs are comprised of two entities: an enforcer and an inspector. Enforcers maintain communication with the client
library, while inspectors are responsible with monitoring the specific layer.
In order to ensure reliability, meaning predicting a service's status correctly, enforcers can also kill and restart the
attached layer in case the program cannot make a definitive conclusion about the layer's status.
Spies are also designed to work as a network, meaning each spy monitors its attached layer, as well as higher layers 
(i.e. OS spy also monitors application spies in the same environment.)
This approach is shown to have sub-second detection time, minimal resource usage, and high reliability. In addition, it is
claimed to be easy to integrate into existing systems with very few lines of code.
In addition, it is claimed that in certain scenarios, this system can replace complex coordination systems such as Paxos, due to
the level of detection reliability introduced.

### Opinion
It is a well-written paper, and the core idea is presented very clearly, although a bit verbose at times.
The idea is simple and easy to understand, but there are a few points that were unclear to me when reading, such as why the
"UP-INTERVAL" does not affect detection time.
Given that it's a relatively old paper, I'm sure it's applicability can simply be verified by how successful it has been over
the years, but I'll leave that to discussion in the class.
Finally, and this may be just me and not having enough background, but the presentation of experiments was a bit hard to follow.

### Strengths and Weaknesses

#### Strengths
If the claim that reliable failure detection hadn't been studied as much and thought to be not fully achievable / impossible
until this paper is true, that serves as one of the most important strengths of the paper.

As previously mentioned, the presentation is mostly clear, and the paper is very easy to follow. Interface, procedure, and
method pseudo-codes, and the simple language used in section 3 is a significant factor.

Experimental setup covers two different platforms with and without the proposed RFD system, and compares it to other failure
detection methods frequently used, and different failure/disruption scenarios and their respective detection and resulting
unavailability times.
The authors also provide CPU overhead measurements in different layers to support their viability claim.


#### Weaknesses
As stated in the paper, the experimentation setup is fairly limited, and not generalizable to practical scenarios without
thorough examination of its performance across different setups. For instance, their setup consisted of only natively run OSes
on 3 different hosts. This means that the problem size is very limited, and based on my understanding, the VMM spy's performance
is not reflected in the experiments (I could not find this discussed either.)
In addition to that, only a single combination of two platforms (ZooKeeper and PMP) are presented, which bears similar concerns.

A possible weakness in the approach (which I'm uncertain of) is that network failures aren't really addressed; meaning any
failure in the network falls back to end-to-end timeouts, which effectively means Falcon does not make any improvements towards
failures due to network-related issues. An example of that can be a faulty link between two switches, which may result in a
partitioned network, but one that is not reliably detected as such.

### Conclusion
Again, as stated in the paper, the experimentation setup is fairly limited, which is fine since this is an academic research
project. As a result, the practicality of Falcon can only be verified by more extensive experiments in real life scenarios.
Having said that, given that reliable failure detection was an overlooked concept due to the commonly held view that it is not
achievable, among the most important implications of this work have to be inspiring researchers to study the problem more.
Even if Falcon itself does not scale or show promise in larger scale environments, it is possible to continue improving upon the
foundations presented in this paper until eventually reliable failure detection is achieved in practice.


## Author
[Ali Hassani](https://alihassanijr.com)
