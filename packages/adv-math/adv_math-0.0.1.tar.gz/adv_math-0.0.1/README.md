# Introduction: 

Advance Math
This is a library for introducing mathematical concepts that are not in-built on python, like ratios, fractions, factors of numbers, etc.

# Usage

This module currently has one out of the many mathematical operational modes (algebra, arithmetic, geometry, trigonometry, etc.)

So to use any function you need to:

from adv_math *

(mode).(function)

For example:

// Finding HCF of three numbers (5, 40, 75)
  from adv_math import arithmetic
  
  hcf = Factor(5, 40, 75).HCF()
  
  print(hcf)
  
# Other classes in this library
  
  artithmetic: 
  - Ratio (methods: get, simplify, add, subtract, multiply, divide)
  - Fraction (methods: get, getType, simplify, add, subtract, multiply, divide)
  - Factor (methods: HCF, LCM)
  - Just Functions (functions: Factors, PrimeNumbers, CompositeNumbers)
