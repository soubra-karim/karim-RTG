import { FunctionComponent } from "react";
import Navigation3 from "../components/Navigation3";
import CreateFrame from "../components/CreateFrame";
import styles from "./CreateAccount.module.css";

const CreateAccount: FunctionComponent = () => {
  return (
    <div className={styles.candidateCreateAccount}>
      <Navigation3 />
      <CreateFrame />
    </div>
  );
};

export default CreateAccount;
