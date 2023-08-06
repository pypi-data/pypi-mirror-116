# Pymetro
Pymetro is a python library that allows you to incorporate scientific notations using symbols into your program. It provides functions that force a specific notation on a variable as specified by the user and includes a function that automatically formats any given numbers to a standard index form.
**Note that all of the returns given by any functions in this module are Strings.**
# Usage
## Manual
To use Pymetro, it is first imported to the Python workspace like any other library as:

    >> import pymetro
You can then call one of the many functions provided in order to format the desired number. For manual formatting functions, the function is called from the library and provided with either an integer or a float. The following is an example of raising the number 2314.124 to a notation of kilo:

    >> pymetro.kilo(2314.124)
    2.314124k
You can also specify the number of digits after the decimal point by providing another integer to the function representing the number of places required after the decimal point:

    >> pymetro.kilo(2314.124, 3)
    2.314k
 
If no integer is provided to specify the rounding place, the function would simply default to not rounding the number at all.

## Auto
The auto function on the other hand automatically formats the number based on the standard index form, to illustrate, these are the results of passing two different numbers into the auto function:

    >> pymetro.auto(2145.235)
    2.145235k
    >> pymetro.auto(0.032523)
    32.523m
As you can see, both numbers were automatically formatted to the recommended notation. This is helpful when the user cannot predict what numbers are going to be generated or inputted in their program.
Similarly, the auto function is also capable of accepting a specific number of integers following the decimal point to round, the result is as follows:

    >> pymetro.auto(2145.235, 3)
    2.145k
    >> pymetro.auto(0.032523, 2)
    32.52m

 
# Functions
|**Notation**|**Symbol**|**Function**|
|--|--|--|
|*Atto*|*a*|atto()|
|*Femto*|*f*|femto()|
|*Pico*|*p*|pico()|
|*Nano*|*n*|nano()|
|*Micro*|*µ*|micro()|
|*Milli*|*m*|milli()|
|*Kilo*|*k*|kilo()|
|*Mega*|*M*|Mega()|
|*Giga*|*G*|giga()|
|*Tera*|*T*|tera()|
|*Peta*|*peta*|peta()|
|*Exa*|*E*|exa()|
|*Zetta*|*Z*|zetta()|
|*Yotta*|*Y*|yotta()|

