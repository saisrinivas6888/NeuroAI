"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"

export default function PatientDetail() {

  const { id } = useParams()
  const [patient, setPatient] = useState<any>(null)

  useEffect(() => {
    fetchPatient()
  }, [])

  async function fetchPatient() {
    const res = await fetch(`/api/patient/${id}`)
    if (!res.ok) {
        console.error("API failed")
        return
    }

    const data = await res.json()
    setPatient(data)
  }

  if (!patient) {
    return <div className="text-white p-10">Loading...</div>
  }

  return (
    <main className="min-h-screen relative overflow-hidden text-white px-10 py-8">

      {/* 🌌 BACKGROUND */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-purple-900 via-black to-cyan-900 opacity-70" />
      <div className="absolute w-[600px] h-[600px] bg-purple-600 blur-[200px] opacity-20 top-[-100px] left-[-100px] rounded-full" />
      <div className="absolute w-[500px] h-[500px] bg-cyan-500 blur-[200px] opacity-20 bottom-[-100px] right-[-100px] rounded-full" />

      {/* 🧑 PATIENT INFO */}
      <h1 className="text-4xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-cyan-400 text-transparent bg-clip-text">
        {patient.name}
      </h1>

      <p className="text-gray-400 mb-10">
        Age: {patient.age} • Gender: {patient.gender}
      </p>

      {/*  EEG RECORDS */}
      <h2 className="text-2xl mb-6">EEG Records</h2>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

  {patient.records?.map((r: any) => {

    const pred = patient.predictions?.find(
      (p: any) => p.filePath === r.filePath
    )

    return (
      <div
        key={r.id}
        className="p-5 rounded-xl bg-white/5 border border-white/10 backdrop-blur-xl hover:border-purple-400 transition"
      >
        <p className="text-sm text-gray-400">
          {new Date(r.createdAt).toLocaleString()}
        </p>

        <p className="mt-2 text-white font-medium">
          {r.fileName}
        </p>

        {/* 🔥 PREDICTION */}
        {pred ? (
          <div className="mt-4">

            <p className="text-sm">
              Prediction:{" "}
              <span className={
                pred.prediction === "Alzheimer"
                  ? "text-red-400"
                  : "text-green-400"
              }>
                {pred.prediction}
              </span>
            </p>

            <p className="text-gray-400 text-sm">
              Confidence: {(pred.confidence * 100).toFixed(2)}%
            </p>

          </div>
        ) : (
          <p className="text-gray-500 text-sm mt-3">
            No analysis yet
          </p>
        )}

      </div>
    )
  })}

</div>
    </main>
  )
}