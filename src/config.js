const TAU = Math.PI * 2;

const Config = {
  // Energy controls dimensional stacking
  ENERGY_RANGE: [0, Math.PI * 4],

  // Base number of points for all patterns
  BASE_DENSITY: 720,  // Double cover of points
  MAX_VERTICES: 1440,

  CONTROL_RANGES: {
    offset: {
      type: WebGL2RenderingContext.FLOAT,
      size: 1,
      range: {
        min: -2,
        max: 2,
        default: 0
      }
    },
    energy: {
      type: WebGL2RenderingContext.FLOAT,
      size: 1,
      range: {
        min: 0,
        max: Math.PI * 4,
        default: 12.0
      }
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
    theory: {
      vertex: '/shaders/theory.vert',
      fragment: '/shaders/theory.frag'
    },
    basic: {
      vertex: '/shaders/basic.vert',
      fragment: '/shaders/basic.frag'
    },
    debug: {
      vertex: '/shaders/debug.vert',
      fragment: '/shaders/debug.frag'
    }
  }
};

export default Config;
