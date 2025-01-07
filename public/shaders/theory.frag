#version 300 es
precision highp float;

in vec4 Color;
out vec4 fColor;

void main() {
    // Create circular points with soft edges
    vec2 coord = 2.0 * gl_PointCoord - 1.0;
    float r = dot(coord, coord);

    // Discard fragments outside unit circle
    if (r > 1.0) {
        discard;
    }

    // Enhanced edge softening with quadratic falloff
    float fade = 1.0 - smoothstep(0.7, 1.0, r);

    // Combine color and opacity with fade
    fColor = vec4(Color.rgb, fade * Color.a);
}
