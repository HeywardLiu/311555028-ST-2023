# ST-Lab06
- Use `valgrind` and `AddressSanitizer (ASAN)` to detect bugs
## Summary Table
|                      | valgrind | ASAN |
|----------------------|----------|------|
| Heap out-of-bounds   | O        | O    |
| Stack out-of-bounds  | X        | O    |
| Global out-of-bounds | X        | O    |
| Use-after-free       | O        | O    |
| Use-after-return     | X        | O    | 

## Heap out-of-bounds
#### buggy code
```C
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
  int *array =  malloc(sizeof(int)*100);
  array[0] = 0;
  int res = array[argc + 100];  // BOOM
  free(array);
  return res;
}
```
#### Valgrind
- 可以偵測出 heap out-of-bounds
```
❯ valgrind ./heap_out_of_bounds
==409== Memcheck, a memory error detector
==409== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==409== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==409== Command: ./heap_out_of_bounds
==409== 
==409== Invalid read of size 4
==409==    at 0x109198: main (in /home/heyward-wsl/311555028-ST-2023/Lab06/heap_out_of_bounds)
==409==  Address 0x4a4a1d0 is 0 bytes after a block of size 400 alloc'd
==409==    at 0x483B7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==409==    by 0x109185: main (in /home/heyward-wsl/311555028-ST-2023/Lab06/heap_out_of_bounds)
==409== 
==409== 
==409== HEAP SUMMARY:
==409==     in use at exit: 0 bytes in 0 blocks
==409==   total heap usage: 1 allocs, 1 frees, 400 bytes allocated
==409== 
==409== All heap blocks were freed -- no leaks are possible
==409== 
==409== For lists of detected and suppressed errors, rerun with: -s
==409== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

#### ASAN 
- 可以偵測出 heap out-of-bounds
```
bin/heap_out_of_bounds
=================================================================
==2061==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6140000001d0 at pc 0x559dd2ca120f bp 0x7fffcc7c3630 sp 0x7fffcc7c3620
READ of size 4 at 0x6140000001d0 thread T0
    #0 0x559dd2ca120e in main /home/heyward-wsl/311555028-ST-2023/Lab06/heap_out_of_bounds.c:7
    #1 0x7fbcb1fab082 in __libc_start_main ../csu/libc-start.c:308
    #2 0x559dd2ca110d in _start (/home/heyward-wsl/311555028-ST-2023/Lab06/bin/heap_out_of_bounds+0x110d)

0x6140000001d0 is located 0 bytes to the right of 400-byte region [0x614000000040,0x6140000001d0)
allocated by thread T0 here:
    #0 0x7fbcb2286808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x559dd2ca11d7 in main /home/heyward-wsl/311555028-ST-2023/Lab06/heap_out_of_bounds.c:5

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/heyward-wsl/311555028-ST-2023/Lab06/heap_out_of_bounds.c:7 in main
Shadow bytes around the buggy address:
  0x0c287fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff8000: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c287fff8010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff8020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c287fff8030: 00 00 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa
  0x0c287fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8070: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2061==ABORTING
```
## Stack out-of-bounds
#### buggy code
```C
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
  int stack_array[10]= {1};
  return stack_array[10];  // BOOM
}
```
#### Valgrind
- 無法偵測出 stack out-of-bounds
```
valgrind bin/stack_out_of_bounds
==1944== Memcheck, a memory error detector
==1944== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1944== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==1944== Command: bin/stack_out_of_bounds
==1944== 
==1944== 
==1944== HEAP SUMMARY:
==1944==     in use at exit: 0 bytes in 0 blocks
==1944==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==1944== 
==1944== All heap blocks were freed -- no leaks are possible
==1944== 
==1944== For lists of detected and suppressed errors, rerun with: -s
==1944== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
#### ASAN
- 可以偵測出 stack out-of-bounds
```
bin/stack_out_of_bounds
=================================================================
==2098==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffced4cd8a8 at pc 0x557e0f4723b0 bp 0x7ffced4cd840 sp 0x7ffced4cd830
READ of size 4 at 0x7ffced4cd8a8 thread T0
    #0 0x557e0f4723af in main /home/heyward-wsl/311555028-ST-2023/Lab06/stack_out_of_bounds.c:6
    #1 0x7ff77069d082 in __libc_start_main ../csu/libc-start.c:308
    #2 0x557e0f47214d in _start (/home/heyward-wsl/311555028-ST-2023/Lab06/bin/stack_out_of_bounds+0x114d)

Address 0x7ffced4cd8a8 is located in stack of thread T0 at offset 88 in frame
    #0 0x557e0f472218 in main /home/heyward-wsl/311555028-ST-2023/Lab06/stack_out_of_bounds.c:4

  This frame has 1 object(s):
    [48, 88) 'stack_array' (line 5) <== Memory access at offset 88 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /home/heyward-wsl/311555028-ST-2023/Lab06/stack_out_of_bounds.c:6 in main
Shadow bytes around the buggy address:
  0x10001da91ac0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10001da91ad0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10001da91ae0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10001da91af0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10001da91b00: 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1 f1 f1
=>0x10001da91b10: 00 00 00 00 00[f3]f3 f3 f3 f3 00 00 00 00 00 00
  0x10001da91b20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10001da91b30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10001da91b40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10001da91b50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10001da91b60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2098==ABORTING
```
## Global out-of-bounds
#### buggy code
```C
#include <stdlib.h>
#include <stdio.h>

int global_array[10] = {-1};

int main(int argc, char **argv) {
  return global_array[10];  // BOOM
}
```
#### Valgrind
- 無法偵測出 global out-of-bounds
```
❯ valgrind bin/global_out_of_bounds
==2722== Memcheck, a memory error detector
==2722== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==2722== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==2722== Command: bin/global_out_of_bounds
==2722== 
==2722== 
==2722== HEAP SUMMARY:
==2722==     in use at exit: 0 bytes in 0 blocks
==2722==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==2722== 
==2722== All heap blocks were freed -- no leaks are possible
==2722== 
==2722== For lists of detected and suppressed errors, rerun with: -s
==2722== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
#### ASAN
- 可以偵測出 global out-of-bounds
```
bin/global_out_of_bounds
=================================================================
==2127==ERROR: AddressSanitizer: global-buffer-overflow on address 0x562c115c8048 at pc 0x562c115c51fa bp 0x7ffeb16a2f20 sp 0x7ffeb16a2f10
READ of size 4 at 0x562c115c8048 thread T0
    #0 0x562c115c51f9 in main /home/heyward-wsl/311555028-ST-2023/Lab06/global_out_of_bounds.c:7
    #1 0x7f6e6dc42082 in __libc_start_main ../csu/libc-start.c:308
    #2 0x562c115c510d in _start (/home/heyward-wsl/311555028-ST-2023/Lab06/bin/global_out_of_bounds+0x110d)

0x562c115c8048 is located 0 bytes to the right of global variable 'global_array' defined in 'global_out_of_bounds.c:4:5' (0x562c115c8020) of size 40
SUMMARY: AddressSanitizer: global-buffer-overflow /home/heyward-wsl/311555028-ST-2023/Lab06/global_out_of_bounds.c:7 in main
Shadow bytes around the buggy address:
  0x0ac6022b0fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac6022b0fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac6022b0fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac6022b0fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac6022b0ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ac6022b1000: 00 00 00 00 00 00 00 00 00[f9]f9 f9 f9 f9 f9 f9
  0x0ac6022b1010: 00 00 00 00 f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00
  0x0ac6022b1020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac6022b1030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac6022b1040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac6022b1050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2127==ABORTING
```
## Use after free
#### buggy code
```C
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
  int *array = malloc(sizeof(int)*100);
  free(array);
  return array[0];  // BOOM
}
```
#### Valgrind
- 可以偵測出 use-after-free
```
valgrind bin/use_after_free
==2779== Memcheck, a memory error detector
==2779== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==2779== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==2779== Command: bin/use_after_free
==2779== 
==2779== Invalid read of size 4
==2779==    at 0x10919A: main (in /home/heyward-wsl/311555028-ST-2023/Lab06/bin/use_after_free)
==2779==  Address 0x4a4a040 is 0 bytes inside a block of size 400 free'd
==2779==    at 0x483CA3F: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2779==    by 0x109195: main (in /home/heyward-wsl/311555028-ST-2023/Lab06/bin/use_after_free)
==2779==  Block was alloc'd at
==2779==    at 0x483B7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2779==    by 0x109185: main (in /home/heyward-wsl/311555028-ST-2023/Lab06/bin/use_after_free)
==2779== 
==2779== 
==2779== HEAP SUMMARY:
==2779==     in use at exit: 0 bytes in 0 blocks
==2779==   total heap usage: 1 allocs, 1 frees, 400 bytes allocated
==2779== 
==2779== All heap blocks were freed -- no leaks are possible
==2779== 
==2779== For lists of detected and suppressed errors, rerun with: -s
==2779== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```
#### ASAN
- 可以偵測出 use-after-free
```
 bin/use_after_free
=================================================================
==2164==ERROR: AddressSanitizer: heap-use-after-free on address 0x614000000040 at pc 0x55cd84203205 bp 0x7ffd7f1add50 sp 0x7ffd7f1add40
READ of size 4 at 0x614000000040 thread T0
    #0 0x55cd84203204 in main /home/heyward-wsl/311555028-ST-2023/Lab06/use_after_free.c:7
    #1 0x7f614ec5b082 in __libc_start_main ../csu/libc-start.c:308
    #2 0x55cd8420310d in _start (/home/heyward-wsl/311555028-ST-2023/Lab06/bin/use_after_free+0x110d)

0x614000000040 is located 0 bytes inside of 400-byte region [0x614000000040,0x6140000001d0)
freed by thread T0 here:
    #0 0x7f614ef3640f in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:122
    #1 0x55cd842031e2 in main /home/heyward-wsl/311555028-ST-2023/Lab06/use_after_free.c:6

previously allocated by thread T0 here:
    #0 0x7f614ef36808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x55cd842031d7 in main /home/heyward-wsl/311555028-ST-2023/Lab06/use_after_free.c:5

SUMMARY: AddressSanitizer: heap-use-after-free /home/heyward-wsl/311555028-ST-2023/Lab06/use_after_free.c:7 in main
Shadow bytes around the buggy address:
  0x0c287fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c287fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c287fff8000: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd
  0x0c287fff8010: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c287fff8020: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c287fff8030: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c287fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c287fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2164==ABORTING
```
## Use after return
#### buggy code
```C
#include <stdlib.h>
#include <stdio.h>

int* ptr;

void foo() {
    int local[10] = {-1};
    ptr = &local[0];
}

int main(int argc, char* argv[]){
    foo();
    *ptr = 0;
}
```
#### Valgrind
- 無法偵測出 use-after-return
```
❯ valgrind bin/use_after_return
==3399== Memcheck, a memory error detector
==3399== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==3399== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==3399== Command: bin/use_after_return
==3399== 
==3399== 
==3399== HEAP SUMMARY:
==3399==     in use at exit: 0 bytes in 0 blocks
==3399==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==3399== 
==3399== All heap blocks were freed -- no leaks are possible
==3399== 
==3399== For lists of detected and suppressed errors, rerun with: -s
==3399== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
#### ASAN 
- 可以偵測出 use-after-return
- 要export 環境變數 ASAN_OPTIONS=detect_stack_use_after_return=1

```
$ export ASAN_OPTIONS=detect_stack_use_after_return=1
$ bin/use_after_return
=================================================================
==3475==ERROR: AddressSanitizer: stack-use-after-return on address 0x7fee7ef80030 at pc 0x55f38808e3ee bp 0x7fff88c56dd0 sp 0x7fff88c56dc0
WRITE of size 4 at 0x7fee7ef80030 thread T0
    #0 0x55f38808e3ed in main /home/heyward-wsl/311555028-ST-2023/Lab06/use_after_return.c:13
    #1 0x7fee826b0082 in __libc_start_main ../csu/libc-start.c:308
    #2 0x55f38808e12d in _start (/home/heyward-wsl/311555028-ST-2023/Lab06/bin/use_after_return+0x112d)

Address 0x7fee7ef80030 is located in stack of thread T0 at offset 48 in frame
    #0 0x55f38808e1f8 in foo /home/heyward-wsl/311555028-ST-2023/Lab06/use_after_return.c:6

  This frame has 1 object(s):
    [48, 88) 'local' (line 7) <== Memory access at offset 48 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return /home/heyward-wsl/311555028-ST-2023/Lab06/use_after_return.c:13 in main
Shadow bytes around the buggy address:
  0x0ffe4fde7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe4fde7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe4fde7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe4fde7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe4fde7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ffe4fde8000: f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0ffe4fde8010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe4fde8020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe4fde8030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe4fde8040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ffe4fde8050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==3475==ABORTING
```
---
## Stack buffer overflow and Redzone
#### Wrtie a simple program with Asan, and use stack buffer overflow with array a so we can modify array b by crossing redzone.
![](https://i.imgur.com/OtbTGXB.png)

#### Code
```C
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]){
    int a[3] = {0, 0, 0};
    int b[3] = {1, 1, 1};

    printf("Before:\n");
    for(int i=0; i<3; i++) {
        printf("  b[%d] = %d\n", i, b[i]);
    }
    printf("\n&a[8] = %p, &b[0]:%p\n\n", &a[8], &b[0]);
    
    a[8] = 0;  // Modifify array of b by crossing redzone

    printf("After modification:\n");
    for(int i=0; i<3; i++) {
        printf("  b[%d] = %d\n", i, b[i]);
    }
    return 0;
}
```

#### Result
```
❯ bin/redzone
Before:
  b[0] = 1
  b[1] = 1
  b[2] = 1

&a[8] = 0x7f3d2b0d1040, &b[0]:0x7f3d2b0d1040

After modification:
  b[0] = 0
  b[1] = 1
  b[2] = 1
```