import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from scipy.integrate import trapezoid

class PhaseSpaceAnalyzer:
    def __init__(self, n_points=401):
        self.tau = 2 * np.pi
        self.n_points = n_points
        self.dims = np.linspace(0, 4, n_points)  # In τ units
        self.phases = np.linspace(0, 1, n_points)  # In τ units
        self.D, self.P = np.meshgrid(self.dims, self.phases)

    def dimension_phase(self, d):
        """Compute phase angle for dimension d in τ units"""
        base = d/2  # Base rotation
        integer = np.floor(d)  # Integer component
        remainder = d - integer  # Fractional component

        # Phase accumulation with integer jumps
        return (base + integer/4) % 1

    def wave_components(self, d, phi):
        """Compute forward and backward wave components"""
        phase = self.dimension_phase(d)
        # Forward wave with phase accumulation
        forward = np.cos(2*np.pi * (phi + phase))
        # Backward wave with phase conjugation
        backward = np.cos(2*np.pi * (phi - phase))
        return forward, backward

    def interference_pattern(self, d, phi):
        """Compute interference between forward and backward waves"""
        f, b = self.wave_components(d, phi)
        # Weighted interference based on dimension
        weight = 1 - np.exp(-d/2)  # Dimensional coupling strength
        return weight * (f + b)/2

    def coherence_measure(self, d):
        """Compute phase coherence with enhanced dimensional sensitivity"""
        phases = np.linspace(0, 1, self.n_points)
        # Get wave components
        forward = np.array([self.wave_components(d, phi)[0] for phi in phases])
        backward = np.array([self.wave_components(d, phi)[1] for phi in phases])

        # Compute interference strength
        interference = np.abs(np.mean(forward * backward))
        # Phase alignment measure
        alignment = np.abs(np.mean(forward + backward))/2

        return interference * alignment

    def phase_structure(self, d, n_theta=50, n_r=20):
        """Compute phase space structure for 3D visualization"""
        theta = np.linspace(0, 1, n_theta)  # In τ units
        r = np.linspace(0, 1, n_r)
        T, R = np.meshgrid(theta, r)

        # Compute wave interference pattern
        Z = np.array([[self.interference_pattern(d, phi) * r
                      for phi in theta] for r in r])

        # Transform to cartesian coordinates
        X = R * np.cos(2*np.pi * T)
        Y = R * np.sin(2*np.pi * T)

        return X, Y, Z

    def create_visualization(self):
        """Generate comprehensive phase space visualization"""
        fig = plt.figure(figsize=(20, 20))

        # Plot A: Center-Boundary Wave Organization
        ax1 = fig.add_subplot(221)
        sample_dims = [1, 2, 3, 4, 8]
        phases = np.linspace(0, 1, 200)

        for d in sample_dims:
            wave = [self.interference_pattern(d, phi) for phi in phases]
            ax1.plot(phases, wave, label=f'd={d}τ')

        ax1.set_xlim(0, 1)
        ax1.set_ylim(-1, 1)
        ax1.set_xlabel('Phase (τ units)')
        ax1.set_ylabel('Wave Amplitude')
        ax1.set_title('Center-Boundary Phase Organization')
        ax1.legend()
        ax1.grid(True)

        # Plot B: Phase Evolution
        ax2 = fig.add_subplot(222)
        phase_field = np.array([[self.interference_pattern(d, phi)
                               for d in self.dims]
                              for phi in self.phases])

        im = ax2.imshow(phase_field, aspect='auto',
                       extent=[0, 4, 0, 1],
                       cmap='RdBu', vmin=-1, vmax=1)
        ax2.set_xlabel('Dimension (τ units)')
        ax2.set_ylabel('Phase (τ units)')
        ax2.set_title('Phase Evolution')
        plt.colorbar(im, ax=ax2)

        # Plot C: Phase Coherence
        ax3 = fig.add_subplot(223)
        coherence = [self.coherence_measure(d) for d in self.dims]
        ax3.plot(self.dims, coherence, 'b-', linewidth=1)
        ax3.set_xlabel('Dimension (τ units)')
        ax3.set_ylabel('Phase Coherence')
        ax3.set_title('Phase Coherence Evolution')
        ax3.grid(True)

        # Plot D: Phase Space Structure
        ax4 = fig.add_subplot(224, projection='3d', proj_type='ortho')

        # Show structure for key dimensions with transparency
        dims = [1, 2, 4]
        alphas = [0.3, 0.4, 0.5]
        colors = plt.cm.viridis(np.linspace(0, 1, len(dims)))

        for d, color, alpha in zip(dims, colors, alphas):
            X, Y, Z = self.phase_structure(d)
            ax4.plot_surface(X, Y, Z, color=color, alpha=alpha)

        ax4.view_init(elev=35.264, azim=-45)
        ax4.set_title('Phase Space Structure')

        # Global title
        fig.suptitle(
            'Dimensional Evolution Through Phase Organization\n' +
            'Phase Space Analysis in τ Units',
            fontsize=16, y=0.95
        )

        plt.tight_layout(rect=[0, 0, 1, 0.95])

        now = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')
        name = f'phase-space-v4-{now}.png'
        plt.savefig(name, dpi=300, bbox_inches='tight')
        plt.close()

        return name

    def analyze_dimension(self, d):
        """Detailed analysis of dimensional characteristics"""
        # Sample points for analysis
        phases = np.linspace(0, 1, self.n_points)

        # Get wave components
        forward, backward = zip(*[self.wave_components(d, phi) for phi in phases])
        forward = np.array(forward)
        backward = np.array(backward)

        # Compute interference pattern
        interference = [self.interference_pattern(d, phi) for phi in phases]

        # Analysis metrics
        coherence = self.coherence_measure(d)
        phase_coupling = np.abs(np.mean(forward * backward))
        amplitude = np.max(np.abs(interference))
        phase_var = np.var(interference)
        base_phase = self.dimension_phase(d)

        return {
            'coherence': coherence,
            'phase_coupling': phase_coupling,
            'amplitude': amplitude,
            'phase_variance': phase_var,
            'base_phase': base_phase
        }

if __name__ == '__main__':
    analyzer = PhaseSpaceAnalyzer()
    output_file = analyzer.create_visualization()
    print(f"Generated visualization: {output_file}")

    special_dims = [1, np.e/analyzer.tau, np.pi/analyzer.tau, 2, 4/analyzer.tau, 8/analyzer.tau]
    print("\nAnalysis at special dimensions (in τ units):")

    for d in special_dims:
        analysis = analyzer.analyze_dimension(d)
        print(f"\nDimension {d:.3f}τ:")
        print(f"  Coherence: {analysis['coherence']:.6f}")
        print(f"  Phase Coupling: {analysis['phase_coupling']:.6f}")
        print(f"  Amplitude: {analysis['amplitude']:.6f}")
        print(f"  Phase Variance: {analysis['phase_variance']:.6f}")
        print(f"  Base Phase: {analysis['base_phase']:.6f}τ")