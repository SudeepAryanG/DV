/**
 * Project Component
 *
 * The Project component is a React functional component that represents a project page
 * with an Excel table.
 * @returns {JSX.Element} The rendered Project element.
 */

//React Imports
import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
//Imports from Reusables
import Table from "../../Components/Reusables/Table/table";
import { useNotification } from "../../Components/Reusables/Notification/Notification";
//Redux Imports
import { useSelector } from "react-redux";
import { useLazyGetExcelQuery } from "../../Redux/ProjectPage/ProjectRtkQuery";
import { rootSelector } from "../../Redux/Root/rootSelector";

const Project = () => {
  const columns = useSelector(rootSelector.Project.projectData.tableColumns);
  const tableData = useSelector(rootSelector.Project.projectData.tableData);
  const notification = useNotification();
  const location = useLocation();
  const [getExcel, getData] = useLazyGetExcelQuery() || {};
  const error = useSelector(rootSelector.Project.projectData.error);
  console.log(error);
  /**
   * useEffect Hook
   * This hook is used to fetch Excel data based on the current path when the component mounts.
   */

  useEffect(() => {
    const path = location.pathname.split("/")[2];
    getExcel(path);
  }, []);

  if (getData.data) {
    if (error !== null && getData.data.error !== null)
      notification.openNotification("Error", error, "error");
    if (error === null && getData.data.error === null)
      notification.openNotification(
        "Success",
        "Project Fetched Successfully",
        "success"
      );
  }

  return (
    <div>
      <div>
        <Table columns={columns} tableData={tableData} />
      </div>
    </div>
  );
};

export default Project;
