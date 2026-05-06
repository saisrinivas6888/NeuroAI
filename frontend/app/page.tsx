"use client"
import Link from "next/link"
import { motion } from "framer-motion"
import { TypeAnimation } from "react-type-animation"

export default function Home() {
  return (
    <main className="relative min-h-screen bg-black text-white overflow-hidden">

      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-black to-cyan-900 opacity-80" />

      {/* Moving energy blobs */}
      <motion.div
        animate={{ x:[0,120,0], y:[0,-80,0] }}
        transition={{ duration:12, repeat:Infinity }}
        className="absolute w-[700px] h-[700px] bg-purple-600 rounded-full blur-[250px] opacity-30 top-[-200px] left-[-200px]"
      />

      <motion.div
        animate={{ x:[0,-120,0], y:[0,80,0] }}
        transition={{ duration:14, repeat:Infinity }}
        className="absolute w-[600px] h-[600px] bg-cyan-500 rounded-full blur-[250px] opacity-30 bottom-[-200px] right-[-200px]"
      />

      {/* NAVBAR */}
      <nav className="relative z-10 flex justify-between items-center px-12 py-6 backdrop-blur-lg">

        <h1 className="text-2xl font-bold tracking-wider bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
          NeuroAI
        </h1>

        <div className="flex gap-8 items-center text-sm">

          <Link href="/">
            <motion.div whileHover={{ y:-3 }} className="relative cursor-pointer group">
              Home
              <span className="absolute left-0 -bottom-1 w-0 h-[2px] bg-cyan-400 transition-all group-hover:w-full"></span>
            </motion.div>
          </Link>

          
          <Link href="/upload">
            <motion.div whileHover={{ y:-3 }} className="relative cursor-pointer group">
              Upload EEG
              <span className="absolute left-0 -bottom-1 w-0 h-[2px] bg-cyan-400 transition-all group-hover:w-full"></span>
            </motion.div>
          </Link>

          <Link href="/signin">
            <button className="border border-gray-600 px-4 py-2 rounded-lg hover:bg-gray-800 transition">
              Sign In
            </button>
          </Link>

          <Link href="/signup">
            <button className="bg-gradient-to-r from-purple-500 to-cyan-500 px-5 py-2 rounded-lg hover:scale-105 transition">
              Sign Up
            </button>
          </Link>

        </div>

      </nav>


      {/* HERO SECTION */}
      <section className="relative z-10 flex flex-col items-center justify-center text-center pt-32 px-6">

        <motion.h1
        initial={{ opacity:0, y:50 }}
        animate={{ opacity:1, y:0 }}
        transition={{ duration:1 }}
        whileHover={{ scale:1.02 }}
        className="text-7xl md:text-8xl font-bold max-w-6xl leading-tight"
        >

        AI That
        <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
        {" "}Reads the Brain
        </span>

        </motion.h1>


        {/* Typing animation */}
        <div className="text-2xl text-gray-400 mt-8 h-12">

        <TypeAnimation
        sequence={[
        "Detecting Alzheimer's before symptoms appear",
        2000,
        "Analyzing EEG brain connectivity",
        2000,
        "Deep learning powered neuroscience",
        2000,
        "Decoding neural signals with AI",
        2000
        ]}
        speed={50}
        repeat={Infinity}
        />

        </div>


        {/* Floating Buttons */}
        <motion.div
        animate={{ y:[0,-6,0] }}
        transition={{ duration:4, repeat:Infinity }}
        className="flex gap-6 mt-14"
        >

        <Link href="/upload">
          <motion.button
          whileHover={{ scale:1.08 }}
          whileTap={{ scale:0.95 }}
          className="bg-gradient-to-r from-purple-500 to-cyan-500 px-10 py-4 rounded-xl text-lg font-semibold
          shadow-lg shadow-purple-500/30 hover:shadow-cyan-500/40 transition duration-300"
          >
          Analyze EEG
          </motion.button>
        </Link>

        </motion.div>

      </section>

    </main>
  )
}