#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define THREAD_DEPTH 4

struct Datum
{
    int class;
    float *x;
};
struct DecisionTreeClassifierNode
{
    float split_threshold;

    int partition_length;
    struct Datum *partition_pointer;

    struct DecisionTreeClassifierNode *left;
    struct DecisionTreeClassifierNode *right;
};
struct DecisionTreeClassifier
{
    int num_classes;
    int *classes;

    int num_features;
    int num_data;
    struct Datum *data;
};

