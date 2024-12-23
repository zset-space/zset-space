import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from scipy.integrate import trapezoid

class WavePhaseAnalyzer:
    def __init__(self, n_points=401):
        self.tau = 2 * np.pi
        self.n_points = n_points
        self.dims = np.linspace(0, 4, n_points)  # In τ units
        self.phases = np.linspace(0, 1, n_points)  # In τ units
        self.D, self.P = np.meshgrid(self.dims, self.phases)
        
    def dimensional_wave(self, d, phi, mode='center'):
        """Compute dimensional wave with phase coupling."""
        # Base phase with dimension-dependent rotation
        base_phase = d * np.pi/2 + phi * self.tau
        
        # Add dimension-specific modulation
        dim_mod = np.exp(-((d % 1) - 0.5)**2 / 0.1)
        
        if mode == 'center':
            # Center wave with forward evolution
            phase = base_phase + d * self.tau/4
            amplitude = np.exp(-d/4) * (1 + dim_mod)
        else:
            # Boundary wave with backward evolution
            phase = -base_phase - d * self.tau/4
            amplitude = np.exp(-d/4) * (1 - dim_mod)
            
        return amplitude * np.cos(phase)
    
    def coupled_waves(self, d, phi):
        """Compute coupled center-boundary waves."""
        # Get individual waves
        center = self.dimensional_wave(d, phi, 'center')
        boundary = self.dimensional_wave(d, phi, 'boundary')
        
        # Compute coupling strength
        coupling = np.exp(-((d % 1) - 0.5)**2 / 0.2)
        
        # Return coupled system
        return center + boundary * coupling
    
    def phase_field(self, d, phi):
        """Compute complete phase field with interactions."""
        waves = self.coupled_waves(d, phi)
        # Add phase space curvature
        curvature = np.exp(-((d % 1) - 0.5)**2 / 0.3)
        return waves * (1 + curvature * np.cos(2*np.pi*phi))
    
    def coherence_measure(self, d):
        """Enhanced coherence measure with phase sensitivity."""
        phases = np.linspace(0, 1, self.n_points)
        field = np.array([self.phase_field(d, phi) for phi in phases])
        
        # Primary coherence through phase alignment
        primary = np.abs(np.mean(field))
        
        # Secondary coherence through phase variation
        secondary = np.abs(np.mean(np.exp(1j * 2*np.pi * phases) * field))
        
        # Combine measures with dimensional weighting
        weight = np.exp(-((d % 1) - 0.5)**2 / 0.1)
        return (primary + weight * secondary) * 1e-3
    
    def create_visualization(self):
        """Generate enhanced phase space visualization."""
        fig = plt.figure(figsize=(20, 20))
        
        # Plot A: Dimensional Wave Organization
        ax1 = fig.add_subplot(221)
        phases = np.linspace(0, 1, 200)
        
        for d in [1, 2, 3, 4, 8]:
            wave = [self.coupled_waves(d/self.tau, phi) for phi in phases]
            ax1.plot(phases, wave, label=f'd={d}τ')
        
        ax1.set_xlim(0, 1)
        ax1.set_ylim(-1, 1)
        ax1.set_xlabel('Phase (τ units)')
        ax1.set_ylabel('Wave Amplitude')
        ax1.set_title('Center-Boundary Wave Organization')
        ax1.legend()
        ax1.grid(True)
        
        # Plot B: Phase Evolution Field
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
        coherence = [self.coherence_measure(d) for d in self.dims]
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
        
        # Sample dimensions for structure visualization
        dims = [1, 2, 4]
        alphas = [0.3, 0.4, 0.5]
        colors = ['lightblue', 'lightgreen', 'salmon']
        
        for d, alpha, color in zip(dims, alphas, colors):
            # Compute wave structure
            Z = np.array([[self.coupled_waves(d, phi/self.tau) * r 
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
        name = f'phase-space-v5-{now}.png'
        plt.savefig(name, dpi=300, bbox_inches='tight')
        plt.close()
        
        return name
        
    def analyze_layer(self, d):
        """Analyze dimensional layer structure."""
        phases = np.linspace(0, 1, self.n_points)
        
        # Get wave components
        center = np.array([self.dimensional_wave(d, phi, 'center') 
                         for phi in phases])
        boundary = np.array([self.dimensional_wave(d, phi, 'boundary') 
                           for phi in phases])
        coupled = np.array([self.coupled_waves(d, phi) for phi in phases])
        
        # Phase field analysis
        field = np.array([self.phase_field(d, phi) for phi in phases])
        
        # Compute various measures
        return {
            'center_power': np.mean(center**2),
            'boundary_power': np.mean(boundary**2),
            'coupling_strength': np.mean(center * boundary),
            'field_coherence': np.abs(np.mean(field)),
            'phase_structure': np.var(field),
            'boundary_ratio': np.mean(np.abs(boundary/center))
        }

if __name__ == '__main__':
    analyzer = WavePhaseAnalyzer()
    output_file = analyzer.create_visualization()
    print(f"Generated visualization: {output_file}")
    
    # Analyze special points
    special_points = [
        (1, "Unity Dimension"),
        (np.e/2/np.pi, "e/τ Point"),
        (np.pi/2/np.pi, "π/τ Point"),
        (2, "Double Dimension"),
        (4/2/np.pi, "Quaternion Scale"),
        (8/2/np.pi, "Octonion Scale")
    ]
    
    print("\nDetailed Layer Analysis:")
    for d, name in special_points:
        analysis = analyzer.analyze_layer(d)
        print(f"\n{name} (d={d:.3f}τ):")
        for key, value in analysis.items():
            print(f"  {key}: {value:.6f}")
