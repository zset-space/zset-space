import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

class PhaseOrganizer:
    """Analyzer for phase organization between bulk and surface."""
    
    def __init__(self, n_points=401):
        self.tau = 2 * np.pi
        self.n_points = n_points
        self.dims = np.linspace(0, 4, n_points)  # In τ units
        self.phases = np.linspace(0, 1, n_points)  # In τ units
        self.D, self.P = np.meshgrid(self.dims, self.phases)
        
    def potential_field(self, d, r):
        """Compute phase potential field.
        
        This represents the total rotational potential available
        before it organizes into bulk and surface components.
        """
        # Base potential scales with dimension
        base = d * self.tau
        
        # Add radial dependence
        radial = np.exp(-((r - 0.5)**2)/0.1)
        
        # Phase organization factor
        organization = 1 - np.exp(-d)
        
        return base * radial * organization
    
    def phase_split(self, d, r):
        """Compute how phase potential splits into bulk and surface.
        
        Returns both components to show how they emerge together.
        """
        # Get total potential
        total = self.potential_field(d, r)
        
        # Organization parameter
        alpha = 1 - np.exp(-d)
        
        # Split potential based on radial position
        bulk = total * (1 - r) * alpha
        surface = total * r * alpha
        
        return bulk, surface
    
    def coherence_measure(self, d):
        """Measure phase coherence between bulk and surface."""
        r = np.linspace(0, 1, self.n_points)
        bulk, surface = self.phase_split(d, r)
        
        # Compute correlation
        correlation = np.mean(bulk * surface)
        
        # Scale by dimensional organization
        organization = 1 - np.exp(-d)
        
        return correlation * organization
    
    def create_visualization(self):
        """Generate visualization of phase organization process."""
        fig = plt.figure(figsize=(20, 20))
        
        # Plot A: Potential Field
        ax1 = fig.add_subplot(221)
        r = np.linspace(0, 1, 100)
        
        for d in [0.5, 1, 2, 4]:
            potential = self.potential_field(d, r)
            ax1.plot(r, potential, label=f'd={d}τ')
            
        ax1.set_xlabel('Radius')
        ax1.set_ylabel('Phase Potential')
        ax1.set_title('Phase Potential Distribution')
        ax1.legend()
        ax1.grid(True)
        
        # Plot B: Bulk-Surface Evolution
        ax2 = fig.add_subplot(222)
        d_sample = 2  # Sample at d=2τ
        bulk, surface = self.phase_split(d_sample, r)
        
        ax2.plot(r, bulk, 'b-', label='Bulk')
        ax2.plot(r, surface, 'r-', label='Surface')
        ax2.plot(r, bulk + surface, 'k--', label='Total', alpha=0.5)
        
        ax2.set_xlabel('Radius')
        ax2.set_ylabel('Phase Component')
        ax2.set_title(f'Bulk-Surface Split at d={d_sample}τ')
        ax2.legend()
        ax2.grid(True)
        
        # Plot C: Coherence Evolution
        ax3 = fig.add_subplot(223)
        coherence = [self.coherence_measure(d) for d in self.dims]
        ax3.plot(self.dims, coherence, 'b-')
        
        ax3.set_xlabel('Dimension (τ units)')
        ax3.set_ylabel('Bulk-Surface Coherence')
        ax3.set_title('Phase Organization Coherence')
        ax3.grid(True)
        
        # Plot D: Phase Space Structure
        ax4 = fig.add_subplot(224, projection='3d', proj_type='ortho')
        
        # Create phase space coordinates
        theta = np.linspace(0, self.tau, 50)
        r_space = np.linspace(0, 1, 20)
        T, R = np.meshgrid(theta, r_space)
        
        # Sample dimensions
        dims = [1, 2, 4]
        colors = ['lightblue', 'lightgreen', 'salmon']
        alphas = [0.3, 0.4, 0.5]
        
        for d, color, alpha in zip(dims, colors, alphas):
            bulk, surface = self.phase_split(d, R)
            Z = bulk * np.cos(T) + surface * np.sin(T)
            X = R * np.cos(T)
            Y = R * np.sin(T)
            
            ax4.plot_surface(X, Y, Z, color=color, alpha=alpha)
            
        ax4.view_init(elev=35.264, azim=-45)
        ax4.set_title('Phase Space Organization')
        
        # Global title
        fig.suptitle(
            'Phase Organization Analysis\n' +
            'Bulk-Surface Emergence through Phase Coherence',
            fontsize=16, y=0.95
        )
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        now = datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')
        name = f'phase-org-{now}.png'
        plt.savefig(name, dpi=300, bbox_inches='tight')
        plt.close()
        
        return name
        
    def analyze_organization(self, d):
        """Analyze phase organization at given dimension."""
        r = np.linspace(0, 1, self.n_points)
        
        # Get components
        potential = self.potential_field(d, r)
        bulk, surface = self.phase_split(d, r)
        
        # Compute metrics
        return {
            'total_potential': np.sum(potential),
            'bulk_fraction': np.sum(bulk)/np.sum(potential),
            'surface_fraction': np.sum(surface)/np.sum(potential),
            'coherence': self.coherence_measure(d),
            'organization': 1 - np.exp(-d)
        }

if __name__ == '__main__':
    analyzer = PhaseOrganizer()
    output_file = analyzer.create_visualization()
    print(f"Generated visualization: {output_file}")
    
    print("\nPhase Organization Analysis:")
    for d in [0.5, 1, 2, 4, 8]:
        d_tau = d/2/np.pi
        analysis = analyzer.analyze_organization(d_tau)
        print(f"\nDimension {d}:")
        for key, value in analysis.items():
            print(f"  {key}: {value:.6f}")