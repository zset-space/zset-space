import React, { useEffect, useRef, useState } from 'react';
import Renderer from './zset/renderer';
import Perf from './components/perf';
import Config from './config';
import { Patterns } from './zset/patterns';
import './index.css';
import './app.css';

function SliderControl({ label, min, max, step = 0.01, value, onChange, disabled }) {
  const wrapperStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    margin: '0.5rem 0'
  };
  const labelStyle = {
    flexShrink: 0,
    width: '6rem',
    textAlign: 'right'
  };
  const valueStyle = {
    flexShrink: 0,
    width: '3rem',
    textAlign: 'right'
  };

  return (
    <div style={wrapperStyle}>
      <div style={labelStyle}>{label}</div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        disabled={disabled}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{ flexGrow: 1 }}
      />
      <div style={valueStyle}>{value.toFixed(2)}</div>
    </div>
  );
}

function DropdownControl({ label, value, options, onChange, disabled }) {
  const wrapperStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    margin: '0.5rem 0'
  };
  const labelStyle = {
    flexShrink: 0,
    width: '6rem',
    textAlign: 'right'
  };

  return (
    <div style={wrapperStyle}>
      <div style={labelStyle}>{label}</div>
      <select
        value={value}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value)}
        style={{ flexGrow: 1 }}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}

const patternOptions = Object.entries(Patterns).map(([key, value]) => ({
  value,
  label: key.toLowerCase()
}));

const shaderOptions = Object.keys(Config.SHADERS).map((key) => ({
  value: key,
  label: key
}));

export default function App() {
  const canvasRef = useRef(null);
  const engineRef = useRef(null);

  const [pattern, setPattern] = useState(Patterns.CIRCLE);
  const [shader, setShader] = useState(Object.keys(Config.SHADERS)[0]);
  const [controls, setControls] = useState([]);
  const [error, setError] = useState(null);
  const [initing, setIniting] = useState(true);

  useEffect(() => {
    if (!canvasRef.current) return;

    async function initRenderer() {
      setIniting(true);
      setError(null);

      try {
        engineRef.current?.dispose();
        engineRef.current = new Renderer(canvasRef.current);

        const { vertex, fragment } = Config.SHADERS[shader];
        await engineRef.current.loadProgram(vertex, fragment);

        const discovered = engineRef.current.getControls();
        const newShaderControls = discovered.map((ctrl) => ({
          name: ctrl.name,
          min: ctrl.min,
          max: ctrl.max,
          step: 0.01,
          value: ctrl.value
        }));
        setControls(newShaderControls);
      } catch (err) {
        console.error('Initialization error:', err);
        setError(err.message);
      } finally {
        setIniting(false);
      }
    }

    initRenderer();
    return () => engineRef.current?.dispose();
  }, [shader]);

  useEffect(() => {
    if (!engineRef.current || initing || error) return;
    engineRef.current.setPattern(pattern);
  }, [pattern, initing, error]);

  function handleShaderControlChange(name, val) {
    setControls((prev) =>
      prev.map((ctrl) => (ctrl.name === name ? { ...ctrl, value: val } : ctrl))
    );
    engineRef.current?.update({ [name]: val });
  }

  const frameStyle = {
    border: '1px solid rgba(255, 255, 255, 0.05)',
    borderRadius: '4px',
    padding: '0.5rem',
    marginBottom: '0.5rem',
    backgroundColor: 'rgba(255, 255, 255, 0.05)'
  };

  const containerStyle = {
    width: 'min(100%, 800px)',
    margin: '0 auto',
    fontFamily: 'sans-serif'
  };

  return (
    <div style={containerStyle}>
      {engineRef.current && <Perf engine={engineRef.current} />}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {/* Shader Section */}
      <div style={frameStyle}>
        <DropdownControl
          label="shader"
          value={shader}
          options={shaderOptions}
          onChange={setShader}
          disabled={initing}
        />

        <DropdownControl
          label="pattern"
          value={pattern}
          options={patternOptions}
          onChange={setPattern}
          disabled={initing}
        />

        {controls.map((ctrl) => (
          <SliderControl
            key={ctrl.name}
            label={ctrl.name}
            min={ctrl.min}
            max={ctrl.max}
            step={ctrl.step}
            value={ctrl.value}
            onChange={(val) => handleShaderControlChange(ctrl.name, val)}
            disabled={initing}
          />
        ))}
      </div>

      <div style={frameStyle}>
        <canvas
          ref={canvasRef}
          width={Config.CANVAS_SIZE}
          height={Config.CANVAS_SIZE}
          style={{
            width: '100%',
            maxWidth: `${Config.CANVAS_SIZE}px`,
            display: 'block',
            margin: '0 auto',
            background: 'transparent'
          }}
        />
      </div>
    </div>
  );
}
