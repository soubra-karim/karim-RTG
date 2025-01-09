import React, { useEffect, useState } from "react";
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import Navigation2 from "../components/Navigation2";
import Footer from "../components/Footer";
import styles from './EmployerRecommendedCandidates.module.css';

type Job = {
  id: number;
  title: string;
  company_name?: string;
  location?: string;
  posted_date?: string;
  application_deadline?: string;
  experience_required?: string;
  job_description?: string;
  skills?: String[];
};

type LocationState = {
  job: Job;
};

type UserFields = {
  id: number;
  name: string;
  email: string;
  phone_number: string;
  score: string;
};

type UserResponse = {
  // pk: number;
  fields: UserFields;
};

type User = {
  id: number;
  name: string;
  email: string;
  phone_number: string;
  score: string;
};
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

name: string;
email?: string;
phone_number?: string;
skills?: Skill[];
educations?: Education[];
work_experiences?: WorkExperience[];
projects?: string[];

};

const EmployerRecommendedCandidates: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as LocationState;
  const token = localStorage.getItem('token');
  const [recommendedCandidates, setRecommendedCandidates] = useState<User[]>([]);
  const [applicant, setApplicant] = useState<Applicant | null>(null);
  const [isLoading, setIsLoading] = useState(true); // State to track loading status
  useEffect(() => {
    // This effect runs once on component mount
    window.scrollTo(0, 0);
  }, []); 
  useEffect(() => {
    console.log("Applicant state updated:", applicant);
  }, [applicant]);
  
  const {
    title,
    company_name,
    location: jobLocation,
    posted_date,
    application_deadline,
    experience_required,
    job_description,
    skills,
  } = state.job;

  useEffect(() => {
    const fetchRecommendedCandidates = async () => {
      try {
        const response = await fetch('http://localhost:8000/Recruiter/candidate-recommendations/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ job_id: jobId }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const jsonResponse = await response.json();
        console.log("printing")
        console.log(jsonResponse)

        const usersArray: UserFields[] = jsonResponse.recommended_users;
        console.log(usersArray)

        const users = usersArray.map(fields => ({
          
          id: fields.id,
          name: fields.name,
          email: fields.email,
          phone_number: fields.phone_number,
          score: fields.score
        }));
        setRecommendedCandidates(users);
        console.log(recommendedCandidates)
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching recommended candidates:', error);
      }
    };

    if (jobId && token) {
      fetchRecommendedCandidates();
    }
  }, [jobId, token]);
  
  const viewapplicant = async (user: User) => {
    try {
      // Assuming 'applicant.id' is the ID of the user you want to fetch details for
      // and 'http://localhost:8000/user-info/' is the endpoint to your Django view.
      const response = await fetch(`http://localhost:8000/Recruiter/display_user_info/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: user.id }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("data",data)
      setApplicant(data)
      
      // If you want to navigate to the candidate page and pass the user info
      navigate(`/recommended-candidate/${user.id}`, { state: { applicant: data,confidence_rating : user.score } });

    } catch (error) {
      console.error('Error fetching user details:', error);
      // Handle any additional error logic here, such as showing a notification to the user
    }
  };

  const handleLike = async (userId: any) => {
    try {
      console.log('Token:', token);
      console.log(jobId);
      const response = await fetch('http://localhost:8000/Recruiter/update_feedback/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, job_id: jobId, feedback: '1' }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      window.location.reload();
      const data = await response.json();
      console.log('Like response:', data);
    } catch (error) {
      console.error('Error sending like:', error);
    }
  };


  const handleDislike = async (userId: any) => {
    try {
      const response = await fetch('http://localhost:8000/Recruiter/update_feedback/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, job_id: jobId, feedback: '-1' }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      window.location.reload();
      const data = await response.json();
      console.log('Dislike response:', data);
    } catch (error) {
      console.error('Error sending dislike:', error);
    }
  };

  const LoadingIcon = () => (
    <div className={styles.loadingContainer}>
      <div className={styles.categoryIconGroup}>
        <div className={styles.sitelogo}>
          <div className={styles.digitalMarketing} />
          <div className={styles.digitalMarketing1} />
          <div className={styles.digitalMarketing2} />
          <div className={styles.sitelogo1} />
        </div>
        <h3 className={styles.jobsync}>JobSync</h3>
    </div>
    <h2 className={styles.loadingHeading}>Please wait while we find the perfect candidates!</h2>
  </div>
  );


  return (
    <div className={styles.jobPage}>
      <Navigation2 />
  
      <div className={styles.jobContent}>
        {/* Left Column for Job Details */}
        <div className={styles.jobDetailColumn}>
          <div className={styles.jobDetailHeader}>
            <h1 className={styles.jobTitle}>{title}</h1>
            {company_name && <p className={styles.jobCompany}>{company_name}</p>}
            {jobLocation && <p className={styles.jobLocation}>{jobLocation}</p>}
          </div>
          <div className={styles.jobDescriptionSection}>
            <h2 className={styles.sectionTitle}>Job Overview</h2>
            <div className={styles.jobOverviewContainer}>
              <div className={styles.jobPosted}>
                <img src="/calendarblank.svg" alt="Calendar Icon" className={styles.icon} />
                <div className={styles.textContainer}>
                  <span className={styles.subHeading}>JOB POSTED:</span>
                  <span className={styles.date}>{posted_date && new Date(posted_date).toLocaleDateString()}</span>
                </div>
              </div>
              <div className={styles.jobExpire}>
                <img src="/timer.svg" alt="Timer Icon" className={styles.icon} />
                <div className={styles.textContainer}>
                  <span className={styles.subHeading}>JOB EXPIRE IN:</span>
                  <span className={styles.date}>{application_deadline && new Date(application_deadline).toLocaleDateString()}</span>
                </div>
              </div>
              <div className={styles.experience}>
                <img src="/briefcase.svg" alt="Briefcase Icon" className={styles.icon} />
                <div className={styles.textContainer}>
                  <span className={styles.subHeading}>EXPERIENCE:</span>
                  <span className={styles.experienceLevel}>{experience_required}</span>
                </div>
              </div>
            </div>
          </div>
          <div className={styles.jobDescriptionSection}>
            <h2 className={styles.sectionTitle}>Skills</h2>
            {skills && skills.length > 0 ? (
              <div className={styles.skillsContainer}> {/* Change from <ul> to <div> */}
                {skills.map((skill, index) => (
                  <span key={index} className={styles.skillBox}> {/* Change from <li> to <span> */}
                    {skill}
                  </span>
                ))}
              </div>
            ) : (
              <p>No skills information provided.</p>
            )}
          </div>
          <div className={styles.jobDescriptionSection}>
            <h2 className={styles.sectionTitle}>Description</h2>
            {job_description && (
              <div className={styles.jobDescriptionContent}>
                {/* First split by new lines, then map and check each line for bullets or dashes */}
                {job_description.split(/\r\n|\r|\n/).map((line, lineIndex) => {
                  // Then split by the pattern that detects standalone bullets or dashes
                  return line.split(/(•|-| -) /).map((text, textIndex, array) => {
                    // Check if the text is a bullet or dash, and not an empty string
                    if (text === '•' || text === '-' || text === '-') {
                      // The next item in the array will be the text after bullet/dash
                      // Return null for the bullet/dash, as we will add it before the actual text item
                      return null;
                    } else {
                      // If the previous item was a bullet/dash, prepend it to this text
                      const bulletOrDash = array[textIndex - 1] === '•' || array[textIndex - 1] === '-' ? array[textIndex - 1] + ' ' : '';
                      return (
                        <div key={`${lineIndex}-${textIndex}`} className={styles.jobDescriptionListItem}>
                          {bulletOrDash}{text}
                        </div>
                      );
                    }
                  });
                })}
              </div>
            )}
          </div>
        </div>
        <div className={styles.additionalContentColumn}>
          {isLoading ? (

            <LoadingIcon />
            
          ) : (
            <>
              <h2 className={styles.recommendationsHeading}>Candidates you might like...</h2>
              {recommendedCandidates.map((user) => (
                <div key={user.id} className={styles.candidateCard}>
                  <div className={styles.candidateDetails}>
                    <h2 className={styles.candidateName}>{user.name}</h2>
                    <p className={styles.candidatePhoneNumber}>{user.phone_number}</p>
                    <p className={styles.candidateEmail}>{user.email}</p>
                    {/* <p className={styles.candidateEmail}>{user.score}</p> */}
                  </div>
                  {/* New container for all action buttons */}
                  <div className={styles.actionButtons}>
                    {/* Like and Dislike buttons */}
                    <div className={styles.interactionIcons}>
                      <button className={styles.likeButton} onClick={() => handleLike(user.id)}>
                        <img
                          className={styles.thumbsupIcon}
                          loading="lazy"
                          alt="Like"
                          src="/thumbsup.svg"
                        />
                      </button>
                      <button className={styles.dislikeButton} onClick={() => handleDislike(user.id)}>
                        <img
                          className={styles.thumbsdownIcon}
                          loading="lazy"
                          alt="Dislike"
                          src="/thumbsdown.svg"
                        />
                      </button>
                    </div>
                    <button
                      className={styles.viewCandidateButton}
                      onClick={() => viewapplicant(user)}
                    >
                      View Candidate
                    </button>
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
  
      <Footer />
    </div>
  );
  
  
  
  
};

export default EmployerRecommendedCandidates;
