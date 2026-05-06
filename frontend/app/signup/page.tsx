"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function SignUp() {

  const router = useRouter()

  const [name, setName] = useState("")
  const [institution, setInstitution] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  async function handleSignup() {

    const res = await fetch("/api/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name,
        institution,
        email,
        password
      })
    })

    const data = await res.json()

    if (data.success) {
      alert("Account created successfully")
      router.push("/signin")
    } else {
      alert(data.error || "Signup failed")
    }
  }

  return (
    <main className="relative min-h-screen bg-black text-white flex items-center justify-center overflow-hidden">

      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-black to-cyan-900 opacity-80"/>

      {/* glow */}
      <motion.div
        animate={{ x:[0,100,0], y:[0,-80,0] }}
        transition={{ duration:12, repeat:Infinity }}
        className="absolute w-[650px] h-[650px] bg-purple-600 blur-[220px] opacity-30 -top-40 -left-40 rounded-full"
      />

      <motion.div
        animate={{ x:[0,-100,0], y:[0,80,0] }}
        transition={{ duration:14, repeat:Infinity }}
        className="absolute w-[600px] h-[600px] bg-cyan-500 blur-[220px] opacity-30 -bottom-40 -right-40 rounded-full"
      />

      {/* Form */}
      <motion.div
        initial={{ opacity:0, y:40 }}
        animate={{ opacity:1, y:0 }}
        transition={{ duration:0.8 }}
        className="relative z-10 w-[440px] backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl p-10 shadow-2xl"
      >

        <h1 className="text-3xl font-bold text-center mb-2">
          Create NeuroAI Account
        </h1>

        <p className="text-gray-400 text-center mb-8 text-sm">
          For clinicians, neurologists and medical researchers
        </p>

        {/* Name */}
        <input
          placeholder="Full Name"
          value={name}
          onChange={(e)=>setName(e.target.value)}
          className="w-full p-3 rounded-lg bg-black border border-gray-700 mb-4 focus:outline-none focus:border-cyan-400"
        />

        {/* Institution */}
        <input
          placeholder="Hospital / University"
          value={institution}
          onChange={(e)=>setInstitution(e.target.value)}
          className="w-full p-3 rounded-lg bg-black border border-gray-700 mb-4 focus:outline-none focus:border-cyan-400"
        />

        {/* Email */}
        <input
          type="email"
          placeholder="professional email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          className="w-full p-3 rounded-lg bg-black border border-gray-700 mb-4 focus:outline-none focus:border-cyan-400"
        />

        {/* Password */}
        <input
          type="password"
          placeholder="Create password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          className="w-full p-3 rounded-lg bg-black border border-gray-700 mb-6 focus:outline-none focus:border-cyan-400"
        />

        <button
          onClick={handleSignup}
          className="w-full bg-gradient-to-r from-purple-500 to-cyan-500 p-3 rounded-lg font-semibold hover:scale-[1.02] transition"
        >
          Create Account
        </button>

        <p className="text-center text-sm text-gray-400 mt-6">
          Already registered?{" "}
          <Link href="/signin" className="text-cyan-400 hover:underline">
            Sign in
          </Link>
        </p>

      </motion.div>

    </main>
  )
}