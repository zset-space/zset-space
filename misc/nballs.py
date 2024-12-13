"""N-Ball Geometry Analysis Suite

A library for exploring dimensional evolution and rotation through geometric and phase relationships.
Focuses on surface-volume coupling, phase transitions, and rotational freedom across dimensions.

Core Relationships:
   S(d+1) = τ·V(d) # Surface-volume coupling
   V(d) = π^(d/2) / Γ(d/2 + 1) # N-ball volume
   S(d) = τ·π^((d-2)/2) / Γ(d/2) # N-ball surface area

The sphere appears to rotate between real and imaginary domains with precise phase evolution,
potentially producing interference patterns through partial domain occlusion.

Critical Points:
   Volume maximum: ≈ 5.256946 (near τ-1)
   Surface maximum: ≈ 7.256946 (near τ+1)

Usage Example:
   class ExperimentAnalyzer(NBallAnalyzer):

       def main(self):
           # Run analysis suite and print results!
           for d, label in self.dimensions(start=1, count=8, split=4).items():
               analysis = self.analyze_dimension(d)
               magnitude, phase, real, imag = self.interference_pattern(d)
               for d, label in self.dimensions().items():
                   # Run analysis suite and print results!
                   pass

   if __name__ == "__main__":
       analyzer = ExperimentAnalyzer()
       analyzer.main()

Core Methods:
   dimensions(start=1, count=8, split=4, special=True):
       Returns dictionary of dimensions with labels, including special points.
       Controls range, resolution and inclusion of critical values.

   ball_volume(d): Calculate n-ball volume
   ball_surface(d): Calculate n-ball surface area

   analyze_dimension(d):
       Returns comprehensive analysis including:
       - Volume and surface area
       - Coupling ratio and geometric freedom
       - Phase relationships

   phase_volume(d, alpha=1.0): Complex phase space volume
   interference_pattern(d): Phase interference analysis
   rotational_freedom(d): Effective rotational freedom
   transition_coupling(d): Coupling strength between dimensions
   phase_rate(d1, d2, points=1001): Phase evolution rate analysis

   find_critical_points(): Identify maxima, minima, inflections
   analyze_complex(d): Complex phase space analysis

Implementation Guidelines:
1. Use dimensions() to ensure consistent sampling of dimension space
2. Maintain continuous transitions - discontinuities indicate errors
3. Never hardcode sphere calculations - use provided methods
4. Verify patterns in both success and failure cases
5. Focus on mathematical relationships over code structure
6. Examine phase transitions and interference patterns carefully
7. Build on existing functionality through subclassing

The library emphasizes discovering fundamental patterns in dimensional evolution
through rapid mathematical exploration. Core volume/surface calculations are
well-verified; complex phase methods may require additional validation.
"""

import numpy as np
from math import e, pi, tau, factorial
from scipy.special import gamma
import matplotlib.pyplot as plt
import matplotlib.pyplot
matplotlib.use('Agg')

class NBallAnalyzer:

    def __init__(self):
        self.EPSILON = 1e-10

    def dimensions(self, start=1, count=8, split=4, special=True):
        # Define the dimensions
        dimensions = {k/split: str(k/split) for k in range(start, (split*(start+count))+1)}
        if special:
            for d, label in (
                (1.324718, 'plastic'),
                (1.618034, 'golden'),
                (e, 'e'),
                (pi, 'pi'),
                (5.256946, 'V-max'),
                (tau - 1, 'tau-1'),
                (tau, 'tau'),
                (7.256946, 'SA-max'),
                (tau + 1, 'tau+1')
            ):
                if start <= d <= start + count:
                    dimensions[d] = label
        return {k: dimensions[k] for k in sorted(dimensions)}

    def ball_volume(self, d):
        if d < 0:
            return 0
        try:
            return (pi ** (d / 2)) / gamma(d / 2 + 1)
        except:
            return 0

    def ball_surface(self, d):
        if d < 0:
            return 0
        try:
            return tau * (pi ** ((d - 2) / 2)) / gamma(d / 2)
        except:
            return 0

    def ball_radius(self, d, volume=1):
        if d <= 0:
            return 0
        try:
            return (volume * gamma(d / 2 + 1) / (pi ** (d / 2))) ** (1 / d)
        except:
            return 0

    def coupling_ratio(self, d):
        v_d = self.ball_volume(d)
        s_d1 = self.ball_surface(d + 1)
        if abs(v_d) < 1e-15:
            return 0
        return s_d1 / (tau * v_d)

    def geometric_freedom(self, d):
        v = self.ball_volume(d)
        s = self.ball_surface(d)
        if abs(v) < 1e-15:
            return 0
        theta = np.arctan2(s, tau * v)
        r = (s ** 2 + (tau * v) ** 2) ** 0.5
        return r * abs(np.sin(theta * d))

    def analyze_dimension(self, d):
        v_d = self.ball_volume(d)
        s_d = self.ball_surface(d)
        s_d1 = self.ball_surface(d + 1)
        freedom = self.geometric_freedom(d)

        result = {
            'dimension': d,
            'volume': v_d,
            'surface': s_d,
            'next_surface': s_d1,
            'coupling_ratio': self.coupling_ratio(d),
            'geometric_freedom': freedom,
            'phase': np.arctan2(s_d1, tau * v_d),
            'sv_ratio': s_d / v_d if abs(v_d) > 1e-15 else 0
        }
        return result

    def scan_range(self, start=0, end=15, points=1001):
        dims = np.linspace(start, end, points)
        data = np.zeros((points, 7))

        for i, d in enumerate(dims):
            result = self.analyze_dimension(d)
            data[i] = [
                d,
                result['volume'],
                result['surface'],
                result['next_surface'],
                result['coupling_ratio'],
                result['geometric_freedom'],
                result['phase']
            ]

        return {
            'dimensions': data[:, 0],
            'volumes': data[:, 1],
            'surfaces': data[:, 2],
            'next_surfaces': data[:, 3],
            'coupling_ratios': data[:, 4],
            'freedom': data[:, 5],
            'phases': data[:, 6]
        }

    def find_critical_points(self, start=0, end=15, points=1001):
        scan = self.scan_range(start, end, points)
        dims = scan['dimensions']
        dx = dims[1] - dims[0]

        metrics = {
            'volume': scan['volumes'],
            'surface': scan['surfaces'],
            'freedom': scan['freedom'],
            'coupling': scan['coupling_ratios']
        }

        critical = {}

        for name, values in metrics.items():
            maxima = []
            minima = []
            inflections = []

            d1 = np.gradient(values, dx)
            d2 = np.gradient(d1, dx)

            for i in range(1, len(values) - 1):
                if d1[i - 1] > 0 and d1[i + 1] < 0:
                    maxima.append(dims[i])
                elif d1[i - 1] < 0 and d1[i + 1] > 0:
                    minima.append(dims[i])
                if d2[i - 1] * d2[i + 1] < 0:
                    inflections.append(dims[i])

            critical[name] = {
                'maxima': maxima,
                'minima': minima,
                'inflections': inflections
            }

        return critical

    def interference_pattern(self, d):
        """Track bidirectional phase interference between adjacent dimensions"""
        # Forward volume-to-surface transition
        v_d = self.ball_volume(d)
        s_d1 = self.ball_surface(d + 1)
        forward_phase = np.angle(complex(s_d1, tau * v_d))

        # Backward surface-to-volume transition
        s_d = self.ball_surface(d)
        v_d1 = self.ball_volume(d - 1)
        backward_phase = np.angle(complex(tau * v_d1, s_d))

        # Phase rotation relative to τ-1
        theta = (d - (tau - 1)) / 2 * pi / 2

        # Compute interference between transitions with damping
        interference = np.sin(forward_phase) * np.cos(backward_phase) * np.exp(-((d - tau)**2)/(2*pi))

        # Extract real and imaginary components
        real_component = interference * np.cos(theta)
        imag_component = interference * np.sin(theta)

        # Calculate total geometric freedom
        magnitude = (real_component**2 + imag_component**2)**0.5
        phase = np.angle(complex(real_component, imag_component))

        return magnitude, phase, real_component, imag_component

    def phase_volume(self, d, alpha=1.0):
        """Volume with complex phase rotation"""
        theta = (d - (tau - 1)) / 2 * pi / 2
        z = alpha * (np.cos(theta) + 1j * np.sin(theta))

        try:
            v_base = (pi ** (d / 2)) / gamma(d / 2 + 1)
            v_phase = np.cosh(z.real) + 1j * np.sinh(z.imag)
            return v_base * v_phase
        except:
            return 0

    def rotational_freedom(self, d):
        """Calculate effective rotational freedom at dimension d"""
        v = self.phase_volume(d)
        # For complex d, use phase_volume for surface too
        s = self.phase_volume(d) if isinstance(d, complex) else self.ball_surface(d)

        theta = np.angle(complex(s, tau * abs(v)))
        # Use real part of d for interference calculation
        d_real = d.real if isinstance(d, complex) else d
        interference = np.sin(theta * d_real) * np.cos(pi * d_real / tau)

        r = (abs(v) ** 2 + (abs(s) / tau) ** 2) ** 0.5
        return r * abs(interference)

    def transition_coupling(self, d):
        """Measure coupling strength between adjacent dimensions"""
        v_d = self.phase_volume(d)
        # Handle complex d+1 for surface
        next_d = d + 1
        s_d1 = self.phase_volume(next_d) if isinstance(d, complex) else self.ball_surface(next_d)

        if abs(v_d) < 1e-15:
            return 0

        phase_diff = np.angle(complex(abs(s_d1), tau * abs(v_d)))
        coupling = abs(s_d1) / (tau * abs(v_d))
        return coupling * np.exp(-((phase_diff - pi / 2) ** 2) / (2 * pi))

    def phase_velocity(self, d, delta=0.001):
        """Compute phase velocity and acceleration at dimension d"""
        # Get phases at d±delta
        v_minus = self.ball_volume(d - delta)
        v_center = self.ball_volume(d)
        v_plus = self.ball_volume(d + delta)

        # Phase angles
        theta_minus = np.angle(complex(v_minus, self.ball_surface(d - delta)))
        theta_center = np.angle(complex(v_center, self.ball_surface(d)))
        theta_plus = np.angle(complex(v_plus, self.ball_surface(d + delta)))

        # Compute velocity and acceleration
        velocity = (theta_plus - theta_minus) / (2 * delta)
        accel = (theta_plus - 2*theta_center + theta_minus) / (delta * delta)

        return velocity, accel

    def analyze_complex(self, d):
        """Analyze sphere properties in complex phase space"""
        v = self.phase_volume(d)
        s = self.phase_volume(d) if isinstance(d, complex) else self.ball_surface(d)
        freedom = self.rotational_freedom(d)
        coupling = self.transition_coupling(d)

        return {
            'dimension': d,
            'volume': abs(v),
            'volume_phase': np.angle(v),
            'surface': abs(s),
            'rotational_freedom': freedom,
            'coupling': coupling
        }

    def phase_rate(self, d1, d2, points=1001):
        """
        Measure the phase evolution rate between two dimensions.
        """
        if d2 <= d1:
            raise ValueError("d2 must be greater than d1")

        dims = np.linspace(d1, d2, points)
        phases = []

        for d in dims:
            _, _, real, imag = self.interference_pattern(d)
            theta = np.arctan2(imag, real) if abs(real) > 1e-10 or abs(imag) > 1e-10 else 0
            phases.append(theta)

        # Convert to numpy arrays
        dims = np.array(dims)
        phases = np.array(phases)

        # Calculate rate through linear regression
        A = np.vstack([dims, np.ones(len(dims))]).T
        rate, _ = np.linalg.lstsq(A, phases, rcond=None)[0]

        # Calculate R² value
        phases_pred = rate * dims + _
        ss_res = np.sum((phases - phases_pred) ** 2)
        ss_tot = np.sum((phases - np.mean(phases)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        return rate, r_squared, phases, dims

    def analyze_transition(self, d):
        """Analyze dimensional transition with robust zero handling"""
        mag, phase, real, imag = self.interference_pattern(d)
        v_d = self.ball_volume(d)
        s_d = self.ball_surface(d)
        s_d1 = self.ball_surface(d + 1)

        # Safe division
        forward_ratio = s_d1/(tau * v_d) if abs(v_d) > 1e-15 else 0
        backward_ratio = s_d/(tau * self.ball_volume(d-1)) if d > 0 and abs(self.ball_volume(d-1)) > 1e-15 else 0

        # Safe gamma ratio calculation
        try:
            g_ratio = gamma(d/2 + 1)/gamma(d/2) if d != 0 else 0
        except:
            g_ratio = 0

        return {
            'dimension': d,
            'phase': phase,
            'forward_ratio': forward_ratio,
            'backward_ratio': backward_ratio,
            'gamma_ratio': g_ratio,
            'freedom': self.geometric_freedom(d)
        }

    def find_maxima(self):
        """Find precise maxima with safe bounds"""
        v_max = self.find_maximum(self.ball_volume, 5.25, 5.27)
        s_max = self.find_maximum(self.ball_surface, 7.25, 7.27)
        f_max = self.find_maximum(self.geometric_freedom, 6.11, 6.13)

        return {
            'volume': v_max,
            'surface': s_max,
            'freedom': f_max
        }

    def find_maximum(self, func, start, end, points=1001):
        """Find maximum with safe bounds and error checking"""
        dims = np.linspace(start, end, points)
        values = [func(d) for d in dims]
        max_idx = np.argmax(values)
        return {
            'dimension': dims[max_idx],
            'value': values[max_idx]
        }

    def analyze_quantum_state(self, d, epsilon=1e-10):
        """Analyze quantum properties at dimension d with smooth phase transition"""
        mag, phase, real, imag = self.interference_pattern(d)
        freedom = self.geometric_freedom(d)

        # π-step quantization
        pi_step = round(d/pi) * pi
        quantum_locked = abs(d - pi_step) < epsilon

        # Smooth phase transition between regimes
        if d < -epsilon:
            # Pure quantum regime - linear π accumulation
            accumulated_phase = d/pi
        elif d < epsilon:
            # Transition region - smooth interpolation
            quantum_phase = d/pi
            classical_phase = -1.321  # Known phase at d=0
            weight = (d + epsilon)/(2*epsilon)
            accumulated_phase = quantum_phase * (1-weight) + classical_phase * weight
        else:
            # Classical regime - tau-based rotation
            theta = (d - (tau-1)) / 2 * pi/2
            accumulated_phase = theta/pi

        # Stability with smooth transition
        if d < -epsilon:
            stability = 1.0 if quantum_locked else np.exp(-(d - pi_step)**2)
        elif d < epsilon:
            # Smooth stability transition
            weight = (d + epsilon)/(2*epsilon)
            stability = (1-weight) if quantum_locked else weight * freedom
        else:
            stability = freedom * np.exp(-((d - (tau-1))**2)/(2*tau))

        # Winding and charge with continuous evolution
        winding = accumulated_phase/2  # Normalize to full rotations
        charge = np.exp(2j * pi * winding)

        return {
            'dimension': d,
            'quantum_locked': quantum_locked,
            'phase': accumulated_phase,
            'stability': stability,
            'freedom': freedom,
            'winding': winding,
            'charge': charge,
            'magnitude': mag,
            'pi_step': pi_step/pi
        }

    def find_transitions(self, d_start, d_end, points=1001, epsilon=1e-10):
        """Find quantum transitions with smooth detection"""
        dims = np.linspace(d_start, d_end, points)
        transitions = []
        last_state = None

        for d in dims:
            state = self.analyze_quantum_state(d, epsilon)

            if last_state is not None:
                # Quantum transitions with hysteresis
                if state['quantum_locked'] != last_state['quantum_locked']:
                    transitions.append({
                        'dimension': d,
                        'type': 'quantum',
                        'from_phase': last_state['phase'],
                        'to_phase': state['phase'],
                        'pi_step': state['pi_step']
                    })

                # Smooth stability transitions
                stability_change = abs(state['stability'] - last_state['stability'])
                if stability_change > 0.5:
                    transitions.append({
                        'dimension': d,
                        'type': 'stability',
                        'from_value': last_state['stability'],
                        'to_value': state['stability']
                    })

                # Freedom peaks with continuity check
                if (state['freedom'] > last_state['freedom'] and
                    state['freedom'] > self.geometric_freedom(d + dims[1] - dims[0])):
                    transitions.append({
                        'dimension': d,
                        'type': 'freedom',
                        'value': state['freedom']
                    })

            last_state = state

        return transitions

    def compute_invariants(self, d, epsilon=1e-10):
        """Compute geometric invariants with transition handling"""
        state = self.analyze_quantum_state(d, epsilon)

        return {
            'dimension': d,
            'pf_product': state['phase'] * state['freedom'],
            'sw_product': state['stability'] * abs(state['winding']),
            'charge': state['charge'],
            'pi_step': state['pi_step']
        }

    def compute_resonance_state(self, d):
        """Compute quantum resonance state at dimension d"""
        try:
            # Basic components
            mag, phase, real, imag = self.interference_pattern(d)
            freedom = self.geometric_freedom(d)

            # Complex dimension analysis
            z = complex(d, 0)
            complex_volume = self.compute_complex_volume(z)

            # Phase state
            theta = (d - (tau-1)) / 2 * pi/2
            state = np.exp(1j * theta)

            # Resonance components
            resonance = self.compute_resonance(d)
            tunneling = self.compute_tunneling(d)
            entanglement = self.compute_entanglement(d)

            return {
                'dimension': d,
                'state': state,
                'resonance': resonance,
                'tunneling': tunneling,
                'entanglement': entanglement,
                'complex_volume': complex_volume,
                'freedom': freedom,
                'valid': True
            }
        except Exception as e:
            return {'valid': False, 'error': str(e)}

    def compute_complex_volume(self, z):
        """Compute n-ball volume for complex dimension z"""
        try:
            return pi**(z/2) / complex_gamma(z/2 + 1)
        except:
            return 0

    def compute_resonance(self, d):
        """Compute dimensional resonance pattern"""
        # Base resonance from π/2 rotation
        theta = (d - (tau-1)) / 2
        base = np.sin(theta * pi/2)

        # Quantum correction term
        quantum = np.exp(-((d - int(d))**2)/(2*self.EPSILON))

        # Combined resonance with phase
        return base * quantum * np.exp(1j * theta)

    def compute_tunneling(self, d):
        """Compute tunneling probability between dimensions"""
        # Barrier height varies with dimensional gap
        barrier = abs(d - round(d))

        # Tunneling probability
        if barrier < self.EPSILON:
            return 1.0
        return np.exp(-barrier * pi)

    def compute_entanglement(self, d):
        """Compute geometric entanglement between adjacent dimensions"""
        d1 = int(d)
        d2 = d1 + 1

        # Relative phase between dimensions
        phase1 = self.geometric_freedom(d1) * np.exp(1j * d1 * pi/2)
        phase2 = self.geometric_freedom(d2) * np.exp(1j * d2 * pi/2)

        # Entanglement measure
        return abs(phase1 * np.conj(phase2))

    def analyze_fractional_dimensions(self, start=0, end=10, points=2001):
        """Analyze behavior in fractional dimensions"""
        dims = np.linspace(start, end, points)
        states = []

        for d in dims:
            state = self.compute_resonance_state(d)
            if state['valid']:
                states.append(state)

        return dims[:len(states)], states

    def find_stable_fractionals(self, tolerance=1e-3):
        """Find potentially stable fractional dimensions"""
        dims, states = self.analyze_fractional_dimensions()
        stable = []

        for d, state in zip(dims, states):
            # Check stability conditions
            resonance_mag = abs(state['resonance'])
            tunneling = state['tunneling']
            entanglement = state['entanglement']

            # Stability criteria
            if (resonance_mag > 0.9 and  # Strong resonance
                tunneling < 0.1 and      # Low tunneling
                entanglement > 0.5):     # Significant entanglement
                stable.append((d, state))

        return stable

    def figure(self):
        dims, states = self.analyze_fractional_dimensions()

        # Extract components
        resonances = [s['resonance'] for s in states]
        tunnelings = [s['tunneling'] for s in states]
        entanglements = [s['entanglement'] for s in states]
        complex_vols = [s['complex_volume'] for s in states]

        fig = plt.figure(figsize=(15, 12))

        # Resonance pattern
        ax1 = plt.subplot(2, 2, 1)
        ax1.plot(dims, [abs(r) for r in resonances], 'b-',
                label='Resonance', alpha=0.7)
        ax1.plot(dims, tunnelings, 'r--',
                label='Tunneling', alpha=0.7)
        ax1.set_title('Quantum Resonance Pattern')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Complex volume evolution
        ax2 = plt.subplot(2, 2, 2)
        ax2.plot(dims, [abs(v) for v in complex_vols], 'g-', alpha=0.7)
        ax2.set_title('Complex Volume Evolution')
        ax2.grid(True, alpha=0.3)

        # Entanglement strength
        ax3 = plt.subplot(2, 2, 3)
        ax3.plot(dims, entanglements, 'b-', alpha=0.7)
        ax3.set_title('Dimensional Entanglement')
        ax3.grid(True, alpha=0.3)

        # Phase space resonance
        ax4 = plt.subplot(2, 2, 4, projection='polar')
        theta = np.angle([r for r in resonances])
        r = [abs(r) for r in resonances]
        ax4.scatter(theta, r, c=dims, cmap='twilight', s=2, alpha=0.6)
        ax4.set_title('Phase Space Resonance')

        plt.tight_layout()
        return fig

    def main(self):
        """Run the main analysis suite, printing results for each dimension (override for custom output)."""
        _ = self.figure()
        plt.savefig('nballs.png')
        plt.close('all')
        print("N-Ball Geometry Analysis Suite")
        print("==================================================\n")
        for d, label in self.dimensions().items():
            print(f"Dimension d = {label} ({d})")
            print("----------------------------------------")
            analysis = self.analyze_dimension(d)
            print(f"Volume:          {analysis['volume']:.8f}")
            print(f"Surface:         {analysis['surface']:.8f}")
            print(f"Next Surface:    {analysis['next_surface']:.8f}")
            print(f"Coupling Ratio:  {analysis['coupling_ratio']:.8f}")
            print(f"S/V Ratio:      {analysis['sv_ratio']:.8f}")
            print(f"Geom Freedom:   {analysis['geometric_freedom']:.8f}")
            print(f"Phase:          {analysis['phase']:.8f}\n")

if __name__ == "__main__":
    analyzer = NBallAnalyzer()
    analyzer.main()
