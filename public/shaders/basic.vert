#version 300 es
precision highp float;

in vec2 pattern;
uniform float energy;
uniform float density;

out vec3 vColor;
out float vOpacity;

const float PI = 3.141592653589793;
const float TAU = 6.283185307179586;
const float SQRT_PI = 1.772453850905516;

float gamma(float x) {
    float sum = 0.0;
    float term = 1.0;
    for (float n = 1.0; n < 5.0; n += 1.0) {
        term *= (x + n - 1.0);
    }
    return term;
}

float nBallVolume(float d) {
    float halfD = d * 0.5;
    return pow(PI, halfD) / gamma(halfD + 1.0);
}

float nBallSurface(float d) {
    return TAU * nBallVolume(d - 1.0);
}

vec2 computeWave(float phase, float dim, float e) {
    float forwardPhase = phase + PI / (dim * (dim + 1.0)) * e;
    float backPhase = -forwardPhase;

    float amplitude = exp(-pow(dim - e, 2.0) / (4.0 * PI));

    vec2 forward = amplitude * vec2(cos(forwardPhase), sin(forwardPhase));
    vec2 backward = amplitude * vec2(cos(backPhase), sin(backPhase));

    return mix(forward, backward, 0.5);
}

void main() {
    float dimIndex = float(gl_InstanceID);
    float energyFloor = floor(energy);

    float dimPresence = 1.0;
    if (dimIndex > energyFloor) {
        dimPresence = 0.0;
    } else if (dimIndex == energyFloor) {
        float fract_e = fract(energy);
        dimPresence = fract_e * (1.0 + 0.2 * sin(fract_e * PI));
    }

    float radius = pattern.x;
    float basePhase = pattern.y;

    // Create spiral through phase evolution
    vec2 wave = computeWave(basePhase, dimIndex + 1.0, energy);

    float volRatio = nBallVolume(dimIndex + 2.0) / max(1e-6, nBallVolume(dimIndex + 1.0));
    float radiusScale = mix(1.0, volRatio, 0.3) * (1.0 - 0.2 * dimIndex/energy);

    // Compute final radial position
    float finalPhase = basePhase + TAU * dimIndex/energy;
    vec2 position = (radius * radiusScale) * vec2(
        cos(finalPhase),
        sin(finalPhase)
    ) + wave * 0.2;

    float waveCoherence = length(wave);
    float sizeScale = exp(density);
    gl_PointSize = mix(2.0, 8.0, sizeScale * waveCoherence);

    float hue = fract((dimIndex + 1.0) * SQRT_PI);
    float sat = mix(0.7, 0.9, waveCoherence);
    float val = mix(0.8, 1.0, waveCoherence);

    vec4 K = vec4(1.0, 2.0/3.0, 1.0/3.0, 3.0);
    vec3 p = abs(fract(vec3(hue) + K.xyz) * 6.0 - K.www);
    vColor = val * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), sat);

    vOpacity = dimPresence * mix(0.3, 0.8, waveCoherence * sizeScale);

    gl_Position = vec4(position, 0.0, 1.0);
}
