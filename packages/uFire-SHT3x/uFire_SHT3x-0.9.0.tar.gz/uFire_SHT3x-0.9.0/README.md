SHT30 Temperature and Humidity Sensor
===

Measure temperature and humidity with the Sensiron SHT30 sensor.

#### Summary ℹ️

- Temperature range of -0 to 65 C
- Humidity range of 0 to 100 % RH
- Temperature accuracy ± 0.3% C
- Humidity accuracy ± 3% RH
- I²C interface
- 2.4 - 5.5 V voltage range
 
### Use


```cpp
#include "uFire_SHT30.h"
uFire::SHT30 sht30;

Wire.begin();
sht30.begin();
float tempC = sht30.tempC;
float tempF = sht30.tempF;
float RH = sht30.RH;
float vpd = sht30.vpd_kPa;
float dew_pointC = sht30.dew_pointC;
float dew_pointF = sht30.dew_pointF;
```
* * * 
#### Ask a question 🤙

*   [Discord](https://discord.gg/rAnZPdW)

* * *
### Buy One
* [SHT30](https://ufire.co/buy/)