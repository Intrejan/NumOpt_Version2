
#include "points.h"
#include "self_math.h"
#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
#include <string>
#include <cfenv>

#define euler_gamma 0.577215664901532860606512090082402431042159335
#define pi 3.1415926535897932384626433832795

using namespace std;

int main(){
	std::fesetround(FE_DOWNWARD);
	std::cout << scientific << setprecision(numeric_limits<double>::digits10);

	double x;
	double r;

	std::string x_str;
	std::cin >> x_str;

	x = binary2double(x_str);

	if(true){
		r = (x-sin(x))/(x-tan(x));
	}

	std::cout << double2binary(r) << "\n";
}

