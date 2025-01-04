const TAU = Math.PI * 2;

const Config = {
  // Energy controls dimensional stacking
  ENERGY_RANGE: [0, Math.PI * 4],
  DEFAULT_ENERGY: Math.PI * 2,

  // Base number of points for all patterns
  BASE_DENSITY: 360,  // Full circle of points
  MAX_VERTICES: 1440,

  // For non-energy controls, we use [-2, 2]. The default is 0.
  // We specifically track 'energy' with [0, 4π].
  // Pattern or shader uniform name 'energy' => [0, 4π], all else => [-2, 2].
  CONTROL_RANGES: {
    // The unique case is 'energy':
    energy: {
      min: 0,
      max: Math.PI * 4,
      default: Math.PI * 2
    },
    // If you want to define named controls that are definitely [-2, 2],
    // put them here. For example 'offset':
    offset: {
      min: -2,
      max: 2,
      default: 0
    }
  },

  CANVAS_SIZE: 800,

  WEBGL_CONTEXT_OPTIONS: {
    alpha: true,
    antialias: true,
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance'
  },

  // Shader definitions
  SHADERS: {
    basic: {
      vertex: '/shaders/basic.vert',
      fragment: '/shaders/basic.frag'
    },
    debug: {
      vertex: '/shaders/debug.vert',
      fragment: '/shaders/debug.frag'
    },
    theory: {
      vertex: '/shaders/theory.vert',
      fragment: '/shaders/theory.frag'
    }
  },

  DEFAULT_SHADER: 'basic'
};

export default Config;
