"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { signIn } from "next-auth/react"
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function SignIn() {

  const router = useRouter()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  async function handleSubmit(e:any) {
    e.preventDefault()

    const res = await signIn("credentials", {
      email,
      password,
      redirect: false
    })

    if (res?.ok) {
      router.push("/dashboard")
    } else {
      alert("Invalid email or password")
    }
  }

  return (
    <main className="relative min-h-screen bg-black text-white flex items-center justify-center overflow-hidden">

      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-black to-cyan-900 opacity-80"/>

      {/* glowing blobs */}
      <motion.div
        animate={{ x:[0,80,0], y:[0,-60,0] }}
        transition={{ duration:10, repeat:Infinity }}
        className="absolute w-[600px] h-[600px] bg-purple-600 blur-[220px] opacity-30 -top-40 -left-40 rounded-full"
      />

      <motion.div
        animate={{ x:[0,-80,0], y:[0,60,0] }}
        transition={{ duration:12, repeat:Infinity }}
        className="absolute w-[500px] h-[500px] bg-cyan-500 blur-[220px] opacity-30 -bottom-40 -right-40 rounded-full"
      />

      {/* Card */}
      <motion.div
        initial={{ opacity:0, y:40 }}
        animate={{ opacity:1, y:0 }}
        transition={{ duration:0.8 }}
        className="relative z-10 w-[420px] backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl p-10 shadow-2xl"
      >

        <h1 className="text-3xl font-bold text-center mb-2">
          NeuroAI Access
        </h1>

        <p className="text-gray-400 text-center mb-8 text-sm">
          Sign in to access EEG Alzheimer detection tools
        </p>

        {/* FORM */}
        <form onSubmit={handleSubmit}>

          {/* Email */}
          <div className="mb-4">
            <label className="text-sm text-gray-400">
              Email
            </label>
            <input
              type="email"
              placeholder="doctor@hospital.org"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
              className="w-full mt-2 p-3 rounded-lg bg-black border border-gray-700 focus:outline-none focus:border-cyan-400"
            />
          </div>

          {/* Password */}
          <div className="mb-6">
            <label className="text-sm text-gray-400">
              Password
            </label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
              className="w-full mt-2 p-3 rounded-lg bg-black border border-gray-700 focus:outline-none focus:border-cyan-400"
            />
          </div>

          {/* Sign In button */}
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-purple-500 to-cyan-500 p-3 rounded-lg font-semibold hover:scale-[1.02] transition"
          >
            Sign In
          </button>

        </form>

        <p className="text-center text-sm text-gray-400 mt-6">
          New to NeuroAI?{" "}
          <Link href="/signup" className="text-cyan-400 hover:underline">
            Create account
          </Link>
        </p>

      </motion.div>

    </main>
  )
}