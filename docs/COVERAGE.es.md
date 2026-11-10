# Cobertura

## Cobertura predicha

Meshview puede mostrar un límite de cobertura predicha para un nodo. Es una estimación
de un **modelo**, no una garantía de cómo se comportará en el mundo real.

### Cómo funciona

El límite de cobertura se calcula con el modelo de propagación Longley-Rice / ITM en
**modo área**. El modo área estima la pérdida de trayecto media sobre un terreno
genérico y no usa un perfil del terreno. Esto significa que recoge los efectos
generales de la distancia, pero **no** tiene en cuenta las sombras del relieve, los
edificios ni la vegetación.

### Qué estás viendo

La interfaz dibuja un **perímetro** (no un mapa de calor) que representa la distancia
máxima en la que la señal predicha supera un umbral (por defecto `-120 dBm`). El modelo
se calcula en varias direcciones alrededor del nodo, y el último punto por encima del
umbral en cada una forma el contorno.

### Parámetros principales

- **Frecuencia**: por defecto `907 MHz`
- **Potencia de transmisión**: por defecto `20 dBm`
- **Altura de las antenas**: por defecto `5 m` (TX) y `1.5 m` (RX)
- **Fiabilidad**: por defecto `0.5` (mediana)
- **Irregularidad del terreno**: por defecto `90 m` (terreno medio)

### Requisitos

El modelo necesita el paquete opcional `pyitm`. Está incluido en `requirements.txt`, y
las instalaciones desde el paquete pueden añadirlo con el extra `coverage`
(`pip install 'meshview[coverage]'`). Sin él, el botón de cobertura indica que la
cobertura predicha no está disponible en el servidor.

### Limitaciones

- No se usan datos de terreno ni de edificios (solo modo área).
- Los resultados dependen mucho de la potencia, la altura y el umbral.
- Los factores del entorno pueden provocar grandes desviaciones en la realidad.
