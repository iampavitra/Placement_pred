/**
 * PlacementPredict - Adpanel Minimal Classy Client-side JS
 * Handles Chart.js initialization, input synchronizations, and responsive interactivity.
 */

document.addEventListener('DOMContentLoaded', () => {
    // =========================================================================
    // 1. Chart.js Interactive Visualizations (Minimal Classy Adpanel Style)
    // =========================================================================

    // Donut Chart: Placement Count
    const donutCtx = document.getElementById('placementDonutChart');
    if (donutCtx && typeof Chart !== 'undefined') {
        new Chart(donutCtx, {
            type: 'doughnut',
            data: {
                labels: ['Placed', 'Not Placed'],
                datasets: [{
                    data: [770, 430],
                    backgroundColor: ['#8774E1', '#2D1B3D'],
                    borderColor: '#FFFFFF',
                    borderWidth: 4,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '76%',
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart',
                    animateScale: true
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#0A0A0A',
                        titleColor: '#FFFFFF',
                        bodyColor: '#E5E5E5',
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const total = 1200;
                                const val = context.raw;
                                const pct = ((val / total) * 100).toFixed(1);
                                return ` ${context.label}: ${val} (${pct}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Bar Chart: Placement by Gender
    const genderCtx = document.getElementById('genderBarChart');
    if (genderCtx && typeof Chart !== 'undefined') {
        new Chart(genderCtx, {
            type: 'bar',
            data: {
                labels: ['Male', 'Female'],
                datasets: [
                    {
                        label: 'Placed',
                        data: [470, 300],
                        backgroundColor: '#8774E1',
                        borderRadius: 6,
                        barThickness: 28
                    },
                    {
                        label: 'Not Placed',
                        data: [260, 170],
                        backgroundColor: '#2D1B3D',
                        borderRadius: 6,
                        barThickness: 28
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1800,
                    easing: 'easeOutQuart'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#0A0A0A',
                        titleColor: '#FFFFFF',
                        bodyColor: '#E5E5E5',
                        padding: 10,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#737373', font: { family: 'Plus Jakarta Sans', size: 12, weight: '500' } }
                    },
                    y: {
                        grid: { color: 'rgba(0, 0, 0, 0.04)' },
                        ticks: { color: '#999999', font: { family: 'Plus Jakarta Sans', size: 11 } }
                    }
                }
            }
        });
    }

    // Bar Chart: Placement by Stream
    const streamCtx = document.getElementById('streamBarChart');
    if (streamCtx && typeof Chart !== 'undefined') {
        new Chart(streamCtx, {
            type: 'bar',
            data: {
                labels: ['CSE', 'ECE', 'EEE', 'ME', 'Others'],
                datasets: [{
                    label: 'Placed',
                    data: [210, 165, 140, 115, 80],
                    backgroundColor: '#A388EE',
                    borderRadius: 6,
                    barThickness: 30
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 2200,
                    easing: 'easeOutQuint'
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#0A0A0A',
                        titleColor: '#FFFFFF',
                        bodyColor: '#E5E5E5',
                        padding: 10,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#737373', font: { family: 'Plus Jakarta Sans', size: 12, weight: '500' } }
                    },
                    y: {
                        grid: { color: 'rgba(0, 0, 0, 0.04)' },
                        ticks: { color: '#999999', font: { family: 'Plus Jakarta Sans', size: 11 } }
                    }
                }
            }
        });
    }

    // =========================================================================
    // 2. Synchronize Graduation Percentage / CGPA in Predict Form
    // =========================================================================
    const cgpaInput = document.getElementById('CGPA');
    if (cgpaInput) {
        cgpaInput.addEventListener('change', () => {
            let val = parseFloat(cgpaInput.value);
            if (!isNaN(val)) {
                if (val > 10.0 && val <= 100.0) {
                    console.log('Graduation Percentage supplied: ', val);
                }
            }
        });
    }
});
