import React, { useEffect, useState, useRef, memo } from 'react';
import PropTypes from 'prop-types';

const FRAME_SAMPLE_SIZE = 30;
const UPDATE_INTERVAL = 500;
const DEFAULT_FPS = '0.00';
const MIN_DT = 0.001;
const FPS_THRESHOLD = {
  GOOD: 55,
  OKAY: 30
};

const Perf = memo(({ engine, enabled = true }) => {
  const [stats, setStats] = useState({ fps: DEFAULT_FPS, min: Infinity, max: 0 });
  const [gpuInfo, setGpuInfo] = useState('');
  const [error, setError] = useState(null);

  const frameTimes = useRef([]);
  const lastTimestamp = useRef(performance.now());
  const rafID = useRef(null);
  const updateInterval = useRef(null);

  useEffect(() => {
    if (!engine || !enabled) return;

    try {
      setGpuInfo(engine.getRendererInfo());
    } catch (err) {
      setError('GPU info unavailable');
      console.error('GPU Info Error:', err);
    }

    function loop(timestamp) {
      const dt = Math.max(timestamp - lastTimestamp.current, MIN_DT);
      lastTimestamp.current = timestamp;

      const instantaneous = 1000 / dt;
      frameTimes.current.push(instantaneous);

      if (frameTimes.current.length > FRAME_SAMPLE_SIZE) {
        frameTimes.current.shift();
      }

      rafID.current = requestAnimationFrame(loop);
    }

    function updateDisplay() {
      if (frameTimes.current.length === 0) return;
      const values = frameTimes.current;
      const avg = values.reduce((a, b) => a + b, 0) / values.length;
      const min = Math.min(...values);
      const max = Math.max(...values);

      setStats({
        fps: avg.toFixed(2),
        min: min.toFixed(2),
        max: max.toFixed(2)
      });
    }

    rafID.current = requestAnimationFrame(loop);
    updateInterval.current = setInterval(updateDisplay, UPDATE_INTERVAL);

    return () => {
      cancelAnimationFrame(rafID.current);
      clearInterval(updateInterval.current);
      frameTimes.current = [];
    };
  }, [engine, enabled]);

  if (!enabled) return null;
  if (error) return <div style={{ color: '#f44336' }}>{error}</div>;

  const fpsNum = parseFloat(stats.fps);
  const fpsColor = fpsNum >= FPS_THRESHOLD.GOOD ? '#4caf50'
                    : fpsNum >= FPS_THRESHOLD.OKAY ? '#ff9800'
                    : '#f44336';

  return (
    <div style={{
      fontFamily: 'monospace',
      fontSize: '12px',
      padding: '4px',
      background: 'rgba(0,0,0,0.1)',
      borderRadius: '4px',
      marginBottom: '1rem'
    }}>
      <div>gpu: {gpuInfo || 'unknown'}</div>
      <div style={{ color: fpsColor }}>
        fps: {stats.fps} (min: {stats.min}, max: {stats.max})
      </div>
    </div>
  );
});

Perf.propTypes = {
  engine: PropTypes.object.isRequired,
  enabled: PropTypes.bool
};

Perf.displayName = 'Perf';

export default Perf;
