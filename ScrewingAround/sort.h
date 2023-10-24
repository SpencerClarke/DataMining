#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <stdio.h>

struct merge_data
{
	int *A;
	int n;
	int *swap_mem;
	int thread_depth;
};
void merge_sort(int *A, int n, int thread_depth);
void *_merge_sort(void *merge_thread_data);
void _merge_sort_2(int *A, int n, int *swap_mem);

void f_merge_sort(float *A, int n, int thread_depth);
void *_f_merge_sort(void *merge_thread_data);
void _f_merge_sort_2(float *A, int n, int *swap_mem);

void merge_sort(int *A, int n, int thread_depth)
{
	int *swap_mem;
	pthread_t thread;
	struct merge_data data;
       	swap_mem = (int *)malloc(sizeof(int) * n); /*One memory allocation instead of making 2 temp arrays per call*/
	if(!swap_mem)
	{
		printf("merge_sort: Failed to allocate memory\n");
		exit(4);
	}
	data.A = A;
	data.n = n;
	data.swap_mem = swap_mem;
	data.thread_depth = thread_depth;

	pthread_create(&thread, NULL, _merge_sort, (void *)&data);
	pthread_join(thread, NULL);

	free(swap_mem);
}
void *_merge_sort(void *arg)
{
	int r_offset, l_offset;
	int mid;
	int i;
	struct merge_data data_left;
	struct merge_data data_right;

	struct merge_data *data = (struct merge_data *)arg;
	
	int *A = data->A;
	int n = data->n;
	int *swap_mem = data->swap_mem;
	int thread_depth = data->thread_depth;

	if(n <= 1)
		if(thread_depth >= 0)
			pthread_exit(NULL);
		else
			return NULL;
	
	mid = n/2;

	data_left.A = A;
	data_left.n = mid;
	data_left.swap_mem = swap_mem;
	data_left.thread_depth = thread_depth-1;

	data_right.A = A + mid;
	data_right.n = n-mid;
	data_right.swap_mem = swap_mem + mid;
	data_right.thread_depth = thread_depth-1;

	if(thread_depth > 0)
	{
		pthread_t thread_1, thread_2;

		pthread_create(&thread_1, NULL, _merge_sort, (void *)&data_left);
		pthread_create(&thread_2, NULL, _merge_sort, (void *)&data_right);
	
		pthread_join(thread_1, NULL);
		pthread_join(thread_2, NULL);
	}
	else
	{
        _merge_sort_2(A, mid, swap_mem); /*Sort the two halves*/
        _merge_sort_2(A + mid, n-mid, swap_mem + mid);
	}
	
	l_offset = 0;
	r_offset = mid;
	
	for(i = 0; l_offset < mid && r_offset < n; i++)
		swap_mem[i] = A[l_offset] < A[r_offset] ? A[l_offset++] : A[r_offset++];

	while(l_offset < mid)
		swap_mem[i++] = A[l_offset++];

	while(r_offset < n)
		swap_mem[i++] = A[r_offset++];
	
	memcpy(A, swap_mem, sizeof(int) * n);
	
	if(thread_depth >= 0)
		pthread_exit(NULL);
	else
		return NULL;
}
void _merge_sort_2(int *A, int n, int *swap_mem)
{
    int r_offset, l_offset;
    int mid;
    int i;

    if(n <= 1)
            return;

    mid = n/2;
    _merge_sort_2(A, mid, swap_mem); /*Sort the two halves*/
    _merge_sort_2(A + mid, n-mid, swap_mem + mid);

    l_offset = 0;
    r_offset = mid;

    for(i = 0; l_offset < mid && r_offset < n; i++) /*Merge the two halves*/
    {
            swap_mem[i] = A[l_offset] < A[r_offset] ? A[l_offset++] : A[r_offset++];
    }
    while(l_offset < mid)
            swap_mem[i++] = A[l_offset++];

    while(r_offset < n)
            swap_mem[i++] = A[r_offset++];

    memcpy(A, swap_mem, sizeof(int) * n);
}