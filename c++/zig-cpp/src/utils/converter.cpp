#include "converter.hpp"

double CelsiusToFahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}

double FahrenheitToCelsius(double fahrenheit) {
    return (fahrenheit - 32.0) * 5.0 / 9.0;
}

double CelsiusToKelvin(double celsius) {
    return celsius + 273.15;
}

double KelvinToCelsius(double kelvin) {
    return kelvin - 273.15;
}