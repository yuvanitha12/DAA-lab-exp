import time, random, math

def interpolation_search(arr, target):
    low, high = 0, len(arr)-1
    comparisons = 0
    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            return (low, comparisons) if arr[low]==target else (-1, comparisons)
        if arr[high] == arr[low]:
            break
        pos = low + int(((target-arr[low])*(high-low))/(arr[high]-arr[low]))
        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1, comparisons

def binary_search(arr, target):
    low, high = 0, len(arr)-1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low+high)//2
        if arr[mid]==target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons

def performance_analysis():
    sizes=[1000,5000,10000,50000,100000]
    is_times=[]; bs_times=[]; is_comp=[]; bs_comp=[]
    print(f"{'Size':>10} {'IS Time(ms)':>14} {'BS Time(ms)':>14} {'IS Comp':>10} {'BS Comp':>10}")
    print("-"*70)
    for size in sizes:
        arr=sorted(random.sample(range(size*10), size))
        target=arr[random.randint(0,size-1)]
        st=time.perf_counter()
        for _ in range(100):
            _,c1=interpolation_search(arr,target)
        t1=(time.perf_counter()-st)/100*1000
        st=time.perf_counter()
        for _ in range(100):
            _,c2=binary_search(arr,target)
        t2=(time.perf_counter()-st)/100*1000
        print(f"{size:>10} {t1:>14.4f} {t2:>14.4f} {c1:>10} {c2:>10}")
        is_times.append(t1); bs_times.append(t2)
        is_comp.append(c1); bs_comp.append(c2)


if __name__=="__main__":
    arr=[2,5,10,12,23,38,50,60,75,99,111,120]
    target=23
    idx,comp=interpolation_search(arr,target)
    print("Array:",arr)
    print("Searching for:",target)
    print("Found at index:",idx)
    print("Comparisons:",comp)
    print()
    performance_analysis()