#ifndef DEBUG_H_
#define DEBUG_H_

/*=============================================================================
  debug.hpp - Debug macros.
  Created on:
  Author: Ken Herdy
=============================================================================*/

#include <iostream>

// #define NDEBUG // if NDEBUG then disable assertions

#ifdef NDEBUG
#define MSG(str)
#define VAR(name, value)
#else
#define MSG(str) std::cout << str << std::endl;
#define VAR(name, value) std::cout << name << ":" << value << std::endl;
#endif

#endif // DEBUG_H_
