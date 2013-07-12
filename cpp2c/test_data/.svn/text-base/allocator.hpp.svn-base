#ifndef ALLOCATOR_HPP_
#define ALLOCATOR_HPP_
/*=============================================================================
  allocator.hpp - Coterminal memory pool allocators.
  Created on: 18-December-2011
  Author: Ken Herdy
=============================================================================*/

#include "debug.hpp"
#include "bitblock.hpp"
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>

#include <iostream>

///////////////////////////////////////////////////////////////////////////////
// Base Class
///////////////////////////////////////////////////////////////////////////////
class pool_allocator {
public:
	/* n - bytes requested, allocd_segment_size - bytes allocated */
	void * allocate (uint64_t n, uint64_t & allocd_segment_size);
	void * allocate_aligned (uint64_t n, uint64_t & allocd_segment_size);
	void destroy ();
protected:
	pool_allocator(){}
	~pool_allocator(){}
};

///////////////////////////////////////////////////////////////////////////////
// Fast Memory Pool Allocator - Trade memory for speed.
//
// Allocates BASE_SIZE initial bytes on the stack.
// Additional memory allocated on the heap. Coterminal deallocation.
// Allocation returns void * pointer to memory block,
// Returns number of bytes allocated.
//
///////////////////////////////////////////////////////////////////////////////
template<uint32_t BASE_SIZE>
class fast_pool_allocator : public pool_allocator {

public:
	fast_pool_allocator(const uint8_t align=64, const uint8_t exp=2): ALIGNMENT(align), EXPANSION_FACTOR(exp) {
		tail = &head;
		tail->segment = stack_segment;
		tail->next = NULL;
		available = BASE_SIZE;
		segment_size = BASE_SIZE;
	}

	~fast_pool_allocator() {}

	void * allocate(uint64_t n, uint64_t & allocd_segment_size) {

		if(n > available) {
			segment_size = next_segment_size(n);

			node * next = (node *) malloc(sizeof(node));
			if (next == NULL) {
                std::cerr << "Out of Memory" << std::endl;
				abort();
			}

			next->segment = (uint8_t *) malloc(segment_size);
			if ((next->segment) == NULL) {
                std::cerr << "Out of Memory" << std::endl;
				abort();
			}

			next->next = NULL;
			tail->next = next;
			tail = next;

			uint64_t address = reinterpret_cast<uint64_t>(&(tail->segment[0]));
			allocd_segment_size = segment_size;
			available = 0;

			return (void *) (address);
		}

		uint32_t i = segment_size - available;
		uint64_t address = reinterpret_cast<uint64_t>(&(tail->segment[i]));

		allocd_segment_size = n;
		available -= n;

		return (void *) (address);
	}

	void * allocate_aligned(uint64_t n, uint64_t & allocd_segment_size) {

		uint64_t n_padded = (n+ALIGNMENT-1);

		if(n_padded > available) {

			segment_size = next_segment_size(n_padded);

			node * next = (node *) malloc(sizeof(node));
			if (next == NULL) {
                std::cerr << "Out of Memory" << std::endl;
				abort();
			}

			next->segment = (uint8_t *) malloc(segment_size);
			if ((next->segment) == NULL) {
                std::cerr << "Out of Memory" << std::endl;
				abort();
			}

			next->next = NULL;
			tail->next = next;
			tail = next;

			uint64_t address = reinterpret_cast<uint64_t>(&(tail->segment[0]));
			uint64_t padding = ((address % ALIGNMENT) == 0) ? 0 :  ALIGNMENT - (address % ALIGNMENT);
			allocd_segment_size = segment_size - padding;
			available = 0;

			assert(((uint64_t)(address + padding))%ALIGNMENT == 0);
			return (void *) (address + padding);
		}

		uint32_t i = segment_size - available;
		uint64_t address = reinterpret_cast<uint64_t>(&(tail->segment[i]));
		uint64_t padding = ((address % ALIGNMENT) == 0) ? 0 :  ALIGNMENT - (address % ALIGNMENT);
		allocd_segment_size = n - padding;
		available -= (padding + n);

		assert(((uint64_t)(address + padding))%ALIGNMENT == 0);

		return (void *) (address + padding);
	}

	void destroy() {
		node * crt = head.next;
		node * next;
		while(crt != NULL) {
			next = crt->next;
			free((uint8_t *) crt->segment);
			free((node *)crt);
			crt = next;
			next = NULL;
		}
	}

	uint64_t get_alloc_size() const { return alloc_size; }

private:
	uint64_t alloc_size;

	const uint8_t ALIGNMENT;
	const uint8_t EXPANSION_FACTOR;
	uint64_t available;
	uint64_t segment_size;

	typedef struct node {
		node * next;
		uint8_t * segment;
	} node;

	uint8_t stack_segment[BASE_SIZE];
	node head;
	node * tail;

	uint64_t next_segment_size(uint64_t n) const {
		return (((n/segment_size) * segment_size) + segment_size) * EXPANSION_FACTOR ; // a multiple of segment_size
	}

};

#endif // ALLOCATOR_HPP_
