"""
N-Ball Geometry Analysis Suite
==================================================

Dimension d = 1 (1)
----------------------------------------
Volume:          2.00000000
Surface:         2.00000000
Next Surface:    6.28318531
Coupling Ratio:  0.50000000
S/V Ratio:      1.00000000
Geom Freedom:   2.00000000
Phase:          0.46364761

Dimension d = 2 (2)
----------------------------------------
Volume:          3.14159265
Surface:         6.28318531
Next Surface:    12.56637061
Coupling Ratio:  0.63661977
S/V Ratio:      2.00000000
Geom Freedom:   11.97437535
Phase:          0.56691150

Dimension d = 3 (3)
----------------------------------------
Volume:          4.18879020
Surface:         12.56637061
Next Surface:    19.73920880
Coupling Ratio:  0.75000000
S/V Ratio:      3.00000000
Geom Freedom:   28.36734393
Phase:          0.64350111

Dimension d = 4 (4)
----------------------------------------
Volume:          4.93480220
Surface:         19.73920880
Next Surface:    26.31894507
Coupling Ratio:  0.84882636
S/V Ratio:      4.00000000
Geom Freedom:   28.18722523
Phase:          0.70381231

Dimension d = 5 (5)
----------------------------------------
Volume:          5.26378901
Surface:         26.31894507
Next Surface:    31.00627668
Coupling Ratio:  0.93750000
S/V Ratio:      5.00000000
Geom Freedom:   9.19114457
Phase:          0.75315128

Dimension d = 6 (6)
----------------------------------------
Volume:          5.16771278
Surface:         31.00627668
Next Surface:    33.07336179
Coupling Ratio:  1.01859164
S/V Ratio:      6.00000000
Geom Freedom:   44.46751635
Phase:          0.79460810

Dimension d = 7 (7)
----------------------------------------
Volume:          4.72476597
Surface:         33.07336179
Next Surface:    32.46969701
Coupling Ratio:  1.09375000
S/V Ratio:      7.00000000
Geom Freedom:   17.63430368
Phase:          0.83014439

Dimension d = 8 (8)
----------------------------------------
Volume:          4.05871213
Surface:         32.46969701
Next Surface:    29.68658012
Coupling Ratio:  1.16410473
S/V Ratio:      8.00000000
Geom Freedom:   33.75064716
Phase:          0.86108362

Dimension d = 9 (9)
----------------------------------------
Volume:          3.29850890
Surface:         29.68658012
Next Surface:    25.50164040
Coupling Ratio:  1.23046875
S/V Ratio:      9.00000000
Geom Freedom:   25.27776223
Phase:          0.88836027

Dimension d = 10 (10)
----------------------------------------
Volume:          2.55016404
Surface:         25.50164040
Next Surface:    20.72514267
Coupling Ratio:  1.29344970
S/V Ratio:      10.00000000
Geom Freedom:   18.78197298
Phase:          0.91265792

Dimension d = 0.5 (0.5)
----------------------------------------
Volume:          1.46881258
Surface:         0.73440629
Next Surface:    3.85131113
Coupling Ratio:  0.41731342
S/V Ratio:      0.50000000
Geom Freedom:   0.36749278
Phase:          0.39534207

Dimension d = plastic (1.324718)
----------------------------------------
Volume:          2.36626415
Surface:         3.13463271
Next Surface:    8.14429230
Coupling Ratio:  0.54778516
S/V Ratio:      1.32471800
Geom Freedom:   4.12991840
Phase:          0.50114117

Dimension d = golden (1.618034)
----------------------------------------
Volume:          2.70361603
Surface:         4.37454266
Next Surface:    9.98688268
Coupling Ratio:  0.58790218
S/V Ratio:      1.61803400
Geom Freedom:   6.95701181
Phase:          0.53147655

Dimension d = e (2.718281828459045)
----------------------------------------
Volume:          3.91663882
Surface:         10.64652813
Next Surface:    17.71336482
Coupling Ratio:  0.71979309
S/V Ratio:      2.71828183
Geom Freedom:   24.01553572
Phase:          0.62388677

Dimension d = pi (3.141592653589793)
----------------------------------------
Volume:          4.31655917
Surface:         13.56087056
Next Surface:    20.74126506
Coupling Ratio:  0.76474681
S/V Ratio:      3.14159265
Geom Freedom:   30.12549698
Phase:          0.65287246

Dimension d = V-max (5.256946)
----------------------------------------
Volume:          5.27776802
Surface:         27.74494149
Next Surface:    31.80099466
Coupling Ratio:  0.95898218
S/V Ratio:      5.25694600
Geom Freedom:   21.51893776
Phase:          0.76446289

Dimension d = tau-1 (5.283185307179586)
----------------------------------------
Volume:          5.27762423
Surface:         27.88266680
Next Surface:    31.87199065
Coupling Ratio:  0.96114930
S/V Ratio:      5.28318531
Geom Freedom:   22.72559253
Phase:          0.76559059

Dimension d = tau (6.283185307179586)
----------------------------------------
Volume:          5.07258486
Surface:         31.87199065
Next Surface:    33.16029103
Coupling Ratio:  1.04042108
S/V Ratio:      6.28318531
Geom Freedom:   43.96354230
Phase:          0.80520574

Dimension d = SA-max (7.256946)
----------------------------------------
Volume:          4.56957989
Surface:         33.16119448
Next Surface:    31.93435621
Coupling Ratio:  1.11224900
S/V Ratio:      7.25694600
Geom Freedom:   2.74385293
Phase:          0.83849016

Dimension d = tau+1 (7.283185307179586)
----------------------------------------
Volume:          4.55299290
Surface:         33.16029103
Next Surface:    31.87199065
Coupling Ratio:  1.11412097
S/V Ratio:      7.28318531
Geom Freedom:   1.18661717
Phase:          0.83932616
"""

import numpy as np
from math import gamma, tau, pi, e

import matplotlib.pyplot
matplotlib.use('Agg')

class NBallAnalyzer:

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


class ComplexSphereDynamics(NBallAnalyzer):

    def ball_volume(self, d):
        # Override to handle complex dimensions
        try:
            return (pi ** (d / 2)) / gamma(d / 2 + 1)
        except:
            return 0

    def ball_surface(self, d):
        # Override to handle complex dimensions
        try:
            return tau * (pi ** ((d - 2) / 2)) / gamma(d / 2)
        except:
            return 0

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

def generate_infosheet():
    analyzer = NBallAnalyzer()

    # Define the first 10 integer dimensions
    dimensions = {k: str(k) for k in range(1, 11)}

    # Define special dimensions with their updated numerical values
    dimensions = {
        0.5: '0.5',
        1.324718: 'plastic',
        1.618034: 'golden',
        e: 'e',
        pi: 'pi',
        5.256946: 'V-max',
        tau - 1: 'tau-1',
        tau: 'tau',
        7.256946: 'SA-max',
        tau + 1: 'tau+1',
    }

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

    for d in sorted(dimensions):
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
