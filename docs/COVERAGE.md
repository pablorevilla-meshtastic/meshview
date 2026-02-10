# Coverage Prediction

Meshview can display a predicted coverage boundary for a node. This is a **model**
estimate, not a guarantee of real-world performance.

## How it works

The coverage boundary is computed using the Longley-Rice / ITM **area mode**
propagation model. Area mode estimates average path loss over generic terrain
and does not use a terrain profile. This means it captures general distance
effects, but **does not** account for terrain shadows, buildings, or foliage.

## What you are seeing

The UI draws a **perimeter** (not a heatmap) that represents the furthest
distance where predicted signal strength is above a threshold (default
`-120 dBm`). The model is run radially from the node in multiple directions,
and the last point above the threshold forms the outline.

## Key parameters

- **Frequency**: default `907 MHz`
- **Transmit power**: default `20 dBm`
- **Antenna heights**: default `5 m` (TX) and `1.5 m` (RX)
- **Reliability**: default `0.5` (median)
- **Terrain irregularity**: default `90 m` (average terrain)

## Limitations

- No terrain or building data is used (area mode only).
- Results are sensitive to power, height, and threshold.
- Environmental factors can cause large real-world deviations.

