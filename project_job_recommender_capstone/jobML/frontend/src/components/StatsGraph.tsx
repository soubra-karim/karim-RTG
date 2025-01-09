import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

// Props type definition
type SkillData = {
  python: number;
  java: number;
  css: number;
  html: number;
  c: number;
};
type StatsGraphProps = {
  statsData: SkillData;
};
const StatsGraph: React.FC<StatsGraphProps> = ({ statsData }) => {
  const data = {
    labels:['Python', 'Java', 'CSS', 'HTML', 'C'],
    datasets: [
      {
        label: 'Number of Jobs per Skill',
        data: [
          statsData.python,
          statsData.java,
          statsData.css,
          statsData.html,
          statsData.c,
        ],
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    plugins: {
      title: {
        display: true,
        text: 'Total Skills per Job',
        font: {
          size: 24,
        },
      },
      legend: {
        display: true,
        position: 'bottom' as const,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
    responsive: true,
    maintainAspectRatio: false,
  };

  return <Bar data={data} options={options} />;
};

export default StatsGraph;