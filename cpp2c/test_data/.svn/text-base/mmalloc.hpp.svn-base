#ifndef ALIGNED_MMALLOC_HPP
#define ALIGNED_MMALLOC_HPP
/*=============================================================================
  allocator.hpp - Platform independent aligned memory allocation.
  Created on: 06-December-2011
  Author: Ken Herdy

	Description:	

	TODO - 	Wrap routines inside a class scope and/or C++ custom namespace.	

=============================================================================*/

#include "bitblock.hpp"

#if defined USE_NEON
	#error "Neon aligned memory allocation not implemented. Aborting compilation."
#else // USE_SSE

	template <class T> T * simd_malloc(uint32_t n) 
	{
		return (T*)_mm_malloc(n*sizeof(T), sizeof(BitBlock)); 		
	}

	template <class T> void simd_free(T* p) 
	{
		if(p != NULL) 
		{ 
			_mm_free(p); 
			p = NULL;			
		}

	}
#endif

#endif // ALIGNED_MMALLOC_HPP
