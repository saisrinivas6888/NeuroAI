"use client"

import { useEffect, useState } from "react"
import Link from "next/link"

export default function HistoryPage() {

  const [data, setData] = useState<any[]>([])
  const [search, setSearch] = useState("")

  useEffect(() => {
    fetchHistory()
  }, [])

  async function fetchHistory() {
    const res = await fetch("/api/history")
    const result = await res.json()
    setData(result)
  }

  return (
    <main className="min-h-screen relative overflow-hidden text-white px-10 py-8">

      {/*  HOME BUTTON */}
      <Link
        href="/dashboard"
        className="fixed top-6 left-6 z-50 px-5 py-3 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl hover:border-cyan-400 hover:bg-white/10 transition-all duration-300 hover:scale-105 hover:shadow-[0_0_30px_rgba(0,255,255,0.2)]"
      >

        <div className="flex items-center gap-3">

          <span className="text-2xl">
        
          </span>

          <span className="font-semibold bg-gradient-to-r from-purple-400 to-cyan-400 text-transparent bg-clip-text">
            NeuroAI
          </span>

        </div>

      </Link>

      {/*  BACKGROUND */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-purple-900 via-black to-cyan-900 opacity-70" />

      <div className="absolute w-[600px] h-[600px] bg-purple-600 blur-[200px] opacity-20 top-[-100px] left-[-100px] rounded-full" />

      <div className="absolute w-[500px] h-[500px] bg-cyan-500 blur-[200px] opacity-20 bottom-[-100px] right-[-100px] rounded-full" />

      <div className="animate-fadeIn pt-24">

        {/* TITLE */}
        <h1 className="text-5xl font-bold mb-10 bg-gradient-to-r from-purple-400 to-cyan-400 text-transparent bg-clip-text">
          Patient History
        </h1>

        {/*  SEARCH */}
        <div className="mb-10 max-w-xl">
          <input
            placeholder="Search patient..."
            value={search}
            onChange={(e)=>setSearch(e.target.value)}
            className="w-full p-4 bg-black/80 border border-gray-700 rounded-xl focus:ring-2 focus:ring-cyan-400 transition-all outline-none"
          />
        </div>

        {/*  HISTORY LIST */}
        <div className="space-y-6">

          {data
            .filter((item) =>
              (item.patient?.name || "")
                .toLowerCase()
                .includes(search.trim().toLowerCase())
            )
            .map((item) => {

              const confidencePercent = item.confidence * 100

              return (
                <div
                  key={item.id}
                  className="p-7 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl transition-all duration-300 hover:scale-[1.01] hover:border-cyan-400 hover:shadow-[0_10px_40px_rgba(0,255,255,0.2)]"
                >

                  {/* HEADER */}
                  <div className="flex justify-between items-center">

                    <h2 className="text-2xl font-semibold">
                      {item.patient?.name}
                    </h2>

                    <span className="text-sm text-gray-400">
                      {new Date(item.createdAt).toLocaleString()}
                    </span>

                  </div>

                  {/* BODY */}
                  <div className="mt-5 flex justify-between items-center">

                    <div>

                      {/* PREDICTION BADGE */}
                      <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                        item.prediction === "Alzheimer"
                          ? "bg-red-500/20 text-red-400 border border-red-500/30"
                          : "bg-green-500/20 text-green-400 border border-green-500/30"
                      }`}>
                        {item.prediction}
                      </span>

                      <p className="text-gray-400 text-sm mt-3">
                        Confidence: {confidencePercent.toFixed(2)}%
                      </p>

                      {/* CONFIDENCE BAR */}
                      <div className="mt-4 w-full max-w-sm bg-white/10 rounded-full h-3 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-cyan-400 to-purple-500 transition-all duration-700"
                          style={{ width: `${confidencePercent}%` }}
                        />
                      </div>

                    </div>

                    {/* RIGHT SIDE */}
                    <div className="text-right">

                      <div className="text-3xl font-bold text-cyan-400">
                        {Math.floor(confidencePercent)}%
                      </div>

                      <p className="text-xs text-gray-400 mb-4">
                        confidence
                      </p>

                      {/* VIEW PATIENT BUTTON */}
                      <Link href={`/patients/${item.patientId}`}>
                        <button className="px-5 py-2 rounded-xl bg-white/10 hover:bg-cyan-500/20 hover:border-cyan-400 border border-white/10 transition-all duration-300 hover:scale-105">
                          View →
                        </button>
                      </Link>

                    </div>

                  </div>

                </div>
              )
            })}

        </div>

      </div>

    </main>
  )
}