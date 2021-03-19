
#include "points.h"
#include "self_math.h"
#include "iRRAM.h"
#include "gamma.h"
#include <string>
#include <cfenv>

#undef euler_gamma
#define euler_gamma REAL("0.57721566490153286060651209008240243104215933593992")
#define pi REAL(3.1415926535897932384626433832795)

using namespace iRRAM;


void compute(){
	std::fesetround(FE_DOWNWARD);
	iRRAM::cout << setRwidth(45);

	REAL x;
	REAL r;

	std::string x_str;
	iRRAM::cin >> x_str;

	x = binary2double(x_str);

	if(true){
		r = (x-iRRAM::sin((REAL)x))/(x-iRRAM::tan((REAL)x));
	}

	iRRAM::cout << double2binary(r.as_double()) << "\n";
}

