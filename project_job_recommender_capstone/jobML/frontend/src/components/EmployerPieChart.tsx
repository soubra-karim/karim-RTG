import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart, TooltipItem } from 'chart.js';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement, // This needs to be imported
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement, // And registered here
    Title,
    Tooltip,
    Legend
  );
  
// Mock data for the charts
const data = {
    labels: ['Data Science', 'Frontend', 'Backend', 'Other'],
    datasets: [
      {
        label: '# of Votes',
        data: [146, 32, 200, 1422 - (146 + 32 + 200)], // Other category calculated by subtracting known categories from total
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#cc65fe'
        ],
        hoverBackgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#cc65fe'
        ]
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom' as const, // Using 'as const' to narrow down the string to a literal type
      },
      title: { // Adding title options here
        display: true,
        text: 'Breakdown of Applicants',
        font: {
          size: 20
        },
        padding: {
          top: 10,
          bottom: 30
        }
      },
      tooltip: {
        callbacks: {
          label: function(context: TooltipItem<'doughnut'>) {
            let label = context.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed !== null) {
              const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
              const percentage = context.parsed as number / total;
              label += new Intl.NumberFormat('en-US', { style: 'percent', minimumFractionDigits: 2 }).format(percentage);
            }
            return label;
          }
        }
      }
    }
  };
  
  const Dashboard = () => {
    return <Doughnut data={data} options={options} />;
  };

export default Dashboard;