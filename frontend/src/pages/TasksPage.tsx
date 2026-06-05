import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { taskService } from '../services/api';
import { TaskCard } from '../components/TaskCard';
import { TaskForm } from '../components/TaskForm';
import type { Task, CreateTaskPayload, UpdateTaskPayload } from '../types/task';

export const TasksPage = () => {
    const { logout } = useAuth();

    const [tasks, setTasks] = useState<Task[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedTask, setSelectedTask] = useState<Task | null>(null);
    const [statusFilter, setStatusFilter] = useState('');
    const [priorityFilter, setPriorityFilter] = useState('');

    const fetchTasks = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await taskService.getTasks(statusFilter, priorityFilter);
            setTasks(response.data.data);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to fetch tasks');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchTasks();
    }, [statusFilter, priorityFilter]);

    const handleCreate = async (data: CreateTaskPayload | UpdateTaskPayload) => {
        setIsLoading(true);
        try {
            const response = await taskService.createTask(data as CreateTaskPayload);
            setTasks(prev => [response.data.data, ...prev]);
            setIsModalOpen(false);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to create task');
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (id: string) => {
        try {
            await taskService.deleteTask(id);
            setTasks(prev => prev.filter(t => t.id !== id));
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to delete task');
        }
    };

    const handleUpdate = async (data: CreateTaskPayload | UpdateTaskPayload) => {
        if (!selectedTask) return;
        setIsLoading(true);
        try {
            const response = await taskService.updateTask(selectedTask.id, data as UpdateTaskPayload);
            setTasks(prev => prev.map(t => t.id === selectedTask.id ? response.data.data : t));
            setIsModalOpen(false);
            setSelectedTask(null);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to update task');
        } finally {
            setIsLoading(false);
        }
    };

    const handleStatusChange = async (id: string, status: Task['status']) => {
        try {
            const response = await taskService.updateTask(id, { status });
            setTasks(prev => prev.map(t => t.id === id ? response.data.data : t));
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to update status');
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950">

            {/* Navbar */}
            <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex items-center justify-between">
                <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Task Manager</h1>
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => { setSelectedTask(null); setIsModalOpen(true); }}
                        className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition"
                    >
                        + New Task
                    </button>
                    <button
                        onClick={logout}
                        className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition"
                    >
                        Logout
                    </button>
                </div>
            </nav>

            <div className="max-w-4xl mx-auto px-6 py-8 flex flex-col gap-6">

                {/* Filters */}
                <div className="flex gap-3 flex-wrap">
                    <select
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                        className="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                    >
                        <option value="">All Statuses</option>
                        <option value="pending">Pending</option>
                        <option value="in_progress">In Progress</option>
                        <option value="completed">Completed</option>
                    </select>

                    <select
                        value={priorityFilter}
                        onChange={(e) => setPriorityFilter(e.target.value)}
                        className="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                    >
                        <option value="">All Priorities</option>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>

                {/* Error */}
                {error && (
                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
                        {error}
                    </div>
                )}

                {/* Task List */}
                {isLoading && tasks.length === 0 ? (
                    <div className="text-center text-gray-400 py-12">Loading...</div>
                ) : tasks.length === 0 ? (
                    <div className="text-center text-gray-400 py-12">
                        No tasks yet. Create your first one.
                    </div>
                ) : (
                    <div className="flex flex-col gap-3">
                        {tasks.map(task => (
                            <TaskCard
                                key={task.id}
                                task={task}
                                onEdit={(task) => { setSelectedTask(task); setIsModalOpen(true); }}
                                onDelete={handleDelete}
                                onStatusChange={handleStatusChange}
                            />
                        ))}
                    </div>
                )}
            </div>

            {/* Modal */}
            {isModalOpen && (
                <TaskForm
                    task={selectedTask}
                    onSubmit={selectedTask ? handleUpdate : handleCreate}
                    onClose={() => { setIsModalOpen(false); setSelectedTask(null); }}
                    isLoading={isLoading}
                />
            )}
        </div>
    );
};