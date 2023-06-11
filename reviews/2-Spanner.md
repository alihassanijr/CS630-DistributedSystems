# CS630 - Distributed Systems
## Spanner review

### Summary
This paper proposes Spanner, a globally distributed database system that not only ensures strong consistency, but strong 
external consistency as well, which is crucial in distributed databases. Spanner controls consistency through version
timestamps, and handles clock uncertainty through a new infrastructure and API called TrueTime. Given certain assumptions, such
as the existence of GPS and atomic clocks on site, and frequent synchronization, TrueTime can ensure clock consistency through
timestamps without using Lamport or vector clocks. Spanner utilizes a two-phase commits with locks, but the timestamp versioning
allows lock-free reads, making exceedingly efficient in reads.
Spanner also uses Paxos for replication consistency.

### Opinion
The paper was well-written, the basic ideas were presented well, and the experiment setup specifically was straightforward, easy
to analyze and easy to understand.
In particular, I found TrueTime and the multi-version control very intuitive and interesting, given that I see very slight 
similarities between it and version control systems (again slight, given that to my knowledge commit hashes in VC are not
comparable, but setting that aside and handling order through commit trees, the core underlying idea is similar in that
consistent reads can be done based on a specific version, and can be done lock-free.)

### Strengths and Weaknesses
One of the most significant contributions in this paper is TrueTime and the resulting clock consistency with minimal wait time.
Ensuring clock consistency allows versioned data through timestamps, leading to many benefits such as the ease of inferring 
causality, and therefore achieving consistency and external consistency. It also allows for lock-free reads, which is
especially important in large-scale databases with more frequent reads than writes (content providers).
TrueTime measures time bounds based on clock drift models, and forces commits to wait the length of the bounds, which results in
consistent timestamps at the cost of the wait time.
However, by modeling clock drift on different nodes, and setting up clock update time intervals accordingly, and of course
maintaining reliable clock servers on site and measuring in round-trip time, they are able to minimize the likelihood of 
drifts exceeding a specific threshold, which in turn minimizes the likelihood of the commit wait time exceeding a relatively low
threshold.

The semi-relational storage model can be treated as both a No-SQL style key-value store, as well as a standard relational
database, effectively eliminating any barrier to entry for clients.

In addition, the non-blocking schema change being modeled as a typical transaction in the future, which leads to minimal
disruption of service, is a really significant improvement over the formerly used Bigtables.

Paper being from Google, their experiments are done in very practical scenarios. For example, they slowly migrated an
advertising service, F1, from the former standard, Bigtables, to Spanner.
F1 had originally been developed with MySQL, and due to its strong dependence on transactional semantics were unable to migrate
to NoSQLs and as a result scale better. 

### Conclusion
Given the significance of what was achieved in this paper, and its apparent success in migrating Google's F1 service, it would
be no surprise that Google would start migrating other services' database elements to Spanner, and also provide it as a cloud
service to clients. The paper being relatively old, upon looking it up, that does appear to be the case.

That said, another implication of this work is how distributed systems engineers address concurrency control and achieve
consistency in transactional systems. While TrueTime is only applicable in certain settings (i.e. requires a dedicated clock
server in every data center), and this would limit its ability to be as widespread, it would not be surprising if other cloud
provides and data centers started working on the infrastructure for this, so that in the event that they come up with their own
version of TrueTime, or possibly an open source version, they would be able to provide the infrastructure for it as well.

## Author
[Ali Hassani](https://alihassanijr.com)
