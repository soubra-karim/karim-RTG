import { FunctionComponent } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Navigation2 from '../components/Navigation2';
import Footer from '../components/Footer';
import styles from './EmployerLikedApplicants.module.css';

type Skill = {
  skill_name: string;
};

type WorkExperience = {
  company_name: string;
  end_date: string;
  job_description: string;
  job_title: string;
  start_date: string;
};

type Education = {
  school_name: string;
  degree: string;
  start_date: string; // or Date
  end_date: string;   // or Date
  gpa?: string;
};

type Applicant = {
  id: string;
  name: string;
  email?: string;
  phone_number?: string;
  skills?: Skill[];
  educations?: Education[];
  work_experiences?: WorkExperience[];
  projects?: string[];
};

type ApplicantsByJobTitle = {
  [jobTitle: string]: Applicant[];
};

type LocationState = {
  applicants: ApplicantsByJobTitle;
};

const EmployerLikedApplicants: FunctionComponent = () => {
  const location = useLocation(); // You can type this with <LocationState> if it's causing errors, leave it untyped.
  const state = location.state as LocationState; // Cast the state to the LocationState type.
  
  const navigate = useNavigate();

  const jobPositionsWithApplicants = state.applicants;

  const viewApplicant = (applicant: Applicant) => {
    // Assuming that the applicant object has an 'id' property that is used for navigation
    navigate(`/candidatepage/${applicant.id}`, { state: { applicant } });
  };

  return (
    <div className={styles.candidateSearchPage}>
      <Navigation2 />
      <div className={styles.jobListingsContainer}>
        <h1 className={styles.searchResultsTitle}>Your liked candidates</h1>
        {Object.entries(jobPositionsWithApplicants).map(([jobPosition, applicants]) => (
          <div className={styles.jobContainer} key={jobPosition}>
            <h2 className={styles.jobPositionTitle}>{jobPosition}</h2>
            {applicants.map((applicant) => ( // Assuming Applicant has a unique identifier called 'id'.
              <div key={applicant.id} className={styles.jobCard}>
                <div>
                  <h3 className={styles.jobTitle}>{applicant.name}</h3>
                  <div className={styles.jobDetails}>
                    <span className={styles.companyName}>{applicant.phone_number}</span>
                    <span className={styles.location}>{applicant.email}</span>
                  </div>
                </div>
                <button
                  className={styles.viewJobButton}
                  onClick={() => viewApplicant(applicant)}
                >
                  View Candidate
                </button>
              </div>
            ))}
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default EmployerLikedApplicants;
