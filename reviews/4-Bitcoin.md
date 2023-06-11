# CS630 - Distributed Systems
## Bitcoin review

### Summary
This paper introduces Bitcoin, a peer to peer monetary transaction system aimed at delivering a decentralized electronic cash
system.
It builds on existing concepts, such as assigning digital signatures to transactions and peer-to-peer consensus systems.
However, its primary contribution is resolving a key issue prohibiting such systems from being used as a reliable electronic 
cash system; double-spending.
The key technical contribution of the paper appears to be the proof-of-work mechanism, which is directly aimed at reaching
consensus and ultimately preventing double-spending.
Aside from the contributions, the paper provides insight into the likelihood of one rouge entity taking control of the system,
as well as expected growth in user storage.

### Opinion
This is obviously not a standard academic paper; despite being carefully written, and easy to understanding, with no outstanding
flaws in writing (something that cannot be said about even some successful academic papers), the structure and presentation
deviates from the typical paper. Aside from having enough background presented within the paper, it was difficult for me to get 
the entire picture without having to go back a few pages to confirm.
That said, if I was working in this field, I would probably find this paper much more interesting given that it only sticks to
necessary information.

### Strengths and Weaknesses
The primary contribution appears to be the proof-of-work solution, which is claimed to prevent double-spending in the system,
and more generally, achieving consensus.
Through this solution, the system can ensure consensus among the distributed ledgers that nodes maintain in the form of block
chains.

While the charts help clarify some of the concepts that are presented, the paper can be difficult to parse, 
since it is for the most part a technical report of a concept.
One of the biggest challenges when reading is that the methodology is broken into multiple sections, and so are topics that
would typically go under discussions. This is not a problem in itself, but because the sections vary in terms of the content
they present, stitching the concepts together to get the big picture is ultimately left up to the reader.

The only numbers presented aren't those of an implementation of the concept, but rather aim to provide evidence of the low
likelihood that attackers can affect the outcome of the system by alternating or faking transactions or chains.

### Conclusion
Proof-of-work should be applicable to systems beyond the one presented in this paper.
Arguably any peer-to-peer network with distributed ledgers should be able to employ the same concept in order to reach consensus
in unreliable networks, whether due to bad actors or other such examples.

One key implication, which goes beyond the objectives of the platform and was therefore not mentioned in the paper, is the
impact that proof-of-work would ultimately have on resource consumption and the environment.
Any meaningful application of proof-of-work should include a considerably large set of nodes, or more specifically, CPU cores,
voting to reach consensus. The problem is that said cores are constantly spinning to solve for their appropriate hash, and this
automatically means consumption of power. More users equals possibly a number of times more transactions, and more transactions
leads to more cores actively trying to solve proof-of-work, which can quickly grow into massive power usage across the network.
If widely adopted around the world, it is not unlikely that these nodes will account for a considerable growth in energy
consumption, and therefore environmental issues.

## Author
[Ali Hassani](https://alihassanijr.com)
