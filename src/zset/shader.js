import Config from '../config';

export default class Shader {
  constructor(gl) {
    this.gl = gl;
    this.program = null;
    this.uniformLocations = new Map();
    this.activeUniforms = new Map();  // type info for active uniforms
    this.attributeLocations = new Map();

    this.vertexPath = null;
    this.fragmentPath = null;
  }

  async load(vertexPath, fragmentPath) {
    this.vertexPath = vertexPath;
    this.fragmentPath = fragmentPath;

    // Load and compile shaders
    const [vert, frag] = await Promise.all([
      this._createShader(this.gl.VERTEX_SHADER, vertexPath),
      this._createShader(this.gl.FRAGMENT_SHADER, fragmentPath)
    ]);

    const program = this.gl.createProgram();
    this.gl.attachShader(program, vert);
    this.gl.attachShader(program, frag);
    this.gl.linkProgram(program);

    if (!this.gl.getProgramParameter(program, this.gl.LINK_STATUS)) {
      const info = this.gl.getProgramInfoLog(program);
      this.gl.deleteProgram(program);
      throw new Error(`Program link failed: ${info}`);
    }

    this.gl.deleteShader(vert);
    this.gl.deleteShader(frag);

    this.program = program;

    // Discover uniforms immediately after program creation
    await this.discoverUniforms();
  }

  use() {
    if (this.program) {
      this.gl.useProgram(this.program);
    }
  }

  async discoverUniforms() {
    if (!this.program) return new Map();

    this.uniformLocations.clear();
    this.activeUniforms.clear();

    const numUniforms = this.gl.getProgramParameter(
      this.program,
      this.gl.ACTIVE_UNIFORMS
    );

    for (let i = 0; i < numUniforms; i++) {
      const info = this.gl.getActiveUniform(this.program, i);
      if (!info) continue;

      const name = info.name;
      const location = this.gl.getUniformLocation(this.program, name);

      // If the uniform name is "energy", we use [0, 4π].
      // Otherwise, we default to [-2, 2].
      let uniformRange;
      if (name === 'energy') {
        uniformRange = Config.CONTROL_RANGES.energy.range;
      } else {
        // Regardless of what might be in Config, we force [-2, 2] for non-energy
        uniformRange = {
          min: -2,
          max: 2,
          default: 0
        };
      }

      this.uniformLocations.set(name, location);
      this.activeUniforms.set(name, {
        type: info.type,
        size: info.size,
        range: uniformRange
      });

      console.log(`Discovered uniform: ${name}`, {
        type: info.type,
        size: info.size,
        location
      });
    }

    return this.activeUniforms;
  }

  getActiveUniforms() {
    return this.activeUniforms;
  }

  hasUniform(name) {
    return this.uniformLocations.has(name);
  }

  setUniform(name, value) {
    const location = this.uniformLocations.get(name);
    if (location === undefined) return false;

    const info = this.activeUniforms.get(name);
    if (!info) return false;

    switch (info.type) {
      case this.gl.FLOAT:
        this.gl.uniform1f(location, value);
        break;
      case this.gl.FLOAT_VEC2:
        this.gl.uniform2fv(location, value);
        break;
      case this.gl.FLOAT_VEC3:
        this.gl.uniform3fv(location, value);
        break;
      case this.gl.FLOAT_VEC4:
        this.gl.uniform4fv(location, value);
        break;
      case this.gl.INT:
        this.gl.uniform1i(location, value);
        break;
      // Add other types if needed
      default:
        console.warn(`Unsupported uniform type for ${name}:`, info.type);
        return false;
    }
    return true;
  }

  cleanup() {
    if (this.program) {
      this.gl.deleteProgram(this.program);
      this.program = null;
    }
    this.uniformLocations.clear();
    this.activeUniforms.clear();
    this.attributeLocations.clear();
  }

  async _createShader(type, path) {
    const resp = await fetch(path);
    if (!resp.ok) {
      throw new Error(`Failed to fetch shader at ${path}: ${resp.statusText}`);
    }
    const source = await resp.text();

    const shader = this.gl.createShader(type);
    this.gl.shaderSource(shader, source);
    this.gl.compileShader(shader);

    if (!this.gl.getShaderParameter(shader, this.gl.COMPILE_STATUS)) {
      const log = this.gl.getShaderInfoLog(shader);
      this.gl.deleteShader(shader);
      throw new Error(`Shader compile failed: ${log}`);
    }

    return shader;
  }
}
