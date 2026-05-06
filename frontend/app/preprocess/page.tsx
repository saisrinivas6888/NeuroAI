"use client"
import Link from "next/link"

import { useState, useEffect } from "react"

export default function Preprocess() {

  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState("")
  const [matrixReady, setMatrixReady] = useState(false)

  const [patients, setPatients] = useState<any[]>([])
  const [selectedPatient, setSelectedPatient] = useState("")
  const [open, setOpen] = useState(false)

  //  Fetch patients
  useEffect(() => {
    fetchPatients()
  }, [])

  async function fetchPatients() {
    try {
      const res = await fetch("/api/patient")
      const data = await res.json()
      setPatients(data)
    } catch {
      setStatus("Failed to load patients")
    }
  }

  async function handlePreprocess() {

    if (!file) {
      setStatus("Please upload an EEG file.")
      return
    }

    if (!selectedPatient) {
      setStatus("Please select a patient.")
      return
    }

    const formData = new FormData()
    formData.append("file", file)
    formData.append("patientId", selectedPatient)

    setStatus("Processing EEG...")

    try {

      const res = await fetch("/api/preprocess-upload", {
        method: "POST",
        body: formData
      })

      const data = await res.json()

      if (data.success) {
        setStatus("Preprocessing complete. Matrix saved in system.")
        setMatrixReady(true)
      } else {
        setStatus("Error preprocessing EEG.")
      }

    } catch (error) {
      setStatus("Server not reachable.")
    }
  }

  return (
  <main className="min-h-screen relative overflow-hidden text-white px-10 py-8 flex items-center justify-center">
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

    {/*  BACKGROUND (same as dashboard) */}
    <div className="absolute inset-0 -z-10 bg-gradient-to-br from-purple-900 via-black to-cyan-900 opacity-70" />
    <div className="absolute w-[600px] h-[600px] bg-purple-600 blur-[200px] opacity-20 top-[-100px] left-[-100px] rounded-full" />
    <div className="absolute w-[500px] h-[500px] bg-cyan-500 blur-[200px] opacity-20 bottom-[-100px] right-[-100px] rounded-full" />

    {/* CONTENT */}
    <div className="w-full max-w-2xl pt-24">

      {/* TITLE */}
      <h1 className="text-5xl font-bold text-center mb-12 bg-gradient-to-r from-purple-400 to-cyan-400 text-transparent bg-clip-text">
        Preprocess EEG
      </h1>

      {/* CARD */}
      <div className="p-10 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl shadow-[0_0_60px_rgba(139,92,246,0.25)]">

        {/* PATIENT DROPDOWN */}
        <label className="text-gray-400 text-sm mb-3 block">
          Select Patient
        </label>

        <div className="relative mb-8">

          {/* CLICK BOX */}
          <div
            onClick={() => setOpen(!open)}
            className="w-full p-5 bg-black/80 border border-purple-500/40 rounded-xl cursor-pointer flex justify-between items-center hover:border-cyan-400 transition"
          >
            <span>
              {selectedPatient
                ? patients.find(p => p.id === selectedPatient)?.name
                : "Choose a patient..."}
            </span>

            <span className={`transition ${open ? "rotate-180" : ""}`}>
              ▼
            </span>
          </div>

          {/* DROPDOWN LIST */}
          <div
            className={`absolute w-full mt-2 bg-black/90 border border-white/10 rounded-xl overflow-hidden backdrop-blur-xl transition-all duration-300 origin-top ${
              open ? "scale-y-100 opacity-100" : "scale-y-0 opacity-0 pointer-events-none"
            }`}
          >
            {patients.map((p) => (
              <div
                key={p.id}
                onClick={() => {
                  setSelectedPatient(p.id)
                  setOpen(false)
                }}
                className="p-4 hover:bg-white/10 cursor-pointer transition"
              >
                {p.name}
              </div>
            ))}
          </div>

        </div>

        {/* FILE INPUT */}
        <div className="mb-6">
          <label className="text-gray-400 text-sm block mb-2">
            Upload EEG File (.set)
          </label>

          <input
            type="file"
            accept=".set"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full p-3 bg-black border border-gray-700 rounded-lg"
          />
        </div>

        {/* BUTTON */}
        <button
          onClick={handlePreprocess}
          className="w-full py-4 text-lg rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 hover:scale-105 hover:shadow-[0_0_30px_rgba(139,92,246,0.5)] transition duration-300 font-semibold"
        >
          Preprocess EEG
        </button>

        {/* STATUS */}
        {status && (
          <p className="mt-4 text-gray-400 text-center">
            {status}
          </p>
        )}

        {/* NEXT STEP */}
        {matrixReady && (
          <a
            href="/upload"
            className="block mt-6 text-center py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 hover:scale-105 transition"
          >
            Run AI Analysis →
          </a>
        )}

      </div>

    </div>

  </main>
)
}