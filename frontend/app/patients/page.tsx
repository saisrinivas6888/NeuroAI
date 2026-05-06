"use client"

import { useEffect, useState } from "react"
import Link from "next/link"

export default function Patients() {

  const [patients, setPatients] = useState<any[]>([])
  const [name, setName] = useState("")
  const [age, setAge] = useState("")
  const [gender, setGender] = useState("")
  const [search, setSearch] = useState("")

  //  EDIT STATES
  const [editingPatient, setEditingPatient] = useState<any>(null)

  const [editName, setEditName] = useState("")
  const [editAge, setEditAge] = useState("")
  const [editGender, setEditGender] = useState("")

  async function fetchPatients() {
    const res = await fetch("/api/patient")
    const data = await res.json()
    setPatients(data)
  }

  useEffect(() => {
    fetchPatients()
  }, [])

  //  ADD PATIENT
  async function handleAdd() {

    if (!name.trim()) {
      alert("Name is required")
      return
    }

    if (!gender.trim()) {
      alert("Gender is required")
      return
    }

    await fetch("/api/patient", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name,
        age: age ? Number(age) : null,
        gender,
        userId: "1"
      })
    })

    setName("")
    setAge("")
    setGender("")

    fetchPatients()
  }

  //  DELETE
  async function handleDelete(id: string) {

    const confirmDelete = confirm(
      "Delete this patient and all records?"
    )

    if (!confirmDelete) return

    await fetch(`/api/patient/${id}`, {
      method: "DELETE"
    })

    fetchPatients()
  }

  //  OPEN EDIT
  function openEdit(patient: any) {

    setEditingPatient(patient)

    setEditName(patient.name)
    setEditAge(patient.age?.toString() || "")
    setEditGender(patient.gender || "")
  }

  //  SAVE EDIT
  async function saveEdit() {

    if (!editingPatient) return

    await fetch(`/api/patient/${editingPatient.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: editName,
        age: Number(editAge),
        gender: editGender
      })
    })

    setEditingPatient(null)

    fetchPatients()
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
          Patients
        </h1>

        {/* ➕ ADD PATIENT */}
        <div className="p-7 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl mb-10">

          <div className="flex flex-wrap gap-4 items-center">

            <input
              placeholder="Name"
              value={name}
              onChange={(e)=>setName(e.target.value)}
              className="p-4 bg-black/70 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
            />

            <input
              placeholder="Age"
              value={age}
              onChange={(e)=>setAge(e.target.value)}
              className="p-4 bg-black/70 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
            />

            <select
              value={gender}
              onChange={(e)=>setGender(e.target.value)}
              className="p-4 bg-black/70 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>

            <button
              onClick={handleAdd}
              className="px-8 py-4 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 hover:scale-105 transition duration-300 font-semibold"
            >
              Add
            </button>

          </div>

        </div>

        {/*  SEARCH */}
        <div className="mb-10">

          <input
            placeholder="Search patient..."
            value={search}
            onChange={(e)=>setSearch(e.target.value)}
            className="w-full p-4 bg-black/70 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-400"
          />

        </div>

        {/*  PATIENT GRID */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

          {patients
            .filter((p)=>
              p.name.toLowerCase().includes(
                search.toLowerCase()
              )
            )
            .map((p) => (

            <div
              key={p.id}
              className="group p-7 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl transition-all duration-300 hover:scale-[1.02] hover:border-cyan-400 hover:shadow-[0_0_40px_rgba(0,255,255,0.2)]"
            >

              <div className="flex justify-between items-start">

                <div>

                  <h2 className="text-2xl font-bold mb-4">
                    {p.name}
                  </h2>

                  <div className="space-y-2 text-gray-300">

                    <p>
                      Age: {p.age || "N/A"}
                    </p>

                    <p>
                      Gender: {p.gender}
                    </p>

                    <p className="mt-4 text-sm text-cyan-400">
                      Scans: {p.records?.length || 0}
                    </p>

                  </div>

                </div>

                {/* ACTIONS */}
                <div className="flex flex-col gap-3 items-end">

                  <Link
                    href={`/patients/${p.id}`}
                    className="text-cyan-400 hover:text-cyan-300 transition"
                  >
                    View →
                  </Link>

                  <button
                    onClick={() => openEdit(p)}
                    className="text-yellow-400 hover:text-yellow-300 text-sm transition"
                  >
                    Edit
                  </button>

                  <button
                    onClick={() => handleDelete(p.id)}
                    className="text-red-400 hover:text-red-300 text-sm transition"
                  >
                    Delete
                  </button>

                </div>

              </div>

            </div>

          ))}

        </div>

      </div>

      {/*  EDIT MODAL */}
      {editingPatient && (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">

          <div className="w-full max-w-md p-8 rounded-3xl bg-zinc-900 border border-white/10 shadow-[0_0_50px_rgba(0,0,0,0.5)]">

            <h2 className="text-3xl font-bold mb-6 text-white">
              Edit Patient
            </h2>

            <div className="space-y-4">

              <input
                value={editName}
                onChange={(e)=>setEditName(e.target.value)}
                placeholder="Name"
                className="w-full p-4 bg-black/70 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
              />

              <input
                value={editAge}
                onChange={(e)=>setEditAge(e.target.value)}
                placeholder="Age"
                className="w-full p-4 bg-black/70 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
              />

              <select
                value={editGender}
                onChange={(e)=>setEditGender(e.target.value)}
                className="w-full p-4 bg-black/70 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="">Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>

            </div>

            {/* ACTIONS */}
            <div className="flex justify-end gap-4 mt-8">

              <button
                onClick={() => setEditingPatient(null)}
                className="px-5 py-3 rounded-xl bg-white/10 hover:bg-white/20 transition"
              >
                Cancel
              </button>

              <button
                onClick={saveEdit}
                className="px-5 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-500 hover:scale-105 transition"
              >
                Save
              </button>

            </div>

          </div>

        </div>

      )}

    </main>
  )
}