import type { Task } from '../types/task';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
  onStatusChange: (id: string, status: Task['status']) => void;
}

const priorityStyles = {
  low: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
  medium: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
  high: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
};

const statusStyles = {
  pending: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
  in_progress: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
  completed: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
};

const statusLabels = {
  pending: 'Pending',
  in_progress: 'In Progress',
  completed: 'Completed',
};

export const TaskCard = ({ task, onEdit, onDelete, onStatusChange }: TaskCardProps) => {
  const isCompleted = task.status === 'completed';

  const handleStatusToggle = () => {
    if (task.status === 'completed') {
      onStatusChange(task.id, 'pending');
    } else if (task.status === 'pending') {
      onStatusChange(task.id, 'in_progress');
    } else {
      onStatusChange(task.id, 'completed');
    }
  };

  return (
    <div className={`bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-5 flex flex-col gap-3 shadow-sm hover:shadow-md transition-shadow ${isCompleted ? 'opacity-60' : ''}`}>
      
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <h3 className={`font-semibold text-gray-900 dark:text-gray-100 text-base leading-tight ${isCompleted ? 'line-through' : ''}`}>
          {task.title}
        </h3>
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={() => onEdit(task)}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-sm transition-colors"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="text-gray-400 hover:text-red-500 text-sm transition-colors"
          >
            Delete
          </button>
        </div>
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-gray-500 dark:text-gray-400 text-sm leading-relaxed">
          {task.description}
        </p>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between gap-2 mt-1">
        <div className="flex items-center gap-2">
          <span className={`text-xs font-medium px-2 py-1 rounded-full ${priorityStyles[task.priority]}`}>
            {task.priority}
          </span>
          <span className={`text-xs font-medium px-2 py-1 rounded-full ${statusStyles[task.status]}`}>
            {statusLabels[task.status]}
          </span>
        </div>

        <div className="flex items-center gap-3">
          {task.due_date && (
            <span className="text-xs text-gray-400 dark:text-gray-500">
              Due {new Date(task.due_date).toLocaleDateString()}
            </span>
          )}
          <button
            onClick={handleStatusToggle}
            className="text-xs text-purple-600 dark:text-purple-400 hover:underline transition-colors"
          >
            {task.status === 'completed' ? 'Reopen' : task.status === 'pending' ? '→ In Progress' : '→ Complete'}
          </button>
        </div>
      </div>
    </div>
  );
};