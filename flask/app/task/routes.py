from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.task import taskBp
from app.extention import db
from app.models.task import Tasks
from prometheus_flask_exporter import Counter

get_task_counter = Counter('get_task_total', 'Number of task retrievals')
create_task_counter = Counter('create_task_total', 'Number of tasks created')
update_task_counter = Counter('update_task_total', 'Number of tasks updated')
delete_task_counter = Counter('delete_task_total', 'Number of tasks deleted')



@taskBp.route('/', strict_slashes=False)
@jwt_required(locations=["headers"])
def get_tasks():
    current_user = int(get_jwt_identity())  
    tasks = db.session.query(Tasks).filter(Tasks.user_id == current_user)
    result = [task.serialize() for task in tasks]

    get_task_counter.inc()
    return jsonify({"data": result}), 200



@taskBp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required(locations=["headers"])
def create_task():
    data = request.get_json()
    user_id = int(get_jwt_identity())  
    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")
    is_done = data.get("is_done")
    project_id = data.get("project_id")

    if not title or not user_id or not project_id or not due_date:
        return jsonify({'message': 'incomplete data'}), 422

    new_task = Tasks(
        title=title,
        description=description,
        due_date=due_date,
        is_done=is_done,
        user_id=user_id,
        project_id=project_id
    )

    db.session.add(new_task)
    db.session.commit()
    create_task_counter.inc()

    return jsonify({
        "success": True,
        "message": 'New task created!',
        "data": new_task.serialize()
    }), 200


@taskBp.route('/<task_id>', methods=["PUT"], strict_slashes=False)
@jwt_required(locations=["headers"])
def update_task(task_id):
    data = request.get_json()
    current_user = int(get_jwt_identity())  

    task = Tasks.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"success": False, "message": f'there is no task with id {task_id}'}), 404

    if current_user != task.user_id:
        return jsonify({"message": 'You do not have permission to edit this task'}), 403

    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")
    is_done = data.get("is_done")
    project_id = data.get("project_id")

    if not title or not project_id or not due_date or is_done is None:
        return jsonify({'message': 'incomplete data'}), 422

    task.title = title
    task.description = description
    task.due_date = due_date
    task.is_done = is_done
    task.user_id = current_user
    task.project_id = project_id

    db.session.commit()
    update_task_counter.inc()

    return jsonify({
        "success": True,
        "message": f'task with id {task_id} has been changed',
        "data": task.serialize()
    }), 200



@taskBp.route('/<task_id>', methods=["DELETE"], strict_slashes=False)
@jwt_required(locations=["headers"])
def delete_task(task_id):
    current_user = int(get_jwt_identity())  

    task = Tasks.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({
            "success": False,
            "message": f'there is no task with id {task_id}'
        }), 404

    if current_user != task.user_id:
        return jsonify({
            "message": 'You do not have permission to delete this task'
        }), 403

    db.session.delete(task)
    db.session.commit()
    delete_task_counter.inc()

    return jsonify({
        "success": True,
        "message": f'task with id {task_id} is successfully deleted'
    }), 200
