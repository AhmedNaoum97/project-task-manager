from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Task
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks")


@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    # Create a new task
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate input
        if not data or not data.get("title"):
            return jsonify({"error": "Title is required"}), 400

        # Create task
        task = Task(
            user_id=user_id,
            title =data["title"],
            description =data.get("description"),
            priority=data.get("priority", "medium"),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": task.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tasks_bp.route("/<task_id>", methods=["GET"])
@jwt_required()
def get_task( task_id):
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tasks_bp.route("/<task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """Update task"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()

        if not task:
            return jsonify({"error": "Task not found"}), 404

        data = request.get_json()

        # Update fields
        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "priority" in data:
            task.priority = data["priority"]
        if "status" in data:
            task.status = data["status"]
            if data["status"] == "completed" and not task.completed_at:
                task.completed_at = datetime.utcnow()
        if "due_date" in data:
            task.due_date = datetime.fromisoformat(data["due_date"]) if data["due_date"] else None

        task.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "success": True,
            "data": task.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


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
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500