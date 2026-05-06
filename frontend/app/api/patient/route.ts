import { prisma } from "../../../lib/prisma"

export async function GET() {
  const patients = await prisma.patient.findMany({
    orderBy: { createdAt: "desc" },
    include:{
        records:true
    }
  })

  return Response.json(patients)
}

export async function POST(req: Request) {
  const body = await req.json()

  const patient = await prisma.patient.create({
    data: {
      name: body.name,
      age: body.age,
      gender: body.gender,
      userId: body.userId
    }
  })

  return Response.json(patient)
}