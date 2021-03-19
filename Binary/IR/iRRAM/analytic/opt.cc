
#include <iostream>
#include <iomanip>
#include <limits>
#include <cmath>
#include <cfenv>

#include "iRRAM.h"
#include "../../../src/points.h"
#include "../../../src/self_math.h"
#include "../../../src/gamma.h"

using namespace std;
using namespace iRRAM;


double evaluate(double x)
{
	double powx;
	REAL powx_real;
	int degree;
	int degree_real;
	double res;
	REAL res_real;
	REAL x_real(x);

	if(true&&(-1.5026064617676354e+304<=x)&&(x<=1.2204343072343305e+307)) {
		powx = 1;
		res = 0;
		{
			int i;
			i = 0;
			while(true) {
				if(!(i<degree)) {
					break;
				}
				if(i<degree) {
					i = 1+i;
					res = res+(powx*x);
					powx = (powx*x);
				}
			}
		}
		return res;
	}

	if(true) {
		powx_real = 1;
		res_real = 0;
		{
			int i;
			i = 0;
			while(true) {
				if(!(i<degree_real)) {
					break;
				}
				if(i<degree_real) {
					i = 1+i;
					res_real = res_real+(powx_real*x_real);
					powx_real = (powx_real*x_real);
				}
			}
		}
		return res_real.as_double();
	}

	return res;
}

void compute() {
	std::fesetround(FE_DOWNWARD);
	std::string x_str;
	iRRAM::cin >> x_str;
	double x_double = binary2double(x_str);
	double r_double = evaluate(x_double);
	iRRAM::cout << double2binary(r_double) << "\n";
}

