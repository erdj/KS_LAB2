#include <iostream>
#include <cmath>
#include <cstring>
#include <bitset>

using namespace std;

void printBinary(int n, int i)
{

    
    int k;
    for (k = i - 1; k >= 0; k--) {

        if ((n >> k) & 1)
            cout << "1";
        else
            cout << "0";
    }
}

typedef union {

    float f;
    struct
    {
        unsigned int mantissa : 23;
        unsigned int exponent : 8;
        unsigned int sign : 1;

    } raw;
} myfloat;


void printIEEE(myfloat var)
{

   

    cout << var.raw.sign << " | ";
    printBinary(var.raw.exponent, 8);
    cout << " | ";
    printBinary(var.raw.mantissa, 23);
    cout << "\n";
}



float addFloats(float a, float b) {
   
    myfloat var;
    myfloat x = { a };
    myfloat y = { b };
    var.f = x.f;
    cout << "a: ";
    printIEEE(var);
    var.f = y.f;
    cout << "b: ";
    printIEEE(var);


    
    int signX = (x.raw.sign == 1) ? -1 : 1;
    int signY = (y.raw.sign == 1) ? -1 : 1;

   
    int expX = x.raw.exponent - 127;
    int expY = y.raw.exponent - 127;

   
    float mantX = 1 + x.raw.mantissa / pow(2, 23);
    float mantY = 1 + y.raw.mantissa / pow(2, 23);

   
    int largerExp = expX > expY ? expX : expY;

   
    mantX *= pow(2, expX - largerExp);
    mantY *= pow(2, expY - largerExp);
    myfloat temp;
    cout << "After shifting" << endl;

    
    temp.raw.sign = (signX == 1) ? 0 : 1;

    temp.raw.exponent = largerExp + 127;

    
    temp.raw.mantissa = mantX * pow(2, 23) - 1;
    cout << "a: ";
    printIEEE(temp);

   
    temp.raw.sign = (signY == 1) ? 0 : 1;

   
    temp.raw.exponent = largerExp + 127;

    
    temp.raw.mantissa = mantY * pow(2, 23) - 1;
    cout << "b: ";
    printIEEE(temp);

    
    float result = (signX * mantX) + (signY * mantY);
    cout << "Result before normalizathion" << endl;
    temp.raw.sign = (result < 0) ? 1 : 0;

    
    temp.raw.exponent = largerExp + 127;

    
    temp.raw.mantissa = ((int)(result * pow(2, 23)) & 0x7FFFFF);
    printIEEE(temp);

    
    while (result >= 2) {
        result /= 2;
        largerExp++;
    }
    cout << "Result after normalizathion" << endl;
    temp.raw.sign = (result < 0) ? 1 : 0;

    
    temp.raw.exponent = largerExp + 127;

   
    temp.raw.mantissa = ((int)(result * pow(2, 23)) & 0x7FFFFF);
    printIEEE(temp);

   
    myfloat z = { result };

    
    z.raw.sign = (result < 0) ? 1 : 0;

   
    z.raw.exponent = largerExp + 127;

    z.raw.mantissa = ((int)(result * pow(2, 23)) & 0x7FFFFF);

   
    return z.f;
}



int main() {


    float a, b;
    cout << "Enter first float number: ";
    cin >> a;
    cout << "Enter second float number: ";
    cin >> b;
    float result = addFloats(a, b);
    cout << "Result: " << result << endl;
    return 0;
}