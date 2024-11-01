# CSC4160 Assignment-1: EC2 Measurement (2 questions)

### Deadline: 23:59, Sep 22, Sunday
---

### Name:郑立
### Student Id:120090155
---

## Question 1: Measure the EC2 CPU and Memory performance

1. (1 mark) Report the name of measurement tool used in your measurements (you are free to choose any open source measurement software as long as it can measure CPU and memory performance). Please describe your configuration of the measurement tool, and explain why you set such a value for each parameter. Explain what the values obtained from measurement results represent (e.g., the value of your measurement result can be the execution time for a scientific computing task, a score given by the measurement tools or something else).

    > My measurement tool is benchmark. 

    >For cpu performance, I use the command"sysbench cpu --threads=4 --cpu-max-prime=10000 run" to test the cpu performance. 
        >Why prime number counting is a reasonable CPU performance test?:
            Prime number computations are integer-based operations that involve a lot of division and modulo 
            operations. These operations rely heavily on the CPU's integer unit, and while prime number calculations are primarily integer operations, other CPU       
            performance tests related to floating point tend to be proportional to integer performance. Therefore, by testing integer operations, it is often possible to
            roughly infer the performance of floating-point operations as well. Therefore, it is possible to evaluate how efficiently a CPU handles integer arithmetic.
        >why threadnumber=4?:t3.medium,m5.large,c5d.large all have 2 vcpu, thus by using the threadnumber=4 we can fully utilize all cores to make a relative fair
            comparison.
        >What the values obtained from measurement results represent?:
            there are many measurement values in the output but we only choose the "events per second". for example: "event per second: 2000". This value represent the
            number of events (operations) performed per second during the test. 

    >For memory performance, I use the command"sysbench --test=memory --threads=4 --memory-total-size=10G --memory-oper=write --memory-scope=global run"
        >Why this is a reasonable memory performance test?:
            Two key factors in memory performance are read and write speeds. Read and write speeds determine how fast a system's response time can be when processing large amounts of data. Typically, writes take more time than reads, so specializing in write performance provides a better understanding of the system's performance bottlenecks.
        >why memory-total-size=10G: This parameter fully utilizes most of the system's memory resources, especially on large-memory EC2 instances such as m5.large and
            c5d.large. 
        >why num-threads=4:  This can be a good way to evaluate the memory performance for multi-core CPU scenarios.
        >why memory-scope=global:  sets the memory scope to "global". This means that all threads will access a shared memory region, thus testing the performance of
            parallel accesses to the same memory region under multiple threads.
        >what the values obtained from measurement results represent?:
            We use"operations per second"as our measurement,because it directly linearly reflects the writing speed of memory.



2. (1 mark) Run your measurement tool on general purpose `t3.medium`, `m5.large`, and `c5d.large` Linux instances, respectively, and find the performance differences among them. Launch all instances in the **US East (N. Virginia)** region. What about the differences among these instances in terms of CPU and memory performance? Please try explaining the differences. 

    In order to answer this question, you need to complete the following table by filling out blanks with the measurement results corresponding to each instance type.

    | Size      | CPU performance | Memory performance |
    |-----------|-----------------|--------------------|
    | `t3.medium` |     1707.25   |  6771544.83        |
    | `m5.large`  |     1639.35   |  7038248.94        |
    | `c5d.large` |     1916.59   |  8247216.75        |

    > Region: US East (N. Virginia)

## Question 2: Measure the EC2 Network performance

1. (1 mark) The metrics of network performance include **TCP bandwidth** and **round-trip time (RTT)**. Within the same region, what network performance is experienced between instances of the same type and different types? In order to answer this question, you need to complete the following table.  

    | Type          | TCP b/w (Mbps) | RTT (ms) |
    |---------------|----------------|----------|
    | `t3.medium`-`t3.medium` |       4930            |   0.329     |
    | `m5.large`-`m5.large`   | 4960(9530 at night)   |   0.160     |
    | `c5n.large`-`c5n.large` |         4960          |   0.162     |
    | `t3.medium`-`c5n.large` |       4910            |   0.676     |
    | `m5.large`-`c5n.large`  |         4950          |   0.540     |
    | `m5.large`-`t3.medium`  |         4950          |   0.151     |

    > Region: US East (N. Virginia)

2. (1 mark) What about the network performance for instances deployed in different regions? In order to answer this question, you need to complete the following table.

    | Connection | TCP b/w (Mbps)  | RTT (ms) |
    |------------|-----------------|--------------------|
    | N. Virginia-Oregon |       1230          |      58.797              |
    | N. Virginia-N. Virginia  |     4960      |      0.656               |
    | Oregon-Oregon |        4960         |           0.135        |

    > All instances are `c5.large`.

