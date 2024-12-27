import React, { useState, useCallback, useEffect, useRef } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { ArrowUpDown, Maximize2, Activity, Move, Combine } from 'lucide-react';

// ------------------- VERTEX SHADER ---------------------
const vertexShader = `
  attribute vec2 position;
  attribute float layer;
  attribute float phase;
  attribute float isVertex;
  attribute float isLine;

  uniform float dimension;
  uniform float waveAmplitude;
  uniform float attractorStrength;
  uniform float symmetryBalance;
  uniform float lemniscateInfluence;
  uniform float rotationAngle;

  varying vec3 vColor;
  varying float vOpacity;
  varying float vIsVertex;
  varying float vIsLine;

  const float PI = 3.141592653589793;
  const float TAU = 6.283185307179586;

  // ------------------------------------------------------
  // Double-lobed Bernoulli Lemniscate (Variant B):
  //   - We double the angle: u = 2*t
  //   - We flip sin(u) => -sin(u) to orient downward
  // ------------------------------------------------------
  vec2 getLemniscatePosition(float t) {
    float u = 2.0 * t;
    float sint = -sin(u);   // negative to flip vertically
    float cost = cos(u);

    float denom = 1.0 + sint * sint;
    return vec2(
      cost / denom,
      cost * sint / denom
    );
  }

  // ------------------------------------------------------
  // HSV -> RGB
  // ------------------------------------------------------
  vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0/3.0, 1.0/3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
  }

  // ------------------------------------------------------
  // Dimension-based color with updated brightness
  //   S=0.85, V=0.85 (or slight tweak for baseDim)
  // ------------------------------------------------------
  vec3 getColor(float layer, float dim) {
    float baseDim = floor(dim);
    float fracPart = dim - baseDim;
    float hue = mod((layer + 1.0) * TAU * TAU, 360.0) / 360.0;

    if (layer < baseDim) {
      // Fully emerged dimension
      return hsv2rgb(vec3(hue, 0.85, 0.85));
    }
    if (layer == baseDim) {
      // Partially emerged dimension
      float sat = 0.15 + 0.85 * fracPart;
      float val = 0.85;
      return hsv2rgb(vec3(hue, sat, val));
    }
    // Not emerged at all
    return vec3(0.0);
  }

  // ------------------------------------------------------
  // Dimension Emergence Opacity
  //  - Below baseDim => fully emerged => 0.9
  //  - Exactly baseDim => partial => 0.1..0.9
  //  - Above => 0
  // ------------------------------------------------------
  float getDimOpacity(float layer, float dim) {
    float baseDim = floor(dim);
    float fracPart = dim - baseDim;

    if (layer < baseDim) {
      // fully emerged
      return 0.9;
    }
    else if (abs(layer - baseDim) < 0.5) {
      // partial
      // range: [0.1..0.9] => 0.1 + 0.8*fracPart
      return 0.1 + 0.8 * fracPart;
    }
    // not emerged => 0
    return 0.0;
  }

  void main() {
    vIsVertex = isVertex;
    vIsLine = isLine;

    // ----------------------------------------------------
    // Dimension-based anchor (with "nonLinearPhase")
    // ----------------------------------------------------
    float basePhase = TAU * layer / max(0.1, dimension);
    float nonLinearPhase = basePhase + (symmetryBalance - 1.0) * PI * sin(basePhase);

    // Let dimension origin scale from radius=1 to 2 with attractor
    float dimensionRadius = mix(1.0, 2.0, attractorStrength);
    vec2 dimensionOrigin = dimensionRadius * vec2(
      cos(nonLinearPhase),
      sin(nonLinearPhase)
    );

    // ----------------------------------------------------
    // 1) Compute a "base" circle around (0,0)
    // ----------------------------------------------------
    vec2 basePos = vec2(0.0);
    if (isVertex > 0.5 || isLine > 0.5) {
      // The dimension's main vertex on that scaled circle
      basePos = dimensionOrigin;
      gl_PointSize = (isVertex > 0.5) ? 8.0 : 1.0;

    } else {
      // "Normal" wave-based points
      float waveVal = sin(nonLinearPhase * (layer + 1.0));
      float wave = waveAmplitude * waveVal;    // in [-waveAmp..+waveAmp]
      float r = 1.0 + wave;

      // oldAttractorDist from original code
      float oldAttractorDist = attractorStrength * cos(phase - nonLinearPhase);
      r += oldAttractorDist;

      float c = cos(nonLinearPhase);
      float s = sin(nonLinearPhase);

      basePos = r * vec2(
        c * cos(phase) - s * sin(phase),
        c * sin(phase) + s * cos(phase)
      );

      gl_PointSize = 4.0;
    }

    // ----------------------------------------------------
    // 2) Lemniscate blending
    // ----------------------------------------------------
    vec2 lemnPos = getLemniscatePosition(phase + 0.5 * nonLinearPhase);
    vec2 blendedPos = mix(basePos, lemnPos, lemniscateInfluence);

    // ----------------------------------------------------
    // 3) Folding around dimensionOrigin
    // ----------------------------------------------------
    vec2 reflectionPos = 2.0 * dimensionOrigin - blendedPos;
    vec2 finalPosBeforeRotation = mix(blendedPos, reflectionPos, 0.0);

    // ----------------------------------------------------
    // 4) Rotation for final "camera" or global spin
    // ----------------------------------------------------
    mat2 rotationMat = mat2(
      cos(rotationAngle), -sin(rotationAngle),
      sin(rotationAngle),  cos(rotationAngle)
    );
    vec2 finalPos = rotationMat * finalPosBeforeRotation;

    // Output Position
    gl_Position = vec4(finalPos * 0.5, 0.0, 1.0);

    // ----------------------------------------------------
    // Color & dimension-based opacity
    // ----------------------------------------------------
    vColor = getColor(layer, dimension);

    // "Dimension Emergence" factor
    float dimFactor = getDimOpacity(layer, dimension);

    // Then multiply by base line/point opacities
    // e.g., lines=0.8, normal points=0.9, vertices=1.0
    float baseOpacity = 0.0;
    if (isVertex > 0.5) {
      baseOpacity = 1.0;
    } else if (isLine > 0.5) {
      baseOpacity = 0.8;
    } else {
      baseOpacity = 0.9;
    }

    vOpacity = baseOpacity * dimFactor;
  }
`;

// ------------------- FRAGMENT SHADER ---------------------
const fragmentShader = `
  precision mediump float;
  varying vec3 vColor;
  varying float vOpacity;
  varying float vIsVertex;
  varying float vIsLine;

  void main() {
    // For points, discard any fragment outside a circle
    if (vIsLine < 0.5) {
      vec2 cxy = 2.0 * gl_PointCoord - 1.0;
      float r = dot(cxy, cxy);
      if (r > 1.0) discard;
    }
    gl_FragColor = vec4(vColor, vOpacity);
  }
`;

const UltrasphereViz = () => {
  // Existing reactive state
  const [dimension, setDimension] = useState(12.0);
  const [layerDensity, setLayerDensity] = useState(4.0);
  const [waveAmplitude, setWaveAmplitude] = useState(0.0);
  const [attractorStrength, setAttractorStrength] = useState(0.0);
  const [symmetryBalance, setSymmetryBalance] = useState(1.0);
  const [lemniscateInfluence, setLemniscateInfluence] = useState(0.5);
  const [rotationAngle, setRotationAngle] = useState(0.0);

  // WebGL Refs
  const canvasRef = useRef(null);
  const glRef = useRef(null);
  const programRef = useRef(null);
  const vertexBufferRef = useRef(null);
  const lineBufferRef = useRef(null);

  // -------------------- Initialization --------------------
  const initGL = useCallback(() => {
    const canvas = canvasRef.current;
    const gl = canvas.getContext('webgl', { antialias: true });
    if (!gl) return;

    const program = gl.createProgram();
    const vShader = gl.createShader(gl.VERTEX_SHADER);
    const fShader = gl.createShader(gl.FRAGMENT_SHADER);

    gl.shaderSource(vShader, vertexShader);
    gl.shaderSource(fShader, fragmentShader);
    gl.compileShader(vShader);
    gl.compileShader(fShader);

    if (!gl.getShaderParameter(vShader, gl.COMPILE_STATUS)) {
      console.error('Vertex shader failed to compile:', gl.getShaderInfoLog(vShader));
      return;
    }
    if (!gl.getShaderParameter(fShader, gl.COMPILE_STATUS)) {
      console.error('Fragment shader failed to compile:', gl.getShaderInfoLog(fShader));
      return;
    }

    gl.attachShader(program, vShader);
    gl.attachShader(program, fShader);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      console.error('Shader program failed to link:', gl.getProgramInfoLog(program));
      return;
    }

    gl.useProgram(program);

    glRef.current = gl;
    programRef.current = program;

    vertexBufferRef.current = gl.createBuffer();
    lineBufferRef.current = gl.createBuffer();

    // Basic GL setup
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    // Attempt to thicken lines (may be ignored on some platforms)
    gl.lineWidth(2.0);
  }, []);

  // -------------------- Render Function -------------------
  const render = useCallback(() => {
    const gl = glRef.current;
    const program = programRef.current;
    if (!gl || !program) return;

    gl.clear(gl.COLOR_BUFFER_BIT);

    // Update uniforms
    gl.uniform1f(gl.getUniformLocation(program, 'dimension'), dimension);
    gl.uniform1f(gl.getUniformLocation(program, 'waveAmplitude'), waveAmplitude);
    gl.uniform1f(gl.getUniformLocation(program, 'attractorStrength'), attractorStrength);
    gl.uniform1f(gl.getUniformLocation(program, 'symmetryBalance'), symmetryBalance);
    gl.uniform1f(gl.getUniformLocation(program, 'lemniscateInfluence'), lemniscateInfluence);
    gl.uniform1f(gl.getUniformLocation(program, 'rotationAngle'), rotationAngle);

    const numPoints = Math.floor(180 * layerDensity);
    const vertices = [];
    const lines = [];
    const baseDim = Math.floor(dimension);

    // 1) Dimension "origin" vertices
    const vertexPositions = [];
    for (let d = 0; d <= baseDim; d++) {
      const weight = d < baseDim ? 1.0 : dimension - baseDim;
      if (weight <= 0) continue;

      const phase = (-2 * Math.PI * d) / Math.max(0.1, dimension);
      const x = Math.cos(phase);
      const y = Math.sin(phase);

      vertexPositions.push({ x, y, d, phase });

      vertices.push(
        x, y,      // position
        d,         // layer
        phase,     // phase
        1.0,       // isVertex
        0.0        // isLine
      );
    }

    // Connect dimension vertices with lines
    for (let i = 0; i < vertexPositions.length; i++) {
      const v1 = vertexPositions[i];
      const v2 = vertexPositions[(i + 1) % vertexPositions.length];
      lines.push(
        v1.x, v1.y, v1.d, v1.phase, 0.0, 1.0,
        v2.x, v2.y, v2.d, v2.phase, 0.0, 1.0
      );
    }

    // 2) Normal "inner" points
    for (let i = 0; i < numPoints; i++) {
      const phase = (-2 * Math.PI * i) / numPoints;
      for (let d = 0; d <= baseDim; d++) {
        const weight = d < baseDim ? 1.0 : dimension - baseDim;
        if (weight <= 0) continue;

        vertices.push(
          Math.cos(phase), Math.sin(phase),
          d,
          phase,
          0.0,
          0.0
        );
      }
    }

    // Setup attribute pointers
    const stride = 6 * 4; // floats per vertex * 4 bytes
    const setupAttributes = (buffer, data) => {
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);

      const positionLoc = gl.getAttribLocation(program, 'position');
      const layerLoc = gl.getAttribLocation(program, 'layer');
      const phaseLoc = gl.getAttribLocation(program, 'phase');
      const isVertexLoc = gl.getAttribLocation(program, 'isVertex');
      const isLineLoc = gl.getAttribLocation(program, 'isLine');

      gl.enableVertexAttribArray(positionLoc);
      gl.enableVertexAttribArray(layerLoc);
      gl.enableVertexAttribArray(phaseLoc);
      gl.enableVertexAttribArray(isVertexLoc);
      gl.enableVertexAttribArray(isLineLoc);

      gl.vertexAttribPointer(positionLoc, 2, gl.FLOAT, false, stride, 0);
      gl.vertexAttribPointer(layerLoc, 1, gl.FLOAT, false, stride, 2 * 4);
      gl.vertexAttribPointer(phaseLoc, 1, gl.FLOAT, false, stride, 3 * 4);
      gl.vertexAttribPointer(isVertexLoc, 1, gl.FLOAT, false, stride, 4 * 4);
      gl.vertexAttribPointer(isLineLoc, 1, gl.FLOAT, false, stride, 5 * 4);
    };

    // Draw lines
    setupAttributes(lineBufferRef.current, lines);
    gl.drawArrays(gl.LINES, 0, lines.length / 6);

    // Draw points
    setupAttributes(vertexBufferRef.current, vertices);
    gl.drawArrays(gl.POINTS, 0, vertices.length / 6);
  }, [
    dimension,
    layerDensity,
    waveAmplitude,
    attractorStrength,
    symmetryBalance,
    lemniscateInfluence,
    rotationAngle
  ]);

  // Initialize on mount
  useEffect(() => {
    initGL();
  }, [initGL]);

  // Re-render when relevant state changes
  useEffect(() => {
    render();
  }, [render]);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Ultrasphere (G₀)</span>
          <span className="text-sm">
            d = {dimension.toFixed(2)}
            {Math.abs(dimension - Math.E) < 0.015 && " ≈ e"}
            {Math.abs(dimension - 1.618033988749895) < 0.015 && " ≈ φ"}
            {Math.abs(dimension - 2 * Math.PI) < 0.015 && " ≈ τ"}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Sliders */}
          <div className="space-y-4">
            {[
              { icon: ArrowUpDown, value: dimension, setValue: setDimension, min: 0.1, max: 24, label: "Dimension" },
              { icon: Maximize2, value: layerDensity, setValue: setLayerDensity, min: 0.1, max: 8, label: "Layer Density" },
              { icon: Activity, value: waveAmplitude, setValue: setWaveAmplitude, min: -1, max: 1, label: "Wave Amplitude" },
              { icon: Move, value: attractorStrength, setValue: setAttractorStrength, min: -1, max: 1, label: "Attractor Strength" },
              { icon: Combine, value: symmetryBalance, setValue: setSymmetryBalance, min: 0, max: 2, label: "Symmetry Distribution" },
              { icon: Combine, value: lemniscateInfluence, setValue: setLemniscateInfluence, min: 0, max: 1, label: "Lemniscate Influence" },
              { icon: Combine, value: rotationAngle, setValue: setRotationAngle, min: 0, max: 6.283185307, label: "Rotation" },
            ].map(({ icon: Icon, value, setValue, min, max, label }) => (
              <div key={label} className="flex items-center space-x-4">
                <Icon className="h-4 w-4" />
                <Slider
                  value={[value]}
                  min={min}
                  max={max}
                  step={0.01}
                  onValueChange={([v]) => setValue(v)}
                  className="w-full"
                />
                <span className="text-sm">{label}</span>
              </div>
            ))}
          </div>

          {/* Canvas */}
          <canvas
            ref={canvasRef}
            width={800}
            height={800}
            className="w-full border rounded-lg"
            style={{ width: '100%', height: 'auto' }}
          />
        </div>
      </CardContent>
    </Card>
  );
};

export default UltrasphereViz;
