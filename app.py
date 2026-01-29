"""Employee Management System - Flask API."""

from flask import Flask, request, jsonify

from employees_manager import (
    create_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee,
    ValidationError,
    NotFoundError,
    UniqueConstraintError,
)

app = Flask(__name__)


# Helper function to format error response
def error_response(errors, status_code):
    """Format error response."""
    if isinstance(errors, dict):
        return jsonify({"errors": errors}), status_code
    return jsonify({"error": str(errors)}), status_code


# CREATE - Add new employee
@app.route("/employees", methods=["POST"])
def create_employee_endpoint():
    """Create a new employee."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        employee = create_employee(data)
        return jsonify(employee.to_dict()), 201
    
    except ValidationError as e:
        return error_response(e.args[0], 400)
    except UniqueConstraintError as e:
        return error_response(e.args[0], 409)
    except Exception as e:
        return error_response(str(e), 500)


# READ - Get all employees
@app.route("/employees", methods=["GET"])
def get_employees_endpoint():
    """Get all employees with pagination support."""
    try:
        limit = request.args.get("limit", default=100, type=int)
        offset = request.args.get("offset", default=0, type=int)
        
        # Validate pagination parameters
        if limit < 1:
            limit = 100
        if offset < 0:
            offset = 0
        
        employees = get_all_employees(limit, offset)
        return jsonify({
            "employees": [emp.to_dict() for emp in employees],
            "count": len(employees),
        }), 200
    
    except Exception as e:
        return error_response(str(e), 500)


# READ - Get single employee by ID
@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee_endpoint(employee_id):
    """Get a single employee by ID."""
    try:
        employee = get_employee_by_id(employee_id)
        return jsonify(employee.to_dict()), 200
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


# UPDATE - Update employee
@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee_endpoint(employee_id):
    """Update an employee (partial update allowed)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        employee = update_employee(employee_id, data)
        return jsonify(employee.to_dict()), 200
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except ValidationError as e:
        return error_response(e.args[0], 400)
    except UniqueConstraintError as e:
        return error_response(e.args[0], 409)
    except Exception as e:
        return error_response(str(e), 500)


# DELETE - Delete employee
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee_endpoint(employee_id):
    """Delete an employee by ID."""
    try:
        result = delete_employee(employee_id)
        return jsonify(result), 200
    
    except NotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


# HTML View - Display employees in readable table format
@app.route("/", methods=["GET"])
@app.route("/employees-view", methods=["GET"])
def employees_view():
    """Display all employees in HTML table format."""
    try:
        employees = get_all_employees(limit=1000)
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Employee Management System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    border-bottom: 2px solid #007bff;
                    padding-bottom: 10px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th {
                    background-color: #007bff;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                }
                td {
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }
                tr:hover {
                    background-color: #f9f9f9;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .no {
                    font-weight: bold;
                    color: #007bff;
                    width: 50px;
                }
                .empty {
                    text-align: center;
                    color: #999;
                    padding: 40px;
                }
                .footer {
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #666;
                    font-size: 12px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>👥 Employee Management System</h1>
                <p>Total Employees: <strong>""" + str(len(employees)) + """</strong></p>
        """
        
        if employees:
            html += """
                <table>
                    <thead>
                        <tr>
                            <th class="no">No.</th>
                            <th>ID</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Email</th>
                            <th>Position</th>
                            <th>Salary</th>
                            <th>Created At</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for idx, emp in enumerate(employees, 1):
                html += f"""
                        <tr>
                            <td class="no">{idx}</td>
                            <td>{emp.id}</td>
                            <td>{emp.first_name}</td>
                            <td>{emp.last_name}</td>
                            <td>{emp.email}</td>
                            <td>{emp.position}</td>
                            <td>R{emp.salary:,.2f}</td>
                            <td>{emp.created_at}</td>
                        </tr>
                """
            
            html += """
                    </tbody>
                </table>
            """
        else:
            html += '<div class="empty"><p>No employees found. Start by creating one!</p></div>'
        
        html += """
                <div class="footer">
                    <p>📍 API Endpoints:</p>
                    <ul>
                        <li>POST /employees - Create employee</li>
                        <li>GET /employees - Get all (JSON)</li>
                        <li>GET /employees/{id} - Get single employee</li>
                        <li>PUT /employees/{id} - Update employee</li>
                        <li>DELETE /employees/{id} - Delete employee</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        return html, 200, {'Content-Type': 'text/html; charset=utf-8'}
    
    except Exception as e:
        return error_response(str(e), 500)


if __name__ == "__main__":
    print("Starting Employee Management System...")
    print("API running at http://localhost:5000")
    print("Database: employees.db")
    app.run(debug=False, host="127.0.0.1", port=5000)
    