
def toLong(a):
    return int(a.cast(gdb.lookup_type('long')))

start_thread_heap = gdb.parse_and_eval("*tcmalloc::ThreadCache::thread_heaps_")
threadcache_t = gdb.lookup_type('tcmalloc::ThreadCache')
freelist_t = gdb.lookup_type('tcmalloc::ThreadCache::FreeList')
sizemap = gdb.parse_and_eval('tcmalloc::Static::sizemap_')

curr_thread_heap = start_thread_heap

kNumClasses  = toLong(gdb.parse_and_eval("kNumClasses"))

while (curr_thread_heap['next_'] != 0):
    print("[+] (tcmalloc::ThreadCache *){}, TID 0x{:x}, Size: {}".format(curr_thread_heap['next_'], toLong(curr_thread_heap['tid_']), curr_thread_heap['size_']))
    
    freelist = curr_thread_heap['list_']
    for i in range(kNumClasses):
        if freelist[i]['length_'] > 0:
            print("[FreeList] Size: {}, {}".format(sizemap['class_to_size_'][i], freelist[i]))


    curr_thread_heap = curr_thread_heap['next_'].cast(threadcache_t.pointer()).dereference()
