# Spam filter manual

To test how well a naïve Bayes classifier _could_ fare against our spambot, 
we created this very simple classifier based on coursework in the University of Helsinki Introduction to Artificial Intelligence
course (DATA 15001). For example, files [cell_1_generated_results.txt](https://github.com/thalvari/SpamReviewGenerator/blob/master/spamfilter/cell_1_generated_results.txt)
and [cell_1_real_results.txt](https://github.com/thalvari/SpamReviewGenerator/blob/master/spamfilter/cell_1_real_results.txt) contain example test output based on 
datasets [cell_1_4_100.txt](https://github.com/thalvari/SpamReviewGenerator/blob/master/generated_samples/cell_1_4_100.txt) 
and [cell_1_sample_100.txt](https://github.com/thalvari/SpamReviewGenerator/blob/master/datasets/cell_1_sample_100.txt), respectively. 
Conclusions and more detailed analysis of results can be found in the [project report](https://github.com/thalvari/SpamReviewGenerator/blob/master/docs/project_report.md).

To run your own classifications tests, do the following (Unix shell assumed):

```shell
javac Spamfilter.java
java Spamfilter < examples.txt > output.txt
```

Note that the input file is assumed to contain sentences ending with a full stop ".", to be able to separate the sentences from each other.
