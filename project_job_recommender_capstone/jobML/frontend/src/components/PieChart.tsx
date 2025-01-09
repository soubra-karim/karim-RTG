import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, TooltipItem, Tooltip, Legend } from 'chart.js';
import Chart from 'chart.js/auto';

ChartJS.register(ArcElement, Tooltip, Legend);

type PieChartProps = {
  statsData: {
    totalUsers: number;
    totalRecruiters: number;
    totalApplicants: number;
    totalJobPostings: number;
    dataScienceRoles: number;
    frontendRoles: number;
    backend_roles: number;
    computer_engineering_roles: number,
    electrical_engineering_roles:number
  };
};

const PieChart: React.FC<PieChartProps> = ({ statsData }) => {
  // Create the data object using statsData
  const data = {
    labels: ['Data Science', 'Frontend', 'Backend', 'Computer Engineering', 'Electircal Engineering', 'Other'],
    datasets: [
      {
        label: '# of Votes',
        data: [
          statsData.dataScienceRoles,
          statsData.frontendRoles,
          statsData.backend_roles,
          statsData.computer_engineering_roles,
          statsData.electrical_engineering_roles,
          statsData.totalJobPostings - (
            statsData.dataScienceRoles +
            statsData.frontendRoles +
            statsData.backend_roles +
            statsData.computer_engineering_roles +
           statsData.electrical_engineering_roles

          ),
        ],
        backgroundColor: [
          '#FF6384', // existing pink
          '#36A2EB', // existing blue
          '#FFCE56', // existing yellow
          '#cc65fe', // existing purple
          '#4BC0C0', // new teal
          '#FF9F40', // new orange
        ],
        hoverBackgroundColor: [
          '#FF6384', // existing pink
          '#36A2EB', // existing blue
          '#FFCE56', // existing yellow
          '#cc65fe', // existing purple
          '#4BC0C0', // new teal
          '#FF9F40', // new orange
        ],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      title: {
        display: true,
        text: 'Breakdown of Jobs',
        font: {
          size: 20,
        },
        padding: {
          top: 10,
          bottom: 30,
        },
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
          },
        },
      },
    },
  };

  return <Doughnut data={data} options={options} />;
};

export default PieChart;