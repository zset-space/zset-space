"""Dimensional Coupling Analysis for N-Ball Evolution.

This module explores how geometric information propagates between dimensions
through fundamental relationships between volume, surface area, and radius.
It reveals deep patterns in how dimensional transitions occur and how
geometric properties emerge from phase space evolution.

The framework maps geometric coupling across dimensions, showing how radius
acts as an information carrier while surface-volume relationships create
resonance patterns near critical points like τ±1.
"""

__package__ = 'nballs'

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
from .core import NBallCore, GeometricState

@dataclass
class CouplingState:
    """Description of geometric coupling between dimensions.

    Attributes:
        dimension: Current dimension being analyzed
        forward_coupling: Surface to next volume relationship
        backward_coupling: Surface from previous volume
        radius_transfer: Information transfer through radius
        phase_advance: Phase evolution between dimensions
        resonance: Coupling strength near critical points
        coherence: Phase space correlation measure
    """
    dimension: float
    forward_coupling: float
    backward_coupling: float
    radius_transfer: float
    phase_advance: float
    resonance: float
    coherence: float

class DimensionalCouplingAnalyzer(NBallCore):
    """Analyzer for geometric coupling between dimensions.

    This class extends NBallCore to study how geometric information propagates
    through dimensional transitions. It reveals deep patterns in how radius
    growth mediates surface-volume coupling and creates resonance near
    critical dimensions.
    """

    def __init__(self, epsilon: float = 1e-10):
        """Initialize dimensional coupling analyzer."""
        super().__init__(epsilon)

    def compute_coupling_state(self, d: float) -> CouplingState:
        """Compute coupling configuration at dimension d."""
        # Get geometric states with safety bounds
        d = max(self.epsilon, d)  # Prevent negative dimensions
        prev_state = self.analyze_dimension(d - 1)
        curr_state = self.analyze_dimension(d)
        next_state = self.analyze_dimension(d + 1)

        # Forward coupling (d → d+1) with safety
        f_coupling = (next_state.volume / (curr_state.surface + self.epsilon))

        # Backward coupling (d-1 → d) with safety
        b_coupling = (curr_state.volume / (prev_state.surface + self.epsilon))

        # Radius information transfer with log safety
        r_transfer = np.log1p(next_state.radius/(curr_state.radius + self.epsilon))

        # Phase evolution
        phase_diff = next_state.phase - curr_state.phase

        # Resonance near critical points scaled by π
        nearest = min(self.critical_points.values(),
                     key=lambda x: abs(x/np.pi - d))
        resonance = np.exp(-((d*np.pi - nearest)**2)/(2*self.tau))

        # Phase space coherence
        coherence = np.cos(curr_state.phase - prev_state.phase)

        return CouplingState(
            dimension=d,
            forward_coupling=f_coupling,
            backward_coupling=b_coupling,
            radius_transfer=r_transfer,
            phase_advance=phase_diff,
            resonance=resonance,
            coherence=coherence
        )

    def coupling_flow(self, d1: float, d2: float, points: int = 401) -> Dict[str, np.ndarray]:
        """Analyze coupling flow between dimensions with π-normalized phases."""
        dims = np.linspace(d1, d2, points)

        # Collect coupling states
        states = [self.compute_coupling_state(d) for d in dims]

        # Extract and normalize components in π units
        f_coupling = np.array([s.forward_coupling for s in states])
        b_coupling = np.array([s.backward_coupling for s in states])
        r_transfer = np.array([s.radius_transfer for s in states])
        phase = np.array([s.phase_advance for s in states])
        coherence = np.array([s.coherence for s in states])
        resonance = np.array([s.resonance for s in states])

        # Normalize to ±π range
        f_norm = np.clip(f_coupling/np.pi, -1, 1)  # Now in π units
        b_norm = np.clip(b_coupling/np.pi, -1, 1)  # Now in π units

        # Combined flow strength preserves π scaling
        flow = np.sqrt(f_norm**2 + b_norm**2) * coherence

        return {
            'dimensions': dims,
            'forward_coupling': f_norm,
            'backward_coupling': b_norm,
            'radius_transfer': r_transfer,
            'phase': phase,
            'coherence': coherence,
            'flow': flow,
            'resonance': resonance
        }

if __name__ == '__main__':
    """Create multi-perspective visualization of dimensional coupling flow."""
    # Create analyzer
    analyzer = DimensionalCouplingAnalyzer()

    # High resolution sampling
    n_points = 401
    dims = np.linspace(0, 4*np.pi, n_points)
    phases = np.linspace(0, 2*np.pi, n_points)

    # Compute coupling with π normalization
    flow = analyzer.coupling_flow(0, 4, points=n_points)

    # Create meshgrid
    D, P = np.meshgrid(dims, phases)

    # Extract π-normalized components
    forward = np.abs(flow['forward_coupling'])
    backward = np.abs(flow['backward_coupling'])
    resonance = (flow['resonance'] - flow['resonance'].min()) / \
                (flow['resonance'].max() - flow['resonance'].min())

    # Create phase space structure
    forward = np.outer(forward, np.cos(phases)).reshape(n_points, n_points)
    backward = np.outer(backward, np.sin(phases)).reshape(n_points, n_points)
    resonance = np.tile(resonance, (n_points, 1))

    # Create figure with 2x2 grid
    fig = plt.figure(figsize=(20, 20))

    # Create subplots
    norm = plt.Normalize(-1, 1)
    for idx, view in enumerate(analyzer.standard_views, 1):
        ax = analyzer.setup_wave_plot(
            fig, idx, view, D,
            forward, backward,
            plt.cm.RdYlBu_r(norm(2*resonance - 1)),
            label='Coupling Flow',
        )

    # Add main title
    fig.suptitle('Dimensional Coupling Flow Analysis\nPhase Space in π Units', fontsize=16, y=0.95)

    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save or show
    now = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')
    name = f'nballs-{now}-{analyzer.__class__.__qualname__}.png'
    plt.savefig(name, dpi=300, bbox_inches='tight')
    plt.close()
