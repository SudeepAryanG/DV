"""This file creates api call for excelpage"""

# python modules
import datetime
import os

# third party modules
from flask import Blueprint, request, jsonify
import dask.dataframe as dd
import pandas as pd

# application modules
from model import Projects, InputFiles, db, Users, Projects
from utilities import handle_errors

# creating the blueprint for excel_page
excel_page = Blueprint("excel_page_api", __name__)


@excel_page.route("/api/v1/upload-csv", methods=["POST"])
@handle_errors
def upload_csv():
    """ 
    This function creates an API call
       for uploading csv to the storage

    Returns:
       It returns a JSON response for status of file uploaded
    """

    current_user = Users.query.order_by(Users.user_id.desc()).first()

    # Create a new project associated with the newly created user
    new_project = Projects(project_name="device-vision", user_id=current_user.user_id)
    db.session.add(new_project)
    db.session.commit()

    csv_file = request.files["file"]
    file_name = (
        str(new_project.project_id)+'_'
        + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        + ".csv"
    )
    os.makedirs('storage\\media_files\\actual_csv_files',exist_ok=True)
    current_csv_path = os.path.join(
        os.getcwd(), "storage\\media_files\\actual_csv_files", file_name
    )
    try:
        csv_file.save(current_csv_path)
        actual_csv = pd.DataFrame(pd.read_csv(current_csv_path))
        actual_csv.fillna('', inplace=True)
        actual_csv.to_csv(current_csv_path, index=False)

        input_file = InputFiles(
            file_path=current_csv_path, project_id=new_project.project_id
        )
        db.session.add(input_file)
        db.session.commit()
        

        return jsonify(
            {"error": None,"fileStatus":"sucesss", "projectId": new_project.project_id}
    )
    
    except Exception as error:
        
        return jsonify({"error": "file not saved in the storage"})

@excel_page.route("/api/v1/get-csv/<project_id>", methods=["GET"])
@handle_errors
def send_csv(project_id):
    """This api is for sending the csv file content 

    Args:
        project_id (int): The project id for the uploaded csv file

    Returns:
        _Json response with csv file content or error message
    """
   
    project = Projects.query.filter_by(project_id=project_id).first()
   
    if project:

        input_file = InputFiles.query.filter_by(project_id=project.project_id).first()
        
        try:
            actual_csv = pd.DataFrame(pd.read_csv(input_file.file_path))
            actual_csv.fillna('', inplace=True)
            df = actual_csv.to_dict(orient="records")
      
            return jsonify(
                {
                    "error": None,
                    "tableContent": df,
                    "columns": [column for column in actual_csv.columns],
                }
            ) 
            
        except Exception as error:
            return jsonify({{"error": "file not found folder"}})

    else:
        return jsonify({"error": "Invalid projectID"})


@excel_page.route("/api/v1/delete-projects", methods=["DELETE"])
@handle_errors
def delete_projects():
    """This API is for deleting projects and their associated CSV files

    The project_ids to be deleted should be provided in the request body as a list.

    Returns:
        _Json response with success message or error message
    """
    data = request.get_json()
    project_ids = data.get("project_ids")

    if not project_ids:
        return jsonify({"error": "No project_ids provided in the request body."})


    for project_id in project_ids:
        project = Projects.query.filter_by(project_id=project_id).first()
        if project:
           
            input_file = InputFiles.query.filter_by(project_id=project.project_id).first()
            if input_file:
               
                db.session.delete(input_file)

            # Delete the project
            db.session.delete(project)
        


    db.session.commit()
    return jsonify({"error":None, "message": "deleted successfully"})

