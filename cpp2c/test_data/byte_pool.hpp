#ifndef BYTE_POOL_HPP
#define BYTE_POOL_HPP

/*=============================================================================
  byte_pool.hpp - Byte pool. Templated on our custom allocator, see allocator.hpp.
  Created on: 18-December-2011
  Author: Ken Herdy
=============================================================================*/

#include "allocator.hpp"
#include <string.h>

template<class ALLOCATOR>
class byte_pool
{
public:
    byte_pool(const uint64_t base_size=1024) {
	alloc_segment_size = 0;
	offset = 0;
	pool = static_cast<uint8_t *>(allocator.allocate(base_size, alloc_segment_size));
    }

    ~byte_pool() {
	allocator.destroy();
    }

    uint8_t * insert(uint8_t * bytes, uint32_t lgth) {

	if(lgth > alloc_segment_size) {
	    pool = static_cast<uint8_t *>(allocator.allocate(lgth, alloc_segment_size));
	    offset = 0;
	}

	uint8_t * next = &(pool[offset]);
	memcpy(next, bytes, lgth);
	alloc_segment_size -= lgth;
	offset += lgth;

	return next;
    }

    uint8_t * insert(uint8_t * bytes, uint32_t lgth, uint32_t advance) {
	uint32_t total_lgth = lgth + advance;
	return insert(bytes, total_lgth);
    }

private:
    ALLOCATOR allocator;
    uint64_t alloc_segment_size;
    uint32_t offset;
    uint8_t * pool;
};

#endif // BYTE_POOL_HPP
