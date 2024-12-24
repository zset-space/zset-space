import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from scipy.integrate import trapezoid

class PhaseSpaceAnalyzer:
    """Analyzer for dimensional evolution through phase organization."""

    def __init__(self, n_points=401):
        self.tau = 2 * np.pi
        self.n_points = n_points
        self.dims = np.linspace(0, 4*self.tau, n_points)
        self.phases = np.linspace(0, self.tau, n_points)
        self.D, self.P = np.meshgrid(self.dims, self.phases)

    def dimension_phase(self, d):
        """Compute phase angle for dimension d."""
        # Base phase rotation
        base = d * self.tau/2
        # Integer phase accumulation
        accum = np.floor(d) * np.pi/2
        return (base + accum) % self.tau

    def center_component(self, d, phi):
        """Compute center wave component."""
        phase = self.dimension_phase(d)
        return np.cos(phi + phase)

    def boundary_component(self, d, phi):
        """Compute boundary wave component."""
        phase = self.dimension_phase(d)
        return np.cos(phi - phase)

    def wave_interference(self, d, phi):
        """Compute wave interference pattern."""
        return (self.center_component(d, phi) +
                self.boundary_component(d, phi))/2

    def phase_coherence(self, d):
        """Compute phase coherence."""
        phases = np.linspace(0, self.tau, self.n_points)
        waves = np.array([self.wave_interference(d, phi) for phi in phases])
        return np.mean(np.abs(waves))

    def create_visualization(self):
        """Generate comprehensive phase space visualization."""
        fig = plt.figure(figsize=(20, 20))

        # Plot A: Center-Boundary Phase Organization
        ax1 = fig.add_subplot(221)

        # Sample dimensions for visualization
        sample_dims = [1, 2, 3, 4, 8]
        for d in sample_dims:
            phases = np.linspace(0, self.tau, 100)
            wave = [self.wave_interference(d, phi) for phi in phases]
            ax1.plot(phases/self.tau, wave, label=f'd={d}')

        ax1.set_xlim(0, 1)
        ax1.set_ylim(-1, 1)
        ax1.set_title('Center-Boundary Phase Organization')
        ax1.legend()
        ax1.grid(True)

        # Plot B: Phase Evolution
        ax2 = fig.add_subplot(222)

        interference = np.array([[self.wave_interference(d, phi)
                                for d in self.dims/self.tau]
                               for phi in self.phases/self.tau])

        im = ax2.imshow(interference, aspect='auto',
                       extent=[0, 4, 0, 1],
                       cmap='RdBu', vmin=-1, vmax=1)
        ax2.set_title('Phase Evolution')
        plt.colorbar(im, ax=ax2)

        # Plot C: Threading Potential
        ax3 = fig.add_subplot(223)

        coherence = np.array([self.phase_coherence(d) for d in self.dims])
        dim_scale = self.dims/self.tau

        ax3.plot(dim_scale, coherence, 'b-')
        ax3.set_xlabel('Dimension (τ units)')
        ax3.set_ylabel('Phase Coherence')
        ax3.set_title('Phase Coherence Evolution')
        ax3.grid(True)

        # Plot D: Phase Space Structure
        ax4 = fig.add_subplot(224, projection='3d', proj_type='ortho')

        # Create phase space coordinates
        theta = np.linspace(0, self.tau, 50)
        r = np.linspace(0, 1, 20)
        T, R = np.meshgrid(theta, r)

        # Sample a few dimensions for structure
        dims = [1, 2, 3, 4]
        colors = plt.cm.viridis(np.linspace(0, 1, len(dims)))

        for d, color in zip(dims, colors):
            Z = np.array([[self.wave_interference(d, phi) * r
                          for phi in theta] for r in r])
            X = R * np.cos(T)
            Y = R * np.sin(T)
            ax4.plot_surface(X, Y, Z, color=color, alpha=0.3)

        ax4.view_init(elev=35.264, azim=-45)
        ax4.set_title('Phase Space Structure')

        # Global title
        fig.suptitle(
            'Dimensional Evolution Through Phase Organization\n' +
            'Phase Space Analysis in τ Units',
            fontsize=16, y=0.95
        )

        plt.tight_layout(rect=[0, 0, 1, 0.95])

        # Save visualization
        now = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')
        name = f'phase-space-v3-{now}.png'
        plt.savefig(name, dpi=300, bbox_inches='tight')
        plt.close()

        return name

    def analyze_dimension(self, d):
        """Detailed analysis of a specific dimension."""
        phases = np.linspace(0, self.tau, self.n_points)
        waves = np.array([self.wave_interference(d, phi) for phi in phases])

        coherence = np.mean(np.abs(waves))
        max_amplitude = np.max(np.abs(waves))
        phase_variance = np.var(waves)

        return {
            'coherence': coherence,
            'amplitude': max_amplitude,
            'phase_variance': phase_variance,
            'base_phase': self.dimension_phase(d)/self.tau
        }

if __name__ == '__main__':
    analyzer = PhaseSpaceAnalyzer()
    output_file = analyzer.create_visualization()
    print(f"Generated visualization: {output_file}")

    print("\nAnalysis at special dimensions:")
    special_dims = [1, np.e, np.pi, 2*np.pi, 4, 8]

    for d in special_dims:
        analysis = analyzer.analyze_dimension(d)
        print(f"\nDimension {d:.3f}:")
        print(f"  Coherence: {analysis['coherence']:.6f}")
        print(f"  Amplitude: {analysis['amplitude']:.6f}")
        print(f"  Phase Variance: {analysis['phase_variance']:.6f}")
        print(f"  Base Phase: {analysis['base_phase']:.6f}τ")