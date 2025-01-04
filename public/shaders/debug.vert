#version 300 es
precision highp float;

// Input is [radius, phase] in polar coordinates
in vec2 pattern;

uniform float density;  // Controls point size and opacity
uniform float energy;   // Controls dimensional stacking

out vec3 vColor;
out float vOpacity;

const float TAU = 6.283185307179586;
const float BASE_SIZE = 2.0 * TAU;    // Base point size
const float MIN_OPACITY = 0.5;  // Minimum opacity

void main() {
    // Extract polar coordinates
    float radius = pattern.x;
    float phase = pattern.y;

    // Convert to cartesian coordinates
    vec2 pos = radius * vec2(cos(phase), sin(phase));
    gl_Position = vec4(pos, 0.0, 1.0);

    // Map density [-1,1] to size and opacity adjustments
    float sizeScale = exp(density);  // Exponential scaling for more natural feel
    gl_PointSize = BASE_SIZE * sizeScale;

    // Color based on phase for debugging
    float hue = phase / TAU;
    vec3 rgb = clamp(
        abs(mod(hue * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0,
        0.0, 1.0
    );

    vColor = rgb;
    // Opacity scales with density but never goes fully transparent
    vOpacity = mix(MIN_OPACITY, 1.0, (density + 1.0) * 0.5);
}
