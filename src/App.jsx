import React, { useState, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { ArrowUpDown, RotateCcw, Maximize2, Activity, Move, Combine } from 'lucide-react';

const UltrasphereViz = () => {
  //const [dimension, setDimension] = useState(2 * Math.PI);
  //const [dimension, setDimension] = useState(Math.E);
  const [dimension, setDimension] = useState(3);
  const [phaseOffset, setPhaseOffset] = useState(0);
  const [layerDensity, setLayerDensity] = useState(0.5);
  //const [waveAmplitude, setWaveAmplitude] = useState(0);
  const [waveAmplitude, setWaveAmplitude] = useState(1/2);
  //const [attractorStrength, setAttractorStrength] = useState(1);
  const [attractorStrength, setAttractorStrength] = useState(0);
  const [symmetryBalance, setSymmetryBalance] = useState(1);

  const radius = 100;

  const getInterpolatedColor = useCallback((layer, dimension) => {
    const baseDim = Math.floor(dimension);
    const fracPart = dimension - baseDim;

    // Special dimension handling
    const isNearE = Math.abs(dimension - Math.E) < 0.015;
    const isNearPhi = Math.abs(dimension - 1.618033988749895) < 0.015;
    // Pretty sure this is a black hole
    const isNearTau = Math.abs(dimension - 2 * Math.PI) < 0.015;

    if (isNearE || isNearPhi || isNearTau) {
      const specialHue = isNearE ? 120 : (isNearPhi ? 60 : 280);
      return `hsl(${specialHue}, 100%, 50%)`;
    }

    // Handle sub-unity dimensions
    if (dimension < 1) {
      return `hsl(280, 85%, 50%)`; // Consistent purple for quantum regime
    }

    // For completed layers (layer < baseDim), use fixed colors
    if (layer < baseDim) {
      const baseHue = ((layer + 1) * 105) % 360; // Fixed color per layer
      return `hsl(${baseHue}, 85%, 50%)`;
    }

    // Only the emerging dimension (layer === baseDim) gets transition colors
    if (layer === baseDim) {
      const emergingBaseHue = ((baseDim + 1) * 105) % 360;
      const saturation = 85 + (15 * fracPart);
      const lightness = 50 - (10 * (1 - fracPart)); // Slightly darker when starting to emerge
      return `hsl(${emergingBaseHue}, ${saturation}%, ${lightness}%)`;
    }

    // Future dimensions (layer > baseDim) should not be visible
    return `hsla(0, 0%, 0%, 0)`;
  }, []);

  const getLayerPhase = useCallback((layerIndex, basePhase, t = 0) => {
    const currentDim = dimension + t;

    // Simple continuous phase calculation
    const naturalPhase = (2 * Math.PI * layerIndex) / Math.max(0.1, currentDim);
    const symmetryPhase = naturalPhase * symmetryBalance;

    return symmetryPhase;
  }, [dimension, symmetryBalance]);

  const projectPoint = useCallback((angle, r, basis) => {
    const attractorAngle = getLayerPhase(basis.layer, 0);
    const attractorDist = attractorStrength * Math.cos(angle - attractorAngle);

    const baseWave = Math.sin(attractorAngle * (basis.layer + 1));
    const modulation = waveAmplitude * baseWave;

    const modR = r * (1 + modulation + attractorDist);

    const x = modR * (basis.cos * Math.cos(angle) - basis.sin * Math.sin(angle));
    const y = modR * (basis.cos * Math.sin(angle) + basis.sin * Math.cos(angle));

    return { x, y };
}, [dimension, waveAmplitude, getLayerPhase, attractorStrength]);

  const getProjectionMatrix = useCallback((dim) => {
    const baseDim = Math.floor(dim);
    const fracPart = dim - baseDim;

    const bases = [];
    for (let d = 0; d < baseDim + 1; d++) {
        const phase = getLayerPhase(d, 0);
        const weight = d < baseDim ? 1.0 : fracPart;

        if (weight > 0) {
            bases.push({
                cos: Math.cos(phase),
                sin: Math.sin(phase),
                weight,
                layer: d,
                phase
            });
        }
  }

    return bases;
  }, [getLayerPhase]);

  const getMeasure = useCallback((r, dim) => {
    const layerScale = 1 / layerDensity;

    if (dim < 1) {
      const quantumEffect = 0.3 * (1 - dim) * Math.exp(-r/radius);
      return Math.min(1, layerScale + quantumEffect);
    }

    return Math.min(1, layerScale);
  }, [layerDensity, radius]);

  const generatePoints = useCallback(() => {
    const points = [];
    const numPoints = Math.floor(180 * layerDensity);
    const angleStep = (2 * Math.PI) / numPoints;
    const bases = getProjectionMatrix(dimension);

    for (let i = 0; i < numPoints; i++) {
      const angle = i * angleStep;

      bases.forEach(basis => {
        if (basis.weight > 0) {
          const r = radius;
          const projected = projectPoint(angle, r, basis);
          const measure = getMeasure(r/radius, dimension) * basis.weight;

          points.push({
            x: projected.x,
            y: projected.y,
            measure,
            layer: basis.layer,
            angle,
            phase: basis.phase
          });
        }
      });
    }

    if (dimension < 1) {
      const quantumPoints = Math.floor(16 * (1 - dimension));
      const quantumRadius = radius * (1 - dimension);

      for (let i = 0; i < quantumPoints; i++) {
        const angle = (2 * Math.PI * i) / quantumPoints;
        const spread = radius * 0.1 * (1 - dimension);

        for (let j = 0; j < 3; j++) {
          const r = quantumRadius + (Math.random() - 0.5) * spread;
          const phase = angle + (Math.random() - 0.5) * (1 - dimension) * Math.PI/4;

          points.push({
            x: r * Math.cos(phase),
            y: r * Math.sin(phase),
            measure: dimension,
            layer: -1,
            angle: phase,
            phase
          });
        }
      }
    }

    return points;
  }, [dimension, getProjectionMatrix, projectPoint, getMeasure, layerDensity, radius]);

  const renderPhaseLines = useCallback((bases) => {
    if (dimension < 1)
      return null;

    const lines = [];
    const r = + radius + radius*attractorStrength;
    const baseDim = Math.floor(dimension);
    const fracPart = dimension - baseDim;

    const nextPhase = (2 * Math.PI * (bases.length)) / (baseDim + 1);
    const nextX = r * Math.cos(nextPhase);
    const nextY = r * Math.sin(nextPhase);

    const transitionWidth = 0.2;
    const transitionFactor = Math.min(fracPart / transitionWidth, 1);

    bases.forEach((basis, i) => {
      const currentX = r * Math.cos(basis.phase);
      const currentY = r * Math.sin(basis.phase);

      const nextBasis = bases[i < bases.length - 1 ? i + 1 : 0];
      lines.push(
        <line
          key={`connection-${i}`}
          x1={currentX}
          y1={currentY}
          x2={r * Math.cos(nextBasis.phase)}
          y2={r * Math.sin(nextBasis.phase)}
          stroke="rgba(100,100,100,0.7)"
          strokeWidth="1"
          strokeDasharray={`${4},4`}
        />
      );

      lines.push(
        <circle
          key={`vertex-${i}`}
          cx={currentX}
          cy={currentY}
          r="2.5"
          fill={getInterpolatedColor(i, dimension)}
          stroke="rgba(255,255,255,0.5)"
          strokeWidth="0.5"
        />
      );
    });

    return lines;
  }, [dimension, radius, attractorStrength, getInterpolatedColor]);

  const renderUltrasphere = useCallback(() => {
    const points = generatePoints();
    const bases = getProjectionMatrix(dimension);
    const centerX = 200;
    const centerY = 200;

    return (
      <g transform={`translate(${centerX}, ${centerY})`}>
        {renderPhaseLines(bases)}
        {points.map((point, i) => {
          const color = point.layer === -1 ?
            `hsla(0, 100%, 50%, ${point.measure})` :
            getInterpolatedColor(point.layer, dimension);

          const opacity = Math.min(0.8, point.measure * (0.5 + 0.5/layerDensity));

          return (
            <circle
              key={i}
              cx={point.x}
              cy={point.y}
              r={point.layer === -1 ? 2 : 1.5}
              fill={color}
              style={{
                transition: 'all 50ms ease-out',
                opacity
              }}
            />
          );
        })}
      </g>
    );
  }, [generatePoints, dimension, layerDensity, getProjectionMatrix, renderPhaseLines, getInterpolatedColor]);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Ultrasphere Visualization (G₀)</span>
          <span className="text-sm">
            Dimension: {dimension.toFixed(2)}
            {Math.abs(dimension - Math.E) < 0.015 && " ≈ e"}
            {Math.abs(dimension - 1.618033988749895) < 0.015 && " ≈ φ"}
            {Math.abs(dimension - 2 * Math.PI) < 0.015 && " ≈ τ"}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <ArrowUpDown className="h-4 w-4" />
              <Slider
                value={[dimension]}
                min={0.1}
                max={24}
                step={0.01}
                onValueChange={([d]) => setDimension(d)}
                className="w-full"
              />
              <span className="text-sm">Dimension</span>
            </div>

            <div className="flex items-center space-x-4">
              <RotateCcw className="h-4 w-4" />
              <Slider
                value={[phaseOffset]}
                min={0}
                max={2 * Math.PI}
                step={0.01}
                onValueChange={([p]) => setPhaseOffset(p)}
                className="w-full"
              />
              <span className="text-sm">Phase Offset</span>
            </div>

            <div className="flex items-center space-x-4">
              <Maximize2 className="h-4 w-4" />
              <Slider
                value={[layerDensity]}
                min={0.1}
                max={2}
                step={0.01}
                onValueChange={([d]) => setLayerDensity(d)}
                className="w-full"
              />
              <span className="text-sm">Layer Density</span>
            </div>

            <div className="flex items-center space-x-4">
              <Activity className="h-4 w-4" />
              <Slider
                value={[waveAmplitude]}
                min={0}
                max={1}
                step={0.01}
                onValueChange={([a]) => setWaveAmplitude(a)}
                className="w-full"
              />
              <span className="text-sm">Wave Amplitude</span>
            </div>

            <div className="flex items-center space-x-4">
              <Move className="h-4 w-4" />
              <Slider
                value={[attractorStrength]}
                min={0}
                max={1}
                step={0.01}
                onValueChange={([a]) => setAttractorStrength(a)}
                className="w-full"
              />
              <span className="text-sm">Attractor Strength</span>
            </div>

            <div className="flex items-center space-x-4">
              <Combine className="h-4 w-4" />
              <Slider
                value={[symmetryBalance]}
                min={0.5}
                max={1.5}
                step={0.01}
                onValueChange={([s]) => setSymmetryBalance(s)}
                className="w-full"
              />
              <span className="text-sm">Symmetry Balance</span>
            </div>
          </div>

          <svg
            viewBox="0 0 400 400"
            className="w-full border rounded-lg bg-white"
          >
            {renderUltrasphere()}
          </svg>
        </div>
      </CardContent>
    </Card>
  );
};

export default UltrasphereViz;
