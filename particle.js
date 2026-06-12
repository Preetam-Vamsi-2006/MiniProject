// 3D Particle System
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];

// Reduce particle count on mobile for better performance
let particleCount = window.innerWidth < 768 ? 80 : 150;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.z = Math.random() * 100;
        this.vx = (Math.random() - 0.5) * 1.5;
        this.vy = (Math.random() - 0.5) * 1.5;
        this.vz = (Math.random() - 0.5) * 1.5;
        
        // Use white and light colors for better visibility on all backgrounds
        const colors = [
            '#FFFFFF',      // White
            '#E0E0E0',      // Light gray
            '#F0F0F0',      // Very light gray
            '#CCFFFF',      // Cyan
            '#FFCCFF',      // Magenta
            '#FFFFCC'       // Yellow
        ];
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.size = Math.random() * 5 + 2;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.z += this.vz;

        if (this.x < 0) this.x = canvas.width;
        if (this.x > canvas.width) this.x = 0;
        if (this.y < 0) this.y = canvas.height;
        if (this.y > canvas.height) this.y = 0;
        if (this.z < 0) this.z = 100;
        if (this.z > 100) this.z = 0;
    }

    draw() {
        const scale = this.z / 100;
        const x = this.x;
        const y = this.y;
        const size = this.size * scale;
        const opacity = scale;

        // Draw main particle
        ctx.fillStyle = this.color;
        ctx.globalAlpha = opacity * 0.9;
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
        
        // Add bright glow effect
        ctx.strokeStyle = '#FFFFFF';
        ctx.globalAlpha = opacity * 0.6;
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Add outer glow
        ctx.strokeStyle = this.color;
        ctx.globalAlpha = opacity * 0.3;
        ctx.lineWidth = 4;
        ctx.stroke();
        
        ctx.globalAlpha = 1;
    }
}

function initParticles() {
    particles.length = 0;
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }
}

let frameCount = 0;
function animate() {
    // Skip frames on mobile for better performance (render every other frame)
    frameCount++;
    const skipFrames = window.innerWidth < 768 ? 2 : 1;
    
    if (frameCount % skipFrames === 0) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        // Draw connections between nearby particles
        // Reduce connection distance on mobile
        const connectionDistance = window.innerWidth < 768 ? 100 : 150;
        
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < connectionDistance) {
                    // Use white for connections so they're always visible
                    ctx.strokeStyle = '#FFFFFF';
                    ctx.globalAlpha = (1 - distance / connectionDistance) * 0.4;
                    ctx.lineWidth = 1.5;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                    ctx.globalAlpha = 1;
                }
            }
        }
    }

    requestAnimationFrame(animate);
}

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Adjust particle count on resize
    const newCount = window.innerWidth < 768 ? 80 : 150;
    if (newCount !== particleCount) {
        particleCount = newCount;
        initParticles();
    }
});

initParticles();
animate();
