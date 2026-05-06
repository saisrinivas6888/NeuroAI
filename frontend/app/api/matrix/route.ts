import { prisma } from "@/lib/prisma"

export async function GET() {

  const records = await prisma.eEGRecord.findMany({
    orderBy: { createdAt: "desc" },
    include: {
      patient: true
    }
  })

  //  keep only latest per patient
  const seen = new Set()
  const latest = []

  for (const r of records) {
    if (!seen.has(r.patientId)) {
      seen.add(r.patientId)
      latest.push(r)
    }
  }

  return Response.json(latest)
}