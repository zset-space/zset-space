"""N-Ball Geometry Analysis Suite"""

import numpy as np
from math import gamma, tau, pi, e

import matplotlib.pyplot
matplotlib.use('Agg')

class NBallAnalyzer:

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

def generate_infosheet():
    analyzer = NBallAnalyzer()
    dimensions = analyzer.dimensions()

    # Initialize lists to store metrics for plotting
    metrics = {
        'Volume': [],
        'Surface': [],
        'Coupling Ratio': [],
        'S/V Ratio': [],
        'Geom Freedom': [],
        'Phase': []
    }

    numerical_dims = []

    # Print Header
    print("N-Ball Geometry Analysis Suite")
    print("==================================================\n")

    for d in dimensions:
        numerical_dims.append(d)
        print(f"Dimension d = {dimensions[d]} ({d})")
        print("----------------------------------------")

        analysis = analyzer.analyze_dimension(d)

        print(f"Volume:          {analysis['volume']:.8f}")
        print(f"Surface:         {analysis['surface']:.8f}")
        print(f"Next Surface:    {analysis['next_surface']:.8f}")
        print(f"Coupling Ratio:  {analysis['coupling_ratio']:.8f}")
        print(f"S/V Ratio:      {analysis['sv_ratio']:.8f}")
        print(f"Geom Freedom:   {analysis['geometric_freedom']:.8f}")
        print(f"Phase:          {analysis['phase']:.8f}\n")

        # Append metrics for plotting
        metrics['Volume'].append(analysis['volume'])
        metrics['Surface'].append(analysis['surface'])
        metrics['Coupling Ratio'].append(analysis['coupling_ratio'])
        metrics['S/V Ratio'].append(analysis['sv_ratio'])
        metrics['Geom Freedom'].append(analysis['geometric_freedom'])
        metrics['Phase'].append(analysis['phase'])

    # Plotting the metrics
    fig, axs = matplotlib.pyplot.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('N-Ball Geometry Metrics Across Dimensions', fontsize=16)

    # Volume
    axs[0, 0].plot(numerical_dims, metrics['Volume'], marker='o', linestyle='-', color='blue')
    axs[0, 0].set_title('Volume vs Dimension')
    axs[0, 0].set_xlabel('Dimension d')
    axs[0, 0].set_ylabel('Volume')
    axs[0, 0].grid(True)

    # Surface
    axs[0, 1].plot(numerical_dims, metrics['Surface'], marker='s', linestyle='-', color='green')
    axs[0, 1].set_title('Surface Area vs Dimension')
    axs[0, 1].set_xlabel('Dimension d')
    axs[0, 1].set_ylabel('Surface Area')
    axs[0, 1].grid(True)

    # Coupling Ratio
    axs[0, 2].plot(numerical_dims, metrics['Coupling Ratio'], marker='^', linestyle='-', color='red')
    axs[0, 2].set_title('Coupling Ratio vs Dimension')
    axs[0, 2].set_xlabel('Dimension d')
    axs[0, 2].set_ylabel('Coupling Ratio')
    axs[0, 2].grid(True)

    # S/V Ratio
    axs[1, 0].plot(numerical_dims, metrics['S/V Ratio'], marker='d', linestyle='-', color='purple')
    axs[1, 0].set_title('S/V Ratio vs Dimension')
    axs[1, 0].set_xlabel('Dimension d')
    axs[1, 0].set_ylabel('S/V Ratio')
    axs[1, 0].grid(True)

    # Geom Freedom
    axs[1, 1].plot(numerical_dims, metrics['Geom Freedom'], marker='*', linestyle='-', color='orange')
    axs[1, 1].set_title('Geometric Freedom vs Dimension')
    axs[1, 1].set_xlabel('Dimension d')
    axs[1, 1].set_ylabel('Geometric Freedom')
    axs[1, 1].grid(True)

    # Phase
    axs[1, 2].plot(numerical_dims, metrics['Phase'], marker='p', linestyle='-', color='brown')
    axs[1, 2].set_title('Phase vs Dimension')
    axs[1, 2].set_xlabel('Dimension d')
    axs[1, 2].set_ylabel('Phase')
    axs[1, 2].grid(True)

    matplotlib.pyplot.tight_layout(rect=[0, 0.03, 1, 0.95])
    matplotlib.pyplot.savefig('nball_geometry_metrics.png')

if __name__ == "__main__":
    generate_infosheet()
