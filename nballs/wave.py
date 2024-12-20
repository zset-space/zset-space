"""Wave Geometry Analysis Framework for N-Ball Evolution.

This module explores how dimensions evolve through wave-like behavior, examining
phase relationships, resonance patterns, and interference effects. It reveals
how geometric information propagates through dimensions via oscillatory patterns
that emerge from fundamental surface-volume coupling.

The framework maps geometric transitions to wave equations, treating dimensional
evolution as a form of quantum-like system with distinct phase states and
resonance conditions. This approach illuminates how rotational freedom emerges
from phase coherence between adjacent dimensions.
"""

__package__ = 'nballs'

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional
from .core import NBallCore, GeometricState

@dataclass
class WaveState:
    """Quantum-like state description of dimensional geometry.

    Attributes:
        dimension: Current dimension being analyzed
        psi_forward: Forward-propagating wave component
        psi_backward: Backward-propagating wave component
        energy: Total geometric energy
        coherence: Phase coherence measure
        resonance: Resonance strength with adjacent dimensions
        stability: State stability measure
    """
    dimension: float
    psi_forward: complex
    psi_backward: complex
    energy: float
    coherence: float
    resonance: float
    stability: float

class WaveGeometryAnalyzer(NBallCore):
    """Analyzer for wave-like behavior in dimensional evolution.

    This class extends NBallCore to explore how geometric information propagates
    through dimensions via wave-like patterns. It reveals deep connections between
    phase coherence, geometric stability, and rotational freedom.

    The framework maps dimensional transitions to quantum-like states, examining
    how phase relationships create resonance patterns that shape geometric
    evolution. This approach illuminates the emergence of stable geometric
    configurations through constructive interference between dimensions.
    """

    def __init__(self, epsilon: float = 1e-10):
        """Initialize wave geometry analyzer.

        Args:
            epsilon: Numerical safety threshold
        """
        super().__init__(epsilon)

        # Quantum energy levels at critical dimensions
        self.energy_levels = {
            'ground': self.critical_points['volume_max'],
            'excited': self.critical_points['freedom_max'],
            'transition': self.critical_points['surface_max']
        }

    def compute_wave_state(self, d: float) -> WaveState:
        """Compute quantum-like wave state with enhanced numerical stability.

        Modified to handle edge cases and improve phase tracking while maintaining
        the core wave-like behavior that emerges from geometric constraints.
        """
        # Get geometric state with safety bounds
        d = max(self.epsilon, d)
        geo = self.analyze_dimension(d)

        # Improved wave components with better numerical stability
        theta = d/(2*np.pi)
        decay = np.exp(-theta/4)  # Amplitude decay

        # Enhanced stability in freedom calculation
        freedom = max(geo.freedom, self.epsilon)

        # Forward and backward waves with phase preservation
        psi_f = decay * freedom * np.exp(1j*theta)
        psi_b = decay * freedom * np.exp(-1j*theta)

        # Safe energy normalization
        total_amp = np.abs(psi_f) + np.abs(psi_b)
        energy = np.abs(psi_f + psi_b)**2 / (1 + d)

        # Improved coherence calculation with safety
        coherence = (np.abs(psi_f + psi_b)/(total_amp + self.epsilon)
                    if total_amp > self.epsilon else 0)

        # Enhanced resonance calculation
        n = np.round(theta)  # Principal quantum number
        resonance = np.exp(-2*(theta - n)**2) * geo.coupling

        # Stability metric incorporating phase coherence
        phase_diff = np.abs(np.angle(psi_f) - np.angle(psi_b))
        stability = np.abs(np.sin(theta * np.pi/2) * coherence *
                         np.cos(phase_diff/2))

        return WaveState(
            dimension=d,
            psi_forward=psi_f,
            psi_backward=psi_b,
            energy=energy,
            coherence=coherence,
            resonance=resonance,
            stability=stability
        )

    def analyze_transitions(self, d: float) -> Dict[str, float]:
        """Analyze quantum transitions between adjacent dimensions.

        Examines how wave states evolve across dimensions, revealing
        patterns in phase coherence and energy transfer.

        Args:
            d: Central dimension for analysis

        Returns:
            Dictionary of transition metrics
        """
        # Get states for d-1, d, d+1
        states = [self.compute_wave_state(d + offset) for offset in [-1, 0, 1]]

        # Transition amplitudes
        t_down = np.abs(states[1].psi_backward * np.conj(states[0].psi_forward))
        t_up = np.abs(states[1].psi_forward * np.conj(states[2].psi_backward))

        # Energy transfer
        e_down = t_down * (states[1].energy - states[0].energy)
        e_up = t_up * (states[2].energy - states[1].energy)

        # Phase evolution
        phase_advance = np.angle(states[2].psi_forward) - np.angle(states[1].psi_forward)

        return {
            'transition_down': t_down,
            'transition_up': t_up,
            'energy_down': e_down,
            'energy_up': e_up,
            'phase_advance': phase_advance,
            'coherence': states[1].coherence,
            'stability': states[1].stability
        }

    def resonance_pattern(self, d: float) -> Tuple[complex, float, float]:
        """Analyze resonance pattern through phase space.

        Examines how wave states achieve coherence through phase
        relationships, revealing stable geometric configurations.

        Args:
            d: Dimension to analyze

        Returns:
            Tuple of (resonance_amplitude, coherence_strength, stability)
        """
        state = self.compute_wave_state(d)

        # Complex resonance amplitude
        theta = (d - (self.tau - 1)) / 2
        z = theta + 1j*state.coherence

        # Resonance wave with phase modulation
        psi = state.freedom * np.exp(1j*theta) * np.exp(-theta/4)

        # Resonance components
        amplitude = psi * np.exp(-((d - self.energy_levels['ground'])**2)/(2*self.tau))
        strength = np.abs(amplitude) * state.coherence
        stability = strength * state.stability

        return amplitude, strength, stability

    def analyze_interference(self, d1: float, d2: float,
                           points: int = 101) -> Dict[str, np.ndarray]:
        """Analyze interference pattern between dimensions.

        Studies how wave states interfere across dimensional range,
        revealing patterns in phase coherence and stability.

        Args:
            d1: Starting dimension
            d2: Ending dimension
            points: Number of sampling points

        Returns:
            Dictionary of interference metrics across dimension range
        """
        dims = np.linspace(d1, d2, points)

        # Collect wave states
        states = [self.compute_wave_state(d) for d in dims]

        # Extract key metrics
        coherence = np.array([s.coherence for s in states])
        energy = np.array([s.energy for s in states])
        stability = np.array([s.stability for s in states])

        # Phase evolution
        phase = np.array([np.angle(s.psi_forward) for s in states])
        phase_vel = np.gradient(phase, dims)

        # Interference strength
        interference = coherence * np.cos(phase) * stability

        return {
            'dimensions': dims,
            'coherence': coherence,
            'energy': energy,
            'stability': stability,
            'phase': phase,
            'phase_velocity': phase_vel,
            'interference': interference
        }

    def find_stable_states(self, d_range: Tuple[float, float],
                          threshold: float = 0.8) -> List[float]:
        """Find stable geometric configurations through wave analysis.

        Identifies dimensions with high coherence and stability,
        revealing preferred geometric configurations.

        Args:
            d_range: (min_dimension, max_dimension) to search
            threshold: Minimum stability for state selection

        Returns:
            List of dimensions with stable configurations
        """
        # Sample dimensions
        dims = np.linspace(*d_range, 1001)
        stable_dims = []

        for d in dims:
            state = self.compute_wave_state(d)

            # Check stability criteria
            if (state.stability > threshold and
                state.coherence > threshold and
                state.resonance > threshold):
                stable_dims.append(d)

        return stable_dims

    def __str__(self) -> str:
        """Return string representation with key information."""
        return (f"Wave Geometry Analyzer\n"
                f"Core framework: {super().__str__()}\n"
                f"Energy levels: {self.energy_levels}")

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return f"WaveGeometryAnalyzer(epsilon={self.epsilon})"

if __name__ == '__main__':
    """Create enhanced multi-perspective visualization of wave geometry patterns."""
    # Create analyzer and visualization helper
    analyzer = WaveGeometryAnalyzer()

    # High resolution sampling
    n_points = 401
    dims = np.linspace(0, 4*np.pi, n_points)
    phases = np.linspace(0, 2*np.pi, n_points)

    # Create dimension-phase meshgrid
    D, P = np.meshgrid(dims, phases)

    # Compute wave states
    states = [analyzer.compute_wave_state(d) for d in dims]

    # Extract wave components
    wave_components = {
        'forward_amp': np.array([abs(s.psi_forward) for s in states]),
        'backward_amp': np.array([abs(s.psi_backward) for s in states]),
        'phase_diff': np.array([np.angle(s.psi_forward) - np.angle(s.psi_backward)
                               for s in states]),
        'coherence': np.array([s.coherence for s in states])
    }

    # Prepare visualization data
    vis_data = analyzer.prepare_wave_data(dims, phases, wave_components)

    # Create main figure
    fig = plt.figure(figsize=(20, 20))

    # Create each subplot with enhanced visualization
    for idx, view in enumerate(analyzer.standard_views, 1):
        ax = analyzer.setup_wave_plot(
            fig, idx, view, D,
            vis_data['forward'], vis_data['backward'],
            plt.cm.coolwarm(vis_data['color_metric'])
        )

    # Add coherence subplot
    # analyzer.add_coherence_subplot(fig, dims, wave_components['coherence'])

    # Add comprehensive title
    fig.suptitle('Wave Geometry Analysis\nDimensional Evolution in π Units', fontsize=16, y=0.95)

    # Final layout adjustments
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save enhanced visualization
    now = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')
    name = f'nballs-{now}-{analyzer.__class__.__qualname__}.png'
    plt.savefig(name, dpi=300, bbox_inches='tight')
    plt.close()
