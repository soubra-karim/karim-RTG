import { FunctionComponent } from "react";
import Navigation1 from "../components/Navigation1";
import CandidateProfile from "../components/CandidateProfile";
import styles from "./CandidateMyProfile.module.css";

const CandidateMyProfile = () => {
  return (
    <div className={styles.candidateSettingAccount}>
      <Navigation1 />
      <section className={styles.candidateSettingsWrapper}>
        <CandidateProfile />
      </section>
    </div>
  );
};

export default CandidateMyProfile;
