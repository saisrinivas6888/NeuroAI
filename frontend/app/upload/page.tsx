"use client"
import Link from "next/link"

import { useEffect, useState } from "react"
import { useSession, signOut } from "next-auth/react"
import { useRouter } from "next/navigation"

export default function UploadPage() {

  const { data: session, status } = useSession()
  const router = useRouter()

  const [matrices, setMatrices] = useState<any[]>([])
  const [selectedMatrix, setSelectedMatrix] = useState("")
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/signin")
    }
  }, [status, router])

  useEffect(() => {
    fetchMatrices()
  }, [])

  async function fetchMatrices() {
    const res = await fetch("/api/matrix")
    const data = await res.json()
    setMatrices(data)
  }

  //  FIXED FUNCTION
  async function handleAnalyze() {

  if (!selectedMatrix) {
    alert("Select a matrix")
    return
  }

  setLoading(true)

  try {

    //  STEP 1: Run AI
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        filePath: selectedMatrix
      })
    })

    const data = await res.json()

    console.log(" AI RESULT:", data)

    //  STEP 2: Show result
    setResult(data)

    //  STEP 3: Find patientId from selected matrix
    const selectedObj = matrices.find(
      (m) => m.filePath === selectedMatrix
    )

    const patientId = selectedObj?.patientId

    if (!patientId) {
      console.error(" patientId not found")
      return
    }

    //  STEP 4: Save result to DB
    await fetch("/api/save-result", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        patientId: patientId,
        filePath: selectedMatrix,
        prediction: data.prediction,
        confidence: data.confidence
      })
    })

    console.log(" Saved to DB")

  } catch (err) {
    console.error(err)
    alert("Error running AI")
  }

  setLoading(false)
}
  if (status === "loading") {
    return <div className="text-white">Loading...</div>
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

    {/*  BACKGROUND (EXACT SAME AS DASHBOARD) */}
    <div className="absolute inset-0 -z-10 bg-gradient-to-br from-purple-900 via-black to-cyan-900 opacity-70" />

    <div className="absolute w-[600px] h-[600px] bg-purple-600 blur-[200px] opacity-20 top-[-100px] left-[-100px] rounded-full" />

    <div className="absolute w-[500px] h-[500px] bg-cyan-500 blur-[200px] opacity-20 bottom-[-100px] right-[-100px] rounded-full" />

    {/* CONTENT WRAPPER */}
    <div className="w-full max-w-2xl pt-24">

      {/* TITLE */}
      <h1 className="text-5xl font-bold text-center mb-12 bg-gradient-to-r from-purple-400 to-cyan-400 text-transparent bg-clip-text">
        Run AI Analysis
      </h1>

      {/* MAIN CARD */}
      <div className="p-10 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl shadow-[0_0_60px_rgba(139,92,246,0.25)]">

        {/* LABEL */}
        <label className="text-gray-400 text-sm mb-3 block">
          Select Patient Matrix
        </label>

        {/* CUSTOM DROPDOWN */}
<div className="relative mb-8">

  {/* SELECT BOX */}
  <div
    onClick={() => setOpen(!open)}
    className="w-full p-5 bg-black/80 border border-purple-500/40 rounded-xl cursor-pointer flex justify-between items-center hover:border-cyan-400 transition"
  >
    <span>
      {selectedMatrix
        ? matrices.find(m => m.filePath === selectedMatrix)?.patient.name + " — selected"
        : "Choose a matrix..."}
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
     {matrices.map((m) => (
       <div
          key={m.id}
          onClick={() => {
          setSelectedMatrix(m.filePath)
          setOpen(false)
          }}
          className="p-4 hover:bg-white/10 cursor-pointer transition"
           >
           {m.patient.name} — {new Date(m.createdAt).toLocaleDateString()}
       </div>
           ))}
       </div>

      </div>

        {/* BUTTON */}
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full py-4 text-lg rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 hover:scale-105 hover:shadow-[0_0_30px_rgba(139,92,246,0.5)] transition duration-300 font-semibold disabled:opacity-50"
        >
          {loading ? "Running AI..." : "Run AI"}
        </button>

        {/* RESULT */}
        {result && (
          <div className="mt-8 p-6 rounded-xl bg-white/5 border border-white/10 text-center">

            <p className="text-xl">
              Prediction:{" "}
              <span className={
                result.prediction === "Alzheimer"
                  ? "text-red-400"
                  : "text-green-400"
              }>
                {result.prediction}
              </span>
            </p>

            <p className="mt-3 text-gray-300 text-lg">
              Confidence: {(result.confidence * 100).toFixed(2)}%
            </p>

          </div>
        )}

      </div>

    </div>

  </main>
)
}