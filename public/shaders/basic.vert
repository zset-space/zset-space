#version 300 es
precision highp float;

// Input is [radius, phase] in polar coordinates
in vec2 pattern;

uniform float density;  // Controls point size and opacity
uniform float energy;   // Controls dimensional stacking

out vec3 vColor;
out float vOpacity;

const float TAU = 6.283185307179586;
const float BASE_SIZE = 2.0 * TAU;     // Base point size
const float MIN_OPACITY = 0.5;   // Minimum opacity

// Helper function to convert polar to cartesian
vec2 polarToCartesian(float radius, float phase) {
    return radius * vec2(cos(phase), sin(phase));
}

void main() {
    float iIndex = float(gl_InstanceID);
    float energyFloor = floor(energy);
    float fraction = energy - energyFloor;

    // Fade control for transitional dimensions
    float alphaFactor = 1.0;
    if (iIndex > energyFloor + 0.5) {
        alphaFactor = 0.0;
    } else if (abs(iIndex - energyFloor) < 0.5) {
        alphaFactor = fraction;
    }

    // Extract base polar coordinates
    float baseRadius = pattern.x;
    float basePhase = pattern.y;

    // Scale radius based on dimension
    float radiusScale = 1.0 - (0.2 * iIndex / max(1.0, energyFloor));
    float finalRadius = baseRadius * radiusScale;

    // Convert to cartesian coordinates
    vec2 finalPos = polarToCartesian(finalRadius, basePhase);
    gl_Position = vec4(finalPos, 0.0, 1.0);

    // Point size now scales with density
    float sizeScale = exp(density);  // Exponential scaling feels more natural
    float baseSize = BASE_SIZE * (1.0 - 0.2 * (iIndex / max(1.0, energyFloor)));
    gl_PointSize = baseSize * sizeScale;

    // Color based on dimensional index
    float hue = 0.2 * (iIndex / max(1.0, energyFloor));
    float sat = 0.8;
    float val = 1.0 - 0.3 * (iIndex / max(1.0, energyFloor));

    // HSV to RGB conversion
    vec4 k = vec4(1.0, 2.0/3.0, 1.0/3.0, 3.0);
    vec3 p = abs(fract(vec3(hue + k.xyz)) * 6.0 - k.www);
    vColor = vec3(val) * mix(k.xxx, clamp(p - k.xxx, 0.0, 1.0), sat);

    // Opacity now combines dimension fade with density control
    float densityOpacity = mix(MIN_OPACITY, 1.0, (density + 1.0) * 0.5);
    vOpacity = alphaFactor * densityOpacity;
}
