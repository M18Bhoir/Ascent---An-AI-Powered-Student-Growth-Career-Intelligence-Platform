import { useAuth } from "../../context/AuthContext";

export default function StudentDashboard() {
  const { user, logout } = useAuth();

  return (
    <main className="min-h-screen bg-slate-950 p-8 text-white">
      <div className="mx-auto max-w-5xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm text-indigo-400">ASCENT / STUDENT</p>
            <h1 className="mt-2 text-3xl font-bold">Student Dashboard</h1>
            <p className="mt-2 text-slate-400">Welcome, {user.email}</p>
          </div>

          <button
            onClick={logout}
            className="rounded-lg border border-slate-700 px-4 py-2 hover:bg-slate-800"
          >
            Sign out
          </button>
        </div>

        <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-xl font-semibold">Your growth journey</h2>
          <p className="mt-2 text-slate-400">
            Authentication is working. Skills, achievements, analytics, and
            career recommendations will be added in later phases.
          </p>
          <p className="mt-4 text-sm text-slate-500">Role: {user.role}</p>
        </section>
      </div>
    </main>
  );
}
