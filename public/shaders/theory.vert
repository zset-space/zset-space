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

// Phase resonance that creates natural regions of influence
float computePhaseResonance(float phase, float layer, float baseEnergy) {
    // Normalize to prevent dimensional collapse
    float energyScale = max(PI/E, baseEnergy);

    // Each dimension resonates at its natural frequency
    float dimensionalFreq = TAU * layer / energyScale;

    // Phase coupling through natural harmonics
    float phaseHarmonic = phase + dimensionalFreq;

    // Natural resonance peaked at dimension's "home" phase
    return cos(phaseHarmonic) * exp(-abs(layer - baseEnergy)/PI);
}

vec3 projectDimension(float radius, float phase, float layer) {
    float energyScale = max(PI/E, energy);
    float baseFreq = TAU * layer / energyScale;

    // Compute dimensional resonance
    float resonance = computePhaseResonance(phase, layer, energy);

    // Phase modulation incorporating resonance
    float modPhase = phase + offset * TAU + baseFreq;

    // Natural binding through phase coherence
    float binding = attractor * cos(modPhase - baseFreq);

    // Wave component scaled by dimensional presence
    float wave = amplitude * sin(baseFreq * (layer + 1.0));

    // Radius modulation preserving ring continuity
    float r = radius * (1.0 + wave + binding);

    // Enhanced depth calculation using resonance
    float naturalDepth = (layer + PI) / (energyScale + PI);
    float phaseDepth = resonance * sin(modPhase);

    // Final depth combines natural layer order with phase influence
    float depth = mix(naturalDepth, naturalDepth + phaseDepth/E,
                     exp(-abs(layer - energy)));

    return vec3(
        r * cos(modPhase),
        r * sin(modPhase),
        clamp(depth, -1.0, 1.0)
    );
}

vec3 computeDimensionalColor(float layer, float dim) {
    // Phase-harmonic hue progression
    float hue = fract((layer + 1.0) * PI/E) * TAU;

    // Natural color harmonics
    vec3 color = vec3(
        0.5 + 0.5 * cos(hue),
        0.5 + 0.5 * cos(hue + TAU/3.0),
        0.5 + 0.5 * cos(hue + 2.0*TAU/3.0)
    );

    // Dimensional presence through natural emergence
    float emergence = 1.0 - exp(-PI * (dim - floor(dim)));
    float presence = layer < floor(dim) ? 1.0 : emergence;

    return mix(vec3(0.1), color, presence);
}

void main() {
    float radius = pattern.x;
    float phase = pattern.y;
    float layer = float(gl_InstanceID);

    // Project dimension with enhanced phase resonance
    vec3 position = projectDimension(radius, phase, layer);
    gl_Position = vec4(position, 1.0);

    // Color computation with dimensional presence
    vec3 color = computeDimensionalColor(layer, energy);
    float alpha = layer < floor(energy) ?
                 1.0 :
                 energy - floor(energy);

    Color = vec4(color, alpha);

    // Dynamic point size with resonance-based scaling
    float sizeScale = exp(-abs(position.z)) * mix(1.0, 2.0, density);
    gl_PointSize = mix(8.0, 32.0, sizeScale);
}