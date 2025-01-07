const TAU = Math.PI * 2;

// Scale factors to ensure geometry remains visible in clip space
const PHASE_SCALE = 1.0;  // Allow full phase range overlap
const RADIUS_SCALE = 0.5; // Keep radius properly scaled

export const Patterns = {
  ORIGIN: 'origin',
  CIRCLE: 'circle',
  CLOVER: 'clover'
};

function generatePolarPoints(count, radiusFn = () => 1.0, offset = 0) {
  const pointCount = Math.max(3, Math.floor(count));
  const vertices = new Float32Array(pointCount * 2);
  const phaseOffset = offset * TAU * PHASE_SCALE;
  for (let i = 0; i < pointCount; i++) {
    const phase = (i / pointCount) * 2 * TAU - TAU + phaseOffset;
    const radius = radiusFn(phase) * RADIUS_SCALE;

    vertices[i * 2] = radius;
    vertices[i * 2 + 1] = phase;
  }

  return vertices;
}

// Pattern-specific radius functions
const radiusFunctions = {
  origin: () => 0.0,
  circle: () => 1.0,
  clover: (phase) => 2.0 * Math.cos(phase) * Math.sin(phase),
};

export function generatePattern(type, maxCount, offset = 0) {
  const radiusFn = radiusFunctions[type.toLowerCase()];
  if (!radiusFn) {
    throw new Error(`Unknown pattern type: ${type}`);
  }
  return generatePolarPoints(maxCount, radiusFn, offset);
}
