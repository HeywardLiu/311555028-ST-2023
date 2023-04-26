valgrind:
	gcc -o bin/heap_out_of_bounds heap_out_of_bounds.c
	gcc -o bin/stack_out_of_bounds stack_out_of_bounds.c
	gcc -o bin/global_out_of_bounds global_out_of_bounds.c
	gcc -o bin/use_after_free use_after_free.c
	gcc -o bin/use_after_return use_after_return.c

asan:
	gcc -fsanitize=address -O1 -g -o bin/heap_out_of_bounds heap_out_of_bounds.c
	gcc -fsanitize=address -O1 -g -o bin/stack_out_of_bounds stack_out_of_bounds.c
	gcc -fsanitize=address -O1 -g -o bin/global_out_of_bounds global_out_of_bounds.c
	gcc -fsanitize=address -O1 -g -o bin/use_after_free use_after_free.c
	gcc -fsanitize=address -O1 -g -o bin/use_after_return use_after_return.c

redzone:
	gcc -fsanitize=address -O1 -g -o bin/redzone redzone.c
	
clean:
	rm -f bin/*
