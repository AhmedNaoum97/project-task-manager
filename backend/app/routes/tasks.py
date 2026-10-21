from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Task
from datetime import datetime
from pydantic import ValidationError
from ..schemas import TaskCreate, TaskUpdate


tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks")


@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    # Create a new task
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)

        # Validate input
        try:
            payload = TaskCreate.model_validate(data)
        except ValidationError as e:
            return jsonify({"error": "Invalid input",
                            "details": e.errors(include_url=False, include_input=False, include_context=False)}), 400
        # Create task
        task = Task(user_id=user_id, **payload.model_dump())

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": task.to_dict()
        }), 201

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Unhandled error in create_task")
        return jsonify({"error": "Internal server error"}), 500


@tasks_bp.route("", methods=["GET"])
@jwt_required()
def get_tasks():
    """Get all tasks for authenticated user"""
    try:
        user_id = get_jwt_identity()

        # Query filters
        status = request.args.get("status")
        priority = request.args.get("priority")

        query = Task.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)

        tasks = query.all()

        return jsonify({
            "success": True,
            "data": [task.to_dict() for task in tasks]
        }), 200

    except Exception:
        current_app.logger.exception("Unhandled error in get_tasks")
        return jsonify({"error": "Internal server error"}), 500


@tasks_bp.route("/<task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    """Get single task"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({
            "success": True,
            "data": task.to_dict()
        }), 200

    except Exception:
        current_app.logger.exception("Unhandled error in get_task")
        return jsonify({"error": "Internal server error"}), 500


@tasks_bp.route("/<task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """Update task"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "Invalid input"}), 400

        try:
            payload = TaskUpdate.model_validate(data)
        except ValidationError as e:
            return jsonify({"error": "Invalid input", "details": e.errors(include_url=False, include_input=False, include_context=False)}), 400

        # Update fields
        # Update fields
        updates = payload.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(task, field, value)

        if updates.get("status") == "completed" and not task.completed_at:
            task.completed_at = datetime.utcnow()
            
        task.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "success": True,
            "data": task.to_dict()
        }), 200

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Unhandled error in update_task")
        return jsonify({"error": "Internal server error"}), 500


@tasks_bp.route("/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """Delete task"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Task deleted successfully",
        }), 200

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Unhandled error in delete_task")
        return jsonify({"error": "Internal server error"}), 500