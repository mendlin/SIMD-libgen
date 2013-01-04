#ifndef PERFSEC_H
#define PERFSEC_H

#if defined(WALL_TIMING)
#include "WallTime.h"
#elif defined(BUFFER_PROFILING)
#include "BOM_Profiler.h"
#elif defined(CODE_CLOCKER)
	#include "../cclib/cc.h"
	#include "../cclib/cc.cxx"	
#endif

#if defined __GNUC__

  #include <sched.h>

  int set_processor_affinity(unsigned long mask) { // mask = 1 sets hard processor affinity for core 1, mask = 2 for core 2, mask = 4 for core 3, mask = 7 for core 1 and core 2 and core 3.

    unsigned int len = sizeof(mask);

    if (sched_setaffinity(0, len, (const cpu_set_t *)&mask) < 0) {
      printf("sched_setaffinity call failed.\n");
      return -1;
    }

    printf("CPU affinity mask: %08lx\n", mask);

    return 0;
  }

#elif defined _MSC_VER

  #include <process.h>
  #include <Windows.h>
  #define getpid _getpid

  int set_processor_affinity(DWORD_PTR mask) {

    HANDLE hProcess  = OpenProcess(PROCESS_ALL_ACCESS, 0, getpid());

	if(0 == SetProcessAffinityMask(hProcess, mask)) {
	      printf("SetProcessAffinityMask call failed.\n");
	      return -1;
	}

	printf("CPU affinity mask: %08lx\n", mask);

	return 0;
  }

#else

  int set_processor_affinity(unsigned long mask) {
	printf("set_processor_affinity is not implemented on the current OS.\n");
	return -1;
  }

#endif

#define PERF_SEC_BIND(mask) \
	set_processor_affinity(mask)

#if defined(WALL_TIMING)

	#define PERF_SEC_INIT(timer) \
		timer = init_Wall_timer()
	
	#define PERF_SEC_START(timer) \
		start_Wall_interval(timer) 
	
	#define PERF_SEC_END(timer,elems) \
		end_Wall_interval(timer,elems) 
	
	#define PERF_SEC_DUMP(timer) \
		dump_Timer_Table(timer)
	
	#define PERF_SEC_DESTROY(timer) \
		destroy_Wall_timer(timer)	
	
#elif defined(BUFFER_PROFILING)

	#define PERF_SEC_INIT(timer) \
		timer = init_BOM_timer()
	
	#define PERF_SEC_START(timer) \
		start_BOM_interval(timer) 
	
	#define PERF_SEC_END(timer,elems) \
		end_BOM_interval(timer,elems) 
	
	#define PERF_SEC_DUMP(timer) \
		dump_BOM_table(timer)
	
	#define PERF_SEC_DESTROY(timer) \
		destroy_BOM_timer(timer)	
	
#elif defined(CODE_CLOCKER)

	#define PERF_SEC_INIT(timer)
		
	#define PERF_SEC_START(timer) \
		timer->start_interval()

	#define PERF_SEC_END(timer,elems) \
		timer->end_interval(elems)
	
	#define PERF_SEC_DUMP(timer) \
		timer->dump_avg_kelem() \
		
	#define PERF_SEC_DESTROY(timer) \
		if(timer) delete timer
		
#else

	#define PERF_SEC_INIT(timer)
	#define PERF_SEC_START(timer)
	#define PERF_SEC_END(timer,elems)
	#define PERF_SEC_DUMP(timer)
	#define PERF_SEC_DESTROY(timer)

#endif
#endif

