const TAU = Math.PI * 2;

// Scale factors to ensure geometry remains visible in clip space
// now that offset can go up to ±2
const PHASE_SCALE = 0.5;
const RADIUS_SCALE = 0.5;

export const PatternType = {
  ORIGIN: 'origin',
  CIRCLE: 'circle',
  SPHERE: 'sphere'
};

function generatePolarPoints(count, radiusFn = () => 1.0, offset = 0) {
  const pointCount = Math.max(3, Math.floor(count));
  const vertices = new Float32Array(pointCount * 2);

  // Instead of offset * TAU, scale offset to avoid geometry escaping view.
  // At offset=±2 => ±2 * TAU * 0.5 => ±2π total rotation shift.
  const phaseOffset = offset * TAU * PHASE_SCALE;

  for (let i = 0; i < pointCount; i++) {
    const phase = (i / pointCount) * TAU + phaseOffset;
    // Also apply a uniform scale to radius so that the pattern is within clip space.
    const radius = radiusFn(phase) * RADIUS_SCALE;

    vertices[i * 2] = radius;
    vertices[i * 2 + 1] = phase;
  }

  return vertices;
}

// Simplified radius functions
const radiusFunctions = {
  origin: () => 0.0,
  circle: () => 1.0,
  sphere: () => 1.0
};

export function generatePattern(type, maxCount, offset = 0) {
  const radiusFn = radiusFunctions[type.toLowerCase()];
  if (!radiusFn) {
    throw new Error(`Unknown pattern type: ${type}`);
  }
  return generatePolarPoints(maxCount, radiusFn, offset);
}
