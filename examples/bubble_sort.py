from tapepy.core import tape
from tapepy.core import replay
from tapepy.stats import tape_stats
from tapepy.export import export_to_html
from tapepy.export import export_to_csv
from tapepy.stats import trace_history

@tape()
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
bubble_sort([5, 3, 1, 4])


replay()
