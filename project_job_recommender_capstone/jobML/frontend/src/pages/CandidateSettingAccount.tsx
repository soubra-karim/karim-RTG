import { FunctionComponent } from "react";
import Navigation1 from "../components/Navigation1";
import CandidateSettings1 from "../components/CandidateProfile";
import styles from "./CandidateSettingAccount.module.css";

const CandidateSettingAccount: FunctionComponent = () => {
  return (
    <div className={styles.candidateSettingAccount}>
      <Navigation1 />
      <section className={styles.candidateSettingsWrapper}>
        <CandidateSettings1 />
      </section>
    </div>
  );
};

export default CandidateSettingAccount;
