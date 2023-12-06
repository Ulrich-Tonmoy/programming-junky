#include <iostream>
#include "./utils/converter.hpp"

int main() {
    // std::cout << "Hello World!";

    int choice;
    double temperature, convertedTemperature;

    std::cout << "Temperature Converter" << std::endl;
    std::cout << "1. Celsius to Fahrenheit" << std::endl;
    std::cout << "2. Fahrenheit to Celsius" << std::endl;
    std::cout << "3. Celsius to Kelvin" << std::endl;
    std::cout << "4. Kelvin to Celsius" << std::endl;
    std::cout << "Enter your choice (1-4): ";
    std::cin >> choice;

    std::cout << "Enter the temperature: ";
    std::cin >> temperature;

    switch (choice) {
        case 1:
            convertedTemperature = CelsiusToFahrenheit(temperature);
            break;
        case 2:
            convertedTemperature = FahrenheitToCelsius(temperature);
            break;
        case 3:
            convertedTemperature = CelsiusToKelvin(temperature);
            break;
        case 4:
            convertedTemperature = KelvinToCelsius(temperature);
            break;
        default:
            std::cout << "Invalid choice." << std::endl;
            return 1;
    }

    std::cout << "Converted Temperature: " << convertedTemperature << std::endl;

    return 0;
}