import Config from '../config';
import Shader from './shader';
import Params from './params';
import { PatternType, generatePattern } from './patterns';

export default class Renderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.gl = null;
    this.shader = null;
    this.params = new Params();

    this.patternBuffer = null;
    this.patternLocation = -1;
    this.currentPattern = PatternType.CIRCLE;
    this._maxVerts = Config.MAX_VERTICES;
    this.contextLost = false;

    this._handleContextLost = this._handleContextLost.bind(this);
    this._handleContextRestored = this._handleContextRestored.bind(this);

    this._initGL();
  }

  _initGL() {
    this.gl = this.canvas.getContext('webgl2', Config.WEBGL_CONTEXT_OPTIONS);
    if (!this.gl) {
      throw new Error('WebGL 2 not supported');
    }

    this.shader = new Shader(this.gl);

    const gl = this.gl;
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.viewport(0, 0, this.canvas.width, this.canvas.height);

    this.canvas.addEventListener('webglcontextlost', this._handleContextLost, false);
    this.canvas.addEventListener('webglcontextrestored', this._handleContextRestored, false);
  }

  getRendererInfo() {
    return this.gl.getParameter(this.gl.RENDERER) || 'unknown renderer';
  }

  async loadProgram(vertexPath, fragmentPath) {
    try {
      this.shader.cleanup();
      await this.shader.load(vertexPath, fragmentPath);
      this.shader.use();

      // Get discovered uniforms and their ranges
      const activeUniforms = this.shader.getActiveUniforms();

      // Initialize parameters with discovered uniforms
      this.params.initFromUniforms(activeUniforms);

      // We set initial values from the uniform range definitions themselves.
      // If 'energy' is discovered, it's already from Config.CONTROL_RANGES.energy.
      // For everything else, we have [-2, 2].
      const defaults = {};
      activeUniforms.forEach((info, name) => {
        defaults[name] = info.range.default;
      });
      this.params.set(defaults);

      this._createGeometry();
      this.update(this.params.getAll());

      // Return discovered uniforms for UI control generation
      return Object.fromEntries(activeUniforms);
    } catch (err) {
      console.error('Program load failed:', err);
      throw err;
    }
  }

  setPattern(type) {
    if (this.currentPattern === type) return;
    console.log('Changing pattern to:', type);
    this.currentPattern = type;
    this._createGeometry();
    this.render();
  }

  render() {
    if (this.contextLost || !this.shader.program) return;
    const gl = this.gl;

    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    if (this.patternLocation >= 0) {
      gl.bindBuffer(gl.ARRAY_BUFFER, this.patternBuffer);
      gl.enableVertexAttribArray(this.patternLocation);
      gl.vertexAttribPointer(this.patternLocation, 2, gl.FLOAT, false, 0, 0);
    }

    const values = this.params.getAll();
    const energy = values.energy ?? Config.DEFAULT_ENERGY;
    const energyFloor = Math.floor(energy);
    const instanceCount = Math.max(0, energyFloor + 1);

    const drawCount = Math.min(Config.BASE_DENSITY, this._maxVerts);

    console.log('Render state:', {
      pattern: this.currentPattern,
      energy,
      drawCount,
      instanceCount,
      params: values
    });

    // Use drawArraysInstanced to replicate the geometry instanceCount times
    gl.drawArraysInstanced(gl.POINTS, 0, drawCount, instanceCount);
  }

  _createGeometry() {
    const gl = this.gl;
    const values = this.params.getAll();
    const offset = values.offset ?? 0;  // If not present, 0

    const verts = generatePattern(this.currentPattern, Config.BASE_DENSITY, offset);

    if (this.patternBuffer) gl.deleteBuffer(this.patternBuffer);
    this.patternBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.patternBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);

    this.patternLocation = gl.getAttribLocation(this.shader.program, 'pattern');

    console.log('Geometry created:', {
      pattern: this.currentPattern,
      vertexCount: verts.length / 2,
      attributeLocation: this.patternLocation,
      offset
    });
  }

  update(updates) {
    if (this.contextLost || !this.shader.program) return;

    const prevParams = this.params.getAll();
    this.params.set(updates);
    const newParams = this.params.getAll();

    // Check if offset changed - requires geometry update
    if (prevParams.offset !== newParams.offset) {
      this._createGeometry();
    }

    this.shader.use();

    // Update shader uniforms
    Object.entries(newParams).forEach(([name, value]) => {
      if (this.shader.hasUniform(name)) {
        this.shader.setUniform(name, value);
      }
    });

    this.render();
  }

  // Return current parameter information for UI
  getControls() {
    const ranges = this.params.getAllRanges();
    const values = this.params.getAll();

    return Object.entries(ranges).map(([name, range]) => ({
      name,
      ...range,
      value: values[name] ?? range.default
    }));
  }

  dispose() {
    this._cleanup();
    this.canvas.removeEventListener('webglcontextlost', this._handleContextLost);
    this.canvas.removeEventListener('webglcontextrestored', this._handleContextRestored);
  }

  _cleanup() {
    if (this.patternBuffer) {
      this.gl.deleteBuffer(this.patternBuffer);
      this.patternBuffer = null;
    }
    this.shader?.cleanup();
  }

  _handleContextLost(e) {
    e.preventDefault();
    console.log('WebGL context lost');
    this.contextLost = true;
  }

  async _handleContextRestored() {
    console.log('WebGL context restored');
    this.contextLost = false;
    if (this.shader.vertexPath && this.shader.fragmentPath) {
      await this.loadProgram(this.shader.vertexPath, this.shader.fragmentPath);
    }
  }
}
