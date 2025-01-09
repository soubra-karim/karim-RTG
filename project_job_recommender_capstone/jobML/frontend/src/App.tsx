import { useEffect } from "react";
import {
  Routes,
  Route,
  useNavigationType,
  useLocation,
} from "react-router-dom";
import SignIn from "./pages/SignIn";
import JobPage from "./pages/JobPage";
import CandidateHomepage from "./pages/CandidateHomepage";
import CandidateMyProfile from "./pages/CandidateMyProfile";
import CandidateSearchPage from "./pages/CandidateSearchPage";
import CandidateFavoriteJobs from "./pages/CandidateFavoriteJobs";
import CandidateSettingAccount from "./pages/CandidateSettingAccount";
import EmployerHomepage from "./pages/EmployerHomepage";
import EmployerLikedApplicants from "./pages/EmployerLikedApplicants";
import EmployerSearchPage from "./pages/EmployerSearchPage";
import CreateAccount from "./pages/CreateAccount";
import EmployerCreateAccount from "./pages/EmployerCreateAccount";
import ResumeUpload from "./pages/ResumeUpload";
import EmployerCreateJob from "./pages/EmployerCreateJob";
import CandidatePage from "./pages/candidatepage";
import EmployerRecommendedCandidates from "./pages/EmployerRecommendedCandidates";
import EmployerMyProfile from "./pages/EmployerMyProfile";
import EditJobPage from "./pages/EditJobPage";
import FeaturedJobsPage from "./pages/FeaturedJobsPage";
import CandidateStats from "./pages/CandidateStats";
import RecommendedCandidate from "./pages/RecommendedCandidate";
import EmployerStats from "./pages/EmployerStats"

function App() {
  const action = useNavigationType();
  const location = useLocation();
  const pathname = location.pathname;

  useEffect(() => {
    if (action !== "POP") {
      window.scrollTo(0, 0);
    }
  }, [action, pathname]);

  useEffect(() => {
    let title = "";
    let metaDescription = "";

    switch (pathname) {
      case "/":
        title = "";
        metaDescription = "";
        break;
      case "/job/:jobId":
        title = "";
        metaDescription = "";
        break;
      case "/candidatepage/:user_id":
          title = "";
          metaDescription = "";
          break;
      case "/recommended-candidate/:user_id":
        title = "";
        metaDescription = "";
        break;
      case "/featured-jobs-page":
        title=""
        metaDescription=""
        break;
      case "/candidate-homepage":
        title = "";
        metaDescription = "";
        break;
      case "/candidate-my-profile":
        title = "";
        metaDescription = "";
        break;
      case "/candidate-search-page":
        title = "";
        metaDescription = "";
        break;
      case "/candidate-favorite-jobs":
        title = "";
        metaDescription = "";
        break;
      case "/employer-homepage":
        title = "";
        metaDescription = "";
        break;
      case "/employer-search-page":
        title = "";
        metaDescription = "";
        break;
        case "/recommended-candidates":
        title = "";
        metaDescription = "";
        break;
      case "/candidate-create-account":
        title = "";
        metaDescription = "";
        break;
      case "/employer-create-account":
       title = "";
        metaDescription = "";
        break;
        case "/create-job":
        title = "";
        metaDescription = "";
        break;
      case "/resume-upload":
        title = "";
        metaDescription = "";
        break;
      case "/employer-liked-applicants":
        title = "";
        metaDescription = "";
        break;
      case "/edit-job/:jobId":
        title = "";
        metaDescription = "";
        break;
      case "/candidate-stats":
        title = "";
        metaDescription = "";
        break;
      case "/employer-stats":
        title = "";
        metaDescription = "";
        break;
      case "/employer-my-profile":
        title = "";
        metaDescription = "";
        break;
    }
    
    if (title) {
      document.title = title;
    }

    if (metaDescription) {
      const metaDescriptionTag: HTMLMetaElement | null = document.querySelector(
        'head > meta[name="description"]'
      );
      if (metaDescriptionTag) {
        metaDescriptionTag.content = metaDescription;
      }
    }
  }, [pathname]);

  return (
    <Routes>
      <Route path="/" element={<SignIn />} />
      <Route path="/job/:jobId" element={<JobPage />} />
      <Route path="/candidate-homepage" element={<CandidateHomepage />} />
      <Route path="/candidate-my-profile" element={<CandidateMyProfile />} />
      <Route path="/candidate-search-page" element={<CandidateSearchPage />} />
      <Route path="/candidate-stats" element={<CandidateStats />} />
      <Route path="/employer-stats" element={<EmployerStats />} />
      <Route path="/candidatepage/:user_id" element={<CandidatePage />} />
      <Route path="/recommended-candidate/:user_id" element={<RecommendedCandidate />} />
      <Route path="/featured-jobs-page/" element={<FeaturedJobsPage />} />

      <Route path="/candidate-liked-jobs" element={<CandidateFavoriteJobs />} />
      <Route path="/candidate-setting-account" element={<CandidateSettingAccount />} />
      <Route path="/employer-homepage" element={<EmployerHomepage />} />
      <Route path="/employer-liked-applicants" element={<EmployerLikedApplicants />} />

      <Route path="/employer-my-profile" element={<EmployerMyProfile />} />
      <Route path="/edit-job/:jobId" element={<EditJobPage />} />
      <Route path="/employer-my-profile" element={<EmployerMyProfile />} />
      <Route path="/employer-search-page" element={<EmployerSearchPage />} />
      <Route path="/create-job" element={<EmployerCreateJob />} />
      <Route path="/recommended-candidates/:jobId" element={<EmployerRecommendedCandidates />} />
      <Route path="/candidate-create-account" element={<CreateAccount />} />
      <Route path="/resume-upload" element={<ResumeUpload />} />
      <Route path="/employer-create-account" element={<EmployerCreateAccount />} />
    </Routes>
  );
}
export default App;
