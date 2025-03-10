#version 300 es
precision highp float;

in vec3 vColor;
in float vOpacity;

out vec4 fragColor;

void main() {
    // Create circular points with soft edges
    vec2 coord = 2.0 * gl_PointCoord - 1.0;
    float r = dot(coord, coord);

    if (r > 1.0) {
        discard;
    }

    // Soft edge for points
    float fade = 1.0 - smoothstep(0.8, 1.0, r);
    fragColor = vec4(vColor, vOpacity * fade);
}