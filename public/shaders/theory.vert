#version 300 es
precision highp float;

in vec2 pattern;
uniform float energy;
uniform float offset;
uniform float amplitude;
uniform float attractor;
uniform float density;

out vec4 Color;

const float PI = 3.141592653589793;
const float E = 2.718281828459045;
const float TAU = 2.0 * PI;

// Wave interference pattern for dimensional presence
float computeWaveInterference(float phase, float layer, float baseEnergy) {
    float energyScale = max(PI/E, baseEnergy);

    // Forward and backward wave components
    float forwardWave = sin(layer * phase/PI + offset * TAU);
    float backwardWave = sin(layer * (TAU - phase)/PI - offset * TAU);

    // Wave interference creates natural standing wave patterns
    float interference = (forwardWave + backwardWave) * 0.5;

    // Phase coherence through dimensional coupling
    float coherence = cos(layer * TAU/energyScale);

    return interference * coherence * exp(-abs(layer - baseEnergy)/PI);
}

// Complex phase rotation for dimensional binding
vec2 complexRotate(float angle) {
    return vec2(cos(angle), sin(angle));
}

vec3 projectDimension(float radius, float phase, float layer) {
    float energyScale = max(PI/E, energy);
    float dimFreq = TAU * layer / energyScale;

    // Wave interference determines dimensional presence
    float interference = computeWaveInterference(phase, layer, energy);

    // Phase evolution through complex rotation
    vec2 rotation = complexRotate(phase + offset * TAU + dimFreq);

    // Natural binding through phase coherence
    float binding = attractor * cos(phase - dimFreq);

    // Standing wave pattern for amplitude modulation
    float wave = amplitude * sin(dimFreq * (layer + 1.0));

    // Enhanced radius computation preserving ring structure
    float r = radius * (1.0 + wave + binding);

    // Depth calculation using interference pattern
    float baseDepth = (layer + PI) / (energyScale + PI);
    float waveDepth = interference * sin(phase * layer/energyScale);

    // Combine depths with natural weighting
    float depth = mix(baseDepth, baseDepth + waveDepth/E,
                     exp(-abs(layer - energy)));

    return vec3(
        r * rotation.x,
        r * rotation.y,
        clamp(depth, -1.0, 1.0)
    );
}

vec3 generateColor(float layer, float dim) {
    // Phase-harmonic color progression
    float hue = fract((layer + 1.0) * PI/E) * TAU;
    float sat = exp(-abs(layer - dim)/PI);

    // Natural color harmonics through wave interference
    vec3 color = vec3(
        0.5 + 0.5 * cos(hue),
        0.5 + 0.5 * cos(hue + TAU/3.0),
        0.5 + 0.5 * cos(hue + 2.0*TAU/3.0)
    );

    // Color presence through dimensional emergence
    float emergence = 1.0 - exp(-PI * (dim - floor(dim)));
    float presence = layer < floor(dim) ? 1.0 : emergence;

    return mix(vec3(0.1), color * sat, presence);
}

void main() {
    float radius = pattern.x;
    float phase = pattern.y;
    float layer = float(gl_InstanceID);

    // Project with wave interference patterns
    vec3 position = projectDimension(radius, phase, layer);
    gl_Position = vec4(position, 1.0);

    // Color with enhanced wave harmonics
    vec3 color = generateColor(layer, energy);
    float alpha = layer < floor(energy) ?
                 1.0 :
                 energy - floor(energy);

    Color = vec4(color, alpha);

    // Dynamic point size with interference scaling
    float sizeScale = exp(-abs(position.z)) * mix(1.0, 2.0, density);
    gl_PointSize = mix(8.0, 32.0, sizeScale);
}