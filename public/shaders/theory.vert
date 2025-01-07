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
const float TAU = 2.0 * PI;

vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0/3.0, 1.0/3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

vec3 rgb(float layer, float dim) {
    float base = floor(dim);
    float frac = dim - base;
    float hue = mod((layer + 1.0) * 105.0, 360.0) / 360.0;

    if (layer < base) {
        return hsv2rgb(vec3(hue, 0.85, 0.5));
    }

    if (layer == base) {
        float sat = 0.15 + 0.85 * frac;
        return hsv2rgb(vec3(hue, sat, 0.5));
    }

    return vec3(0.0);
}

vec3 project(float radius, float phase, float layer) {
    float basis = (TAU * layer) / max(0.1, energy);
    float attract = attractor * cos(phase - basis);
    float wave = amplitude * sin(basis * layer);
    float angle = phase + offset * TAU + basis;
    float r = radius * (1.0 + wave + attract);
    return vec3(cos(angle) * r, sin(angle) * r, phase/TAU);
}

void main() {
    float radius = pattern.x;
    float phase = pattern.y;
    float base = floor(energy);
    float layer = mod(float(gl_VertexID), ceil(energy));
    Color = vec4(rgb(layer, energy), layer < base ? 1.0 : energy - base);
    gl_Position = vec4(project(radius, phase, layer), 1.0);
    gl_PointSize = mix(8.0, 32.0, density);
}
