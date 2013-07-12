#ifndef STL_ALIGNED_ALLOCATOR_HPP_
#define STL_ALIGNED_ALLOCATOR_HPP_

/*=============================================================================
  stl_aligned_allocator.hpp 
  Created on: 06-November-2012
  Author: Ken Herdy
=============================================================================*/

#include <cstddef>
#include "bitblock.hpp"
#include "mmalloc.hpp"

template <typename T, size_t N=sizeof(BitBlock)>
class AAllocator
{
public:

	typedef	T	value_type;
	typedef	size_t size_type;
	typedef	ptrdiff_t difference_type;
	typedef	T* pointer;
	typedef const T* const_pointer;
	typedef	T& reference;
	typedef const T& const_reference;

	inline AAllocator() throw(){}

	template <typename T2> inline  AAllocator(const AAllocator<T2, N> &) throw(){}
	inline ~AAllocator() throw(){}	

	inline pointer adress(reference r)
	{ 
		return &r; 
	}

	inline const_pointer adress(const_reference r) const
	{ 
		return &r; 
	}

	inline pointer allocate(size_type n)
	{ 
		return simd_malloc<T>(n*sizeof(value_type));

		//return (pointer)_mm_malloc(n*sizeof(value_type), N); 
	}

	inline void deallocate(pointer p, size_type)
	{ 
		return simd_free<T>(p); 
		//_mm_free(p); 
	}

	inline void construct(pointer p, const value_type & wert)	
	{ 
		new(p) value_type(wert); 
	}

	inline void destroy(pointer p)
	{ 
		p; 
		p->~value_type(); // C4100 warning
	}

	inline size_type max_size() const throw()
	{ 
		return (size_type(-1) / sizeof(value_type)); 
	}

	template <typename T2> struct rebind 
	{ 
		typedef AAllocator<T2, N> other; 
	};

};

#endif // STL_ALIGNED_ALLOCATOR_HPP_ 
