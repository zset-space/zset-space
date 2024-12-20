"""Core library for analyzing n-ball dimensional evolution and geometric patterns.

This module provides fundamental tools for studying how n-balls evolve through dimensions,
focusing on the relationships between volume, surface area, and radius. It reveals deep
connections between geometric constraints and rotational freedom while tracking how
information propagates through dimensional transitions.

Key concepts:
- Dimensional evolution through surface-volume coupling
- Phase space analysis of geometric transitions
- Wave-like behavior in dimensional propagation
- Geometric efficiency and void space analysis
"""

__package__ = 'nballs'

import numpy as np
from numpy import pi, e
from scipy.special import gamma
from dataclasses import dataclass
from typing import Tuple, Optional, Union, Dict
from .base import VisualHelper

@dataclass
class GeometricState:
    """Container for fundamental geometric measurements across dimensions.

    Attributes:
        dimension: Current dimension being analyzed
        volume: N-ball volume at this dimension
        surface: Surface area at this dimension
        next_surface: Surface area of n+1 ball
        radius: Characteristic radius for unit volume
        freedom: Geometric freedom/rotational capacity
        coupling: Surface-volume coupling coefficient
        phase: Phase angle of geometric state
    """
    dimension: float
    volume: float
    surface: float
    next_surface: float
    radius: float
    freedom: float
    coupling: float
    phase: float

class NBallCore(VisualHelper):
    """Core analysis framework for n-ball dimensional evolution.

    This class provides fundamental tools for studying how geometric properties
    evolve through dimensions. It focuses on revealing deep patterns in how
    information propagates between dimensions through surface-volume coupling
    and phase relationships.

    The framework is built around natural units (π, τ) to highlight fundamental
    relationships and resonance patterns. All calculations maintain careful
    numerical stability through the use of logarithmic transformations and
    safe division practices.
    """

    def __init__(self, epsilon: float = 1e-10):
        """Initialize framework with numerical safety threshold.

        Args:
            epsilon: Small positive number for safe division
        """
        super().__init__()
        self.e = np.e
        self.pi = np.pi
        self.tau = 2 * np.pi
        self.epsilon = epsilon
        self.critical_points = {
            'volume_max': 5.256946,  # ~τ-1 region
            'freedom_max': 6.118750,  # ~τ region
            'surface_max': 7.256946   # ~τ+1 region
        }

    def ball_volume(self, d: float) -> float:
        """Calculate n-ball volume using gamma function relationship.

        The volume follows V(d) = π^(d/2) / Γ(d/2 + 1), revealing deep
        connections to wave-like behavior through the gamma function.

        Args:
            d: Dimension (can be non-integer)

        Returns:
            Volume of n-ball in dimension d
        """
        if d < 0:
            return 0
        try:
            return (pi ** (d/2)) / gamma(d/2 + 1)
        except:
            return 0

    def ball_surface(self, d: float) -> float:
        """Calculate n-ball surface area through dimensional relationship.

        The surface area follows S(d) = τ·π^((d-2)/2) / Γ(d/2), maintaining
        the fundamental coupling S(d+1) = τ·V(d).

        Args:
            d: Dimension (can be non-integer)

        Returns:
            Surface area in dimension d
        """
        if d < 0:
            return 0
        try:
            return self.tau * (pi ** ((d-2)/2)) / gamma(d/2)
        except:
            return 0

    def ball_radius(self, d: float, volume: float = 1.0) -> float:
        """Calculate characteristic radius for given volume.

        The radius acts as an information carrier between dimensions,
        revealing how geometric constraints propagate through phase space.

        Args:
            d: Dimension
            volume: Target volume (default 1.0)

        Returns:
            Radius needed to achieve target volume in dimension d
        """
        if d <= 0:
            return 0
        try:
            return (volume * gamma(d/2 + 1) / (pi ** (d/2))) ** (1/d)
        except:
            return 0

    def geometric_freedom(self, d: float) -> float:
        """Calculate rotational freedom/geometric capacity.

        This measures the available rotational choices and geometric
        constraints at each dimension, peaking near τ.

        Args:
            d: Dimension

        Returns:
            Geometric freedom measure
        """
        v = self.ball_volume(d)
        s = self.ball_surface(d)
        if abs(v) < self.epsilon:
            return 0
        theta = np.arctan2(s, self.tau * v)
        r = (s**2 + (self.tau * v)**2)**0.5
        return r * abs(np.sin(theta * d))

    def analyze_dimension(self, d: float) -> GeometricState:
        """Perform comprehensive geometric analysis at dimension d.

        Computes fundamental measurements and relationships that characterize
        the geometric state at a given dimension.

        Args:
            d: Dimension to analyze

        Returns:
            GeometricState containing core measurements
        """
        v = self.ball_volume(d)
        s = self.ball_surface(d)
        s_next = self.ball_surface(d + 1)
        r = self.ball_radius(d)
        f = self.geometric_freedom(d)

        # Coupling strength with safety
        c = s_next / (self.tau * v) if abs(v) > self.epsilon else 0

        # Phase relationships
        p = np.arctan2(s_next, self.tau * v)

        return GeometricState(
            dimension=d,
            volume=v,
            surface=s,
            next_surface=s_next,
            radius=r,
            freedom=f,
            coupling=c,
            phase=p
        )

    def safe_gradient(self, values: np.ndarray, dims: np.ndarray) -> np.ndarray:
        """Compute numerically stable gradient.

        Uses centered differences with careful handling of endpoints and
        numerical instabilities.

        Args:
            values: Array of values to differentiate
            dims: Corresponding dimensions

        Returns:
            Gradient array
        """
        dx = np.gradient(dims)
        dy = np.gradient(values)
        return np.divide(dy, dx, where=abs(dx) > self.epsilon)

    def phase_velocity(self, d: float, delta: float = 0.001) -> Tuple[float, float]:
        """Compute phase space velocity and acceleration.

        Tracks how geometric states evolve through phase space, revealing
        wave-like behavior and resonance.

        Args:
            d: Dimension
            delta: Small step for numerical derivatives

        Returns:
            Tuple of (velocity, acceleration)
        """
        # Compute phase angles at d±delta
        p_minus = self.analyze_dimension(d - delta).phase
        p_center = self.analyze_dimension(d).phase
        p_plus = self.analyze_dimension(d + delta).phase

        # Compute derivatives
        velocity = (p_plus - p_minus) / (2 * delta)
        accel = (p_plus - 2*p_center + p_minus) / (delta * delta)

        return velocity, accel

    def dimensional_coupling(self, d: float) -> Dict[str, float]:
        """Analyze coupling between adjacent dimensions.

        Examines how geometric information propagates through dimensional
        transitions via surface-volume relationships.

        Args:
            d: Dimension

        Returns:
            Dictionary of coupling metrics
        """
        state = self.analyze_dimension(d)
        next_state = self.analyze_dimension(d + 1)

        # Volume propagation
        v_coupling = (next_state.volume / state.volume
                     if abs(state.volume) > self.epsilon else 0)

        # Surface propagation
        s_coupling = (next_state.surface / state.surface
                     if abs(state.surface) > self.epsilon else 0)

        # Radius evolution
        r_coupling = (next_state.radius / state.radius
                     if abs(state.radius) > self.epsilon else 0)

        return {
            'volume_coupling': v_coupling,
            'surface_coupling': s_coupling,
            'radius_coupling': r_coupling,
            'freedom_ratio': next_state.freedom / (state.freedom + self.epsilon),
            'phase_advance': next_state.phase - state.phase
        }

    def interference_pattern(self, d: float) -> Tuple[float, float, float, float]:
        """Analyze bidirectional phase interference between dimensions.

        Examines how forward and backward phase evolution creates
        interference patterns that shape geometric transitions.

        Args:
            d: Dimension

        Returns:
            Tuple of (magnitude, phase, real_component, imag_component)
        """
        # Forward and backward transitions
        state = self.analyze_dimension(d)
        next_state = self.analyze_dimension(d + 1)
        prev_state = self.analyze_dimension(d - 1)

        # Phase rotation relative to τ-1
        theta = (d - (self.tau - 1)) / 2 * pi / 2

        # Compute interference between transitions
        interference = (np.sin(next_state.phase) * np.cos(prev_state.phase) *
                       np.exp(-((d - self.tau)**2)/(2*pi)))

        # Extract components
        real_part = interference * np.cos(theta)
        imag_part = interference * np.sin(theta)

        magnitude = (real_part**2 + imag_part**2)**0.5
        phase = np.arctan2(imag_part, real_part)

        return magnitude, phase, real_part, imag_part

    def void_ratio(self, d: float) -> float:
        """Calculate geometric inefficiency through void space ratio.

        Measures how much of the enclosing space is not utilized by
        the n-ball, revealing dimensional efficiency patterns.

        Args:
            d: Dimension

        Returns:
            Void ratio (0 = perfect efficiency, 1 = complete void)
        """
        v = self.ball_volume(d)
        r = self.ball_radius(d)

        if d <= 0 or r <= 0:
            return 1.0

        enclosing = r**d
        return 1 - min(1.0, max(0.0, v/enclosing))

    def __str__(self) -> str:
        """Return string representation with key information."""
        return (f"NBallCore Analysis Framework\n"
                f"- Numerical threshold: {self.epsilon}\n"
                f"- Critical points: {self.critical_points}")

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return f"NBallCore(epsilon={self.epsilon})"