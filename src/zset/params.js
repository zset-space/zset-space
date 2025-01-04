export default class Params {
  constructor() {
    this.values = new Map();        // Current parameter values
    this.ranges = new Map();        // Parameter ranges
    this.pattern = null;            // Current pattern type
  }

  // Initialize parameters based on discovered shader uniforms
  initFromUniforms(uniforms) {
    uniforms.forEach((info, name) => {
      // info.range is determined in the shader code, then passed here
      this.ranges.set(name, info.range);

      if (!this.values.has(name)) {
        this.values.set(name, info.range.default);
      }
    });
  }

  // Update one or more parameter values
  set(updates) {
    if (typeof updates === 'object') {
      Object.entries(updates).forEach(([name, value]) => {
        if (this.ranges.has(name)) {
          const range = this.ranges.get(name);
          // Clamp value to valid range
          const clamped = Math.min(Math.max(value, range.min), range.max);
          this.values.set(name, clamped);
        }
      });
    }
  }

  // Get current value of a parameter
  get(name) {
    return this.values.get(name);
  }

  // Get all current parameter values
  getAll() {
    const result = {};
    this.values.forEach((value, name) => {
      result[name] = value;
    });
    return result;
  }

  // Get range information for a parameter
  getRange(name) {
    return this.ranges.get(name);
  }

  // Get all parameter ranges
  getAllRanges() {
    const result = {};
    this.ranges.forEach((range, name) => {
      result[name] = range;
    });
    return result;
  }

  // Set the current pattern type
  setPattern(pattern) {
    this.pattern = pattern;
  }

  // Get the current pattern type
  getPattern() {
    return this.pattern;
  }

  // Reset all parameters to their default values
  reset() {
    this.ranges.forEach((range, name) => {
      this.values.set(name, range.default);
    });
    this.pattern = null;
  }

  // Check if a parameter exists
  has(name) {
    return this.ranges.has(name);
  }

  // Get list of all parameter names
  getParameterNames() {
    return Array.from(this.ranges.keys());
  }
}
