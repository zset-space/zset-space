#version 300 es
precision highp float;

in vec2 pattern;
uniform float energy;
uniform float density;

out vec3 vColor;
out float vOpacity;

const float PI = 3.141592653589793;
const float TAU = 6.283185307179586;

// Phase function capturing geometric necessity
float fn(float d) {
    return PI / (d * (d + 1.0));
}

// N-ball surface area ratio
float getSurfaceRatio(float d) {
    return TAU / d;  // S(d+1) / S(d)
}

void main() {
    float layerIndex = float(gl_InstanceID);

    // Geometric state visualization
    float radius = pattern.x;
    float phase = pattern.y;

    // Phase accumulation
    float accPhase = phase + fn(energy) * layerIndex;

    // Position with dimension-based scaling
    float r = radius * (1.0 - 0.2 * layerIndex / max(1.0, energy));
    vec2 pos = r * vec2(cos(accPhase), sin(accPhase));

    gl_Position = vec4(pos, 0.0, 1.0);

    // Point size from density
    float sizeScale = exp(density);
    gl_PointSize = mix(2.0, 4.0, sizeScale);

    // Debug coloring: phase visualization
    float phaseColor = accPhase / TAU;
    vColor = vec3(
        0.5 + 0.5 * cos(TAU * phaseColor),
        0.5 + 0.5 * cos(TAU * (phaseColor + 1.0/3.0)),
        0.5 + 0.5 * cos(TAU * (phaseColor + 2.0/3.0))
    );

    // Opacity shows dimensional boundary
    float dimBoundary = step(layerIndex, energy);
    vOpacity = dimBoundary * mix(0.3, 0.8, sizeScale);
}
