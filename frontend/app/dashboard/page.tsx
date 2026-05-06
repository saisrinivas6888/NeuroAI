"use client"

import Link from "next/link"
import { signOut, useSession } from "next-auth/react"

export default function Dashboard() {

  const { data: session } = useSession()

  return (
    <main className="min-h-screen relative overflow-hidden text-white px-14 py-10">

      {/*  BACKGROUND */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-purple-950 via-black to-cyan-950 opacity-90" />

      <div className="absolute w-[700px] h-[700px] bg-purple-600 blur-[220px] opacity-20 top-[-200px] left-[-150px] rounded-full animate-pulse" />

      <div className="absolute w-[600px] h-[600px] bg-cyan-500 blur-[220px] opacity-20 bottom-[-200px] right-[-150px] rounded-full animate-pulse" />

      {/*  PAGE WRAPPER */}
      <div className="animate-fadeIn">

        {/*  TOP BAR */}
        <div className="flex justify-between items-center mb-20">

          <div>

            <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-400 to-cyan-400 text-transparent bg-clip-text drop-shadow-[0_0_25px_rgba(139,92,246,0.5)]">
              NeuroAI
            </h1>

            <p className="text-gray-400 mt-2 text-lg">
              EEG Intelligence Platform
            </p>

          </div>

          <div className="flex items-center gap-6">

            <div className="text-right">
              <p className="text-sm text-gray-500">
                Logged in as
              </p>

              <p className="text-lg text-white font-medium">
                Dr. {session?.user?.name || "User"}
              </p>
            </div>

            <button
            onClick={() =>
                signOut({
                     callbackUrl: "/"
                 })
               }
              className="px-6 py-3 border border-white/10 rounded-2xl bg-white/5 hover:bg-white/10 hover:border-cyan-400 transition-all duration-300 hover:shadow-[0_0_30px_rgba(0,255,255,0.2)]"
            >
              Logout
            </button>

          </div>

        </div>

        {/* 🏷 TITLE */}
        <div className="mb-16">

          <h2 className="text-7xl font-black leading-tight bg-gradient-to-r from-purple-300 via-purple-400 to-cyan-400 text-transparent bg-clip-text drop-shadow-[0_0_20px_rgba(139,92,246,0.4)]">
            Dashboard
          </h2>

          <p className="text-gray-400 mt-4 text-xl max-w-2xl">
            Advanced AI-powered EEG workflow for preprocessing,
            neural analysis, patient management, and prediction tracking.
          </p>

        </div>

        {/*  GRID */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-8">

          {/* Upload */}
          <Link href="/upload">

            <div
              style={{ animationDelay: "0.1s" }}
              className="animate-fadeIn group p-10 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-2xl cursor-pointer transition-all duration-500 hover:-translate-y-3 hover:scale-[1.03] hover:border-cyan-400 hover:shadow-[0_25px_70px_rgba(0,255,255,0.18)]"
            >

              <div className="mb-8 text-5xl">
                
              </div>

              <h3 className="text-3xl font-bold group-hover:text-cyan-300 transition">
                Upload EEG
              </h3>

              <p className="text-gray-400 mt-4 text-base leading-relaxed">
                Upload EEG recordings and prepare patient data for AI analysis.
              </p>

            </div>

          </Link>

          {/* Preprocess */}
          <Link href="/preprocess">

            <div
              style={{ animationDelay: "0.2s" }}
              className="animate-fadeIn group p-10 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-2xl cursor-pointer transition-all duration-500 hover:-translate-y-3 hover:scale-[1.03] hover:border-purple-400 hover:shadow-[0_25px_70px_rgba(168,85,247,0.18)]"
            >

              <div className="mb-8 text-5xl">
                
              </div>

              <h3 className="text-3xl font-bold group-hover:text-purple-300 transition">
                Preprocess
              </h3>

              <p className="text-gray-400 mt-4 text-base leading-relaxed">
                Generate neural connectivity matrices and preprocess EEG signals.
              </p>

            </div>

          </Link>

          {/* Patients */}
          <Link href="/patients">

            <div
              style={{ animationDelay: "0.3s" }}
              className="animate-fadeIn group p-10 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-2xl cursor-pointer transition-all duration-500 hover:-translate-y-3 hover:scale-[1.03] hover:border-pink-400 hover:shadow-[0_25px_70px_rgba(236,72,153,0.18)]"
            >

              <div className="mb-8 text-5xl">
                
              </div>

              <h3 className="text-3xl font-bold group-hover:text-pink-300 transition">
                Patients
              </h3>

              <p className="text-gray-400 mt-4 text-base leading-relaxed">
                Manage patient profiles, scan history, and AI diagnostic records.
              </p>

            </div>

          </Link>

          {/* History */}
          <Link href="/history">

            <div
              style={{ animationDelay: "0.4s" }}
              className="animate-fadeIn group p-10 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-2xl cursor-pointer transition-all duration-500 hover:-translate-y-3 hover:scale-[1.03] hover:border-yellow-400 hover:shadow-[0_25px_70px_rgba(234,179,8,0.18)]"
            >

              <div className="mb-8 text-5xl">
                
              </div>

              <h3 className="text-3xl font-bold group-hover:text-yellow-300 transition">
                History
              </h3>

              <p className="text-gray-400 mt-4 text-base leading-relaxed">
                Review previous predictions, confidence scores, and AI analysis.
              </p>

            </div>

          </Link>

        </div>

      </div>

    </main>
  )
}