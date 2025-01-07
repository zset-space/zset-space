#version 300 es
precision highp float;

in vec3 vColor;
in float vOpacity;

out vec4 fragColor;

void main() {
    // Enhanced soft circular points with stronger edge effects
    vec2 coord = 2.0 * gl_PointCoord - 1.0;
    float r = dot(coord, coord);

    if (r > 1.0) {
        discard;
    }

    // Stronger radial fade for wave-like effect
    float fade = 1.0 - smoothstep(0.7, 1.0, r);

    // Add subtle radial color variation
    vec3 finalColor = vColor * (1.0 + 0.1 * (1.0 - r));

    fragColor = vec4(finalColor, vOpacity * fade);
}
