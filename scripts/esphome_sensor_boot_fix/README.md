# ESPHome Sensor Boot Fix

Prevents ESPHome sensors from publishing invalid/garbage values during device startup before the hardware has stabilized.

## Problem

On boot, sensors like DHT22/BME280 often report `0`, `NaN`, or out-of-range values for the first few seconds while the sensor initializes.

## Solution

Uses a global `boot_complete` flag set after a delay in `on_boot`. Sensor filters suppress values until the flag is true.

## Usage

Merge the relevant sections into your existing ESPHome config:

```yaml
# Copy globals, on_boot, and sensor filter sections into your device config
```

## Customization

- Adjust `delay: 5s` to match your sensor's warmup time
- Works with any sensor platform that supports `filters`
- The `lambda` filter returning `{}` means "skip this value"
