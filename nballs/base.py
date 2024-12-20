"""Visualization utilities for n-ball dimensional analysis.

This module provides core visualization tools for analyzing dimensional evolution,
focusing on wave mechanics, phase relationships, and geometric transitions. It
handles common operations like signal enhancement, view management, and dimensional
markers.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict

@dataclass
class VisualConfig:
    """Configuration for 3D view perspectives."""
    elev: float
    azim: float
    title: str
    dimension_axis: str = 'z'  # Which axis represents dimension

class VisualHelper:
    """Core visualization utilities for dimensional analysis."""

    def __init__(self):
        self.standard_views = [
            VisualConfig(-90, 0, 'Base View (Phase Space)'),
            VisualConfig(0, 0, 'Side View (Wave Propagation)'),
            VisualConfig(0, -45, 'Dual View (Phase Evolution)'),
            VisualConfig(35.264, -45, 'Ortho View (Wave Structure)'),
        ]

    def enhance_signal(self, x: np.ndarray, sharpness: float = 1.5,
                      normalize: bool = True) -> np.ndarray:
        """Enhance signal visibility while preserving structure.

        Uses tanh transformation to sharpen transitions while maintaining
        continuity and preventing saturation.
        """
        if normalize:
            x = (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x) + self.epsilon)
        return np.tanh(sharpness * x) / np.tanh(sharpness)

    def create_dimension_markers(self, ax: plt.Axes, scale: float = 1.0,
                               color: str = 'red', alpha: float = 0.5):
        """Add dimensional transition markers at critical points."""
        for name, value in self.critical_points.items():
            value_pi = value / np.pi
            # Add marker line
            ax.plot([value_pi, value_pi], [-scale, scale], [0],
                   color=color, alpha=alpha, linestyle='--')
            # Add label
            ax.text(value_pi, scale, 0, f'{name}\n(τ{value_pi-2:.2f}π)',
                   color=color, alpha=alpha, ha='center', va='bottom')

    def setup_wave_plot(self, fig: plt.Figure, idx: int, view: VisualConfig,
                       D: np.ndarray, forward: np.ndarray, backward: np.ndarray,
                       colors: np.ndarray,
                       label='Wave') -> plt.Axes:
        """Configure a single wave visualization subplot."""
        ax = fig.add_subplot(2, 2, idx, projection='3d', proj_type='ortho')

        # Handle different dimension axis configurations
        x, y, z = forward, backward, D/np.pi
        xlim, xlabel = (-1, 1), f'Forward {label} (π units)'
        ylim, ylabel = (-1, 1), f'Backward {label} (π units)'
        zlim, zlabel = (0, 4), f'Dimensional {label} (π units)'
        match view.dimension_axis:
            case 'x':
                x, y, z = D/np.pi, forward, backward
                xlabel, zlabel = zlabel, xlabel
                xlim, zlim = zlim, xlim
            case 'y':
                x, y, z = forward, D/np.pi, backward
                ylabel, zlabel = zlabel, ylabel
                ylim, zlim = zlim, ylim
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_zlim(*zlim)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        ax.set_box_aspect([1, 1, 1])
        ax.plot_surface(x, y, z, facecolors=colors, alpha=0.9)
        ax.view_init(elev=view.elev, azim=view.azim)
        ax.set_title(f'Geometric {label}: {view.title}')

        # Add dimension markers for non-3D views
        if view.dimension_axis != 'z':
            self.create_dimension_markers(ax)

        return ax

    def add_coherence_subplot(self, fig: plt.Figure, dims: np.ndarray,
                            coherence: np.ndarray):
        """Add small coherence reference subplot."""
        # Create inset axes for coherence plot
        ax_coh = fig.add_axes([0.15, 0.02, 0.3, 0.1])
        ax_coh.plot(dims/np.pi, coherence, 'k-', alpha=0.7)
        ax_coh.set_xlabel('Dimension (π units)')
        ax_coh.set_ylabel('Coherence')
        ax_coh.grid(True, alpha=0.3)

        # Add critical point markers
        for name, value in self.critical_points.items():
            ax_coh.axvline(value/np.pi, color='red', alpha=0.3, linestyle='--')

    def prepare_wave_data(self, dims: np.ndarray, phases: np.ndarray,
                         wave_components: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Prepare wave data for visualization with consistent normalization."""
        forward = np.outer(wave_components['forward_amp'], np.cos(phases))
        backward = np.outer(wave_components['backward_amp'], np.sin(phases))

        # Enhance signals
        forward = 2 * self.enhance_signal(forward) - 1
        backward = 2 * self.enhance_signal(backward) - 1

        # Create color metric from coherence and phase
        color_metric = (self.enhance_signal(wave_components['coherence'])[:, np.newaxis] *
                       np.abs(np.cos(wave_components['phase_diff']))[:, np.newaxis])
        color_metric = np.tile(color_metric, (1, len(phases)))

        return {
            'forward': forward,
            'backward': backward,
            'color_metric': color_metric
        }
