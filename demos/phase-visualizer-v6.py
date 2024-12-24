import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

class DimensionalWaveAnalyzer:
    def __init__(self, n_points=401):
        self.tau = 2 * np.pi
        self.n_points = n_points
        self.dims = np.linspace(0, 4, n_points)  # In τ units
        self.phases = np.linspace(0, 1, n_points)  # In τ units
        self.D, self.P = np.meshgrid(self.dims, self.phases)

    def wave_component(self, d, phi, direction='up'):
        """Compute wave component with linear phase progression."""
        # Base frequency increases with dimension
        freq = d * self.tau

        # Linear phase progression
        if direction == 'up':
            phase = freq * phi
        else:
            phase = -freq * phi + np.pi/2  # Quarter turn offset for boundary

        return np.cos(phase)

    def dimensional_interference(self, d, phi):
        """Compute interference between center and boundary waves."""
        # Get base components
        center = self.wave_component(d, phi, 'up')
        boundary = self.wave_component(d, phi, 'down')

        # Add dimensional weight
        weight = 1 - (d % 1)  # Linear weight transition

        return (center + weight * boundary)/(1 + weight)

    def phase_field(self, d, phi):
        """Compute phase field with dimensional evolution."""
        # Base interference
        wave = self.dimensional_interference(d, phi)

        # Add dimensional modulation
        mod = np.sin(2*np.pi * d)  # Dimensional oscillation

        return wave * (1 + 0.1 * mod)

    def compute_coherence(self, d):
        """Compute phase coherence with dimensional sensitivity."""
        phases = np.linspace(0, 1, 100)
        waves = [self.phase_field(d, phi) for phi in phases]

        # Primary coherence
        mean_wave = np.mean(waves)

        # Add dimensional weight
        weight = np.exp(-((d % 1) - 0.5)**2)

        return np.abs(mean_wave) * weight * 1e-3

    def create_visualization(self):
        """Generate enhanced phase space visualization."""
        fig = plt.figure(figsize=(20, 20))

        # Plot A: Wave Components
        ax1 = fig.add_subplot(221)
        phases = np.linspace(0, 1, 200)

        for d in [1, 2, 3, 4, 8]:
            wave = [self.dimensional_interference(d/self.tau, phi)
                   for phi in phases]
            ax1.plot(phases, wave, label=f'd={d}τ')

        ax1.set_xlim(0, 1)
        ax1.set_ylim(-1, 1)
        ax1.set_xlabel('Phase (τ units)')
        ax1.set_ylabel('Wave Amplitude')
        ax1.set_title('Center-Boundary Wave Organization')
        ax1.legend()
        ax1.grid(True)

        # Plot B: Phase Evolution
        ax2 = fig.add_subplot(222)

        field = np.array([[self.phase_field(d, phi)
                          for d in self.dims]
                         for phi in self.phases])

        im = ax2.imshow(field, aspect='auto',
                       extent=[0, 4, 0, 1],
                       cmap='RdBu', vmin=-1, vmax=1)
        ax2.set_xlabel('Dimension (τ units)')
        ax2.set_ylabel('Phase (τ units)')
        ax2.set_title('Phase Evolution')
        plt.colorbar(im, ax=ax2)

        # Plot C: Coherence Pattern
        ax3 = fig.add_subplot(223)
        coherence = [self.compute_coherence(d) for d in self.dims]
        ax3.plot(self.dims, coherence, 'b-', linewidth=1)
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

        # Sample key dimensions
        dims = [1, 2, 3]
        colors = ['lightblue', 'lightgreen', 'salmon']
        alphas = [0.3, 0.4, 0.5]

        for d, color, alpha in zip(dims, colors, alphas):
            # Generate surface
            Z = np.array([[self.phase_field(d, phi/self.tau) * r
                          for phi in theta]
                         for r in r])
            X = R * np.cos(T)
            Y = R * np.sin(T)

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
        name = f'phase-space-v6-{now}.png'
        plt.savefig(name, dpi=300, bbox_inches='tight')
        plt.close()

        return name

    def analyze_wave_structure(self, d):
        """Analyze wave structure at specific dimension."""
        phases = np.linspace(0, 1, self.n_points)

        # Get wave components
        center = np.array([self.wave_component(d, phi, 'up')
                         for phi in phases])
        boundary = np.array([self.wave_component(d, phi, 'down')
                           for phi in phases])
        interference = np.array([self.dimensional_interference(d, phi)
                               for phi in phases])

        # Compute metrics
        return {
            'wave_frequency': d * self.tau,
            'center_amplitude': np.max(np.abs(center)),
            'boundary_amplitude': np.max(np.abs(boundary)),
            'interference_strength': np.mean(center * boundary),
            'phase_coherence': np.abs(np.mean(interference)),
            'dimensional_weight': 1 - (d % 1)
        }

if __name__ == '__main__':
    analyzer = DimensionalWaveAnalyzer()
    output_file = analyzer.create_visualization()
    print(f"Generated visualization: {output_file}")

    print("\nWave Structure Analysis:")
    for d in [1, 2, 3, 4, 8]:
        d_tau = d/2/np.pi  # Convert to τ units
        analysis = analyzer.analyze_wave_structure(d_tau)
        print(f"\nDimension {d}:")
        for key, value in analysis.items():
            print(f"  {key}: {value:.6f}")