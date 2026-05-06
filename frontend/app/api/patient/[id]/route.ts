import { prisma } from "@/lib/prisma"

export async function GET(
  req: Request,
  context: { params: Promise<{ id: string }> }
) {

  const { id } = await context.params

  const patient = await prisma.patient.findUnique({
    where: { id },
    include: {
      records: true,
      predictions: true
    }
  })

  return Response.json(patient)
}


//  DELETE PATIENT
export async function DELETE(
  req: Request,
  context: { params: Promise<{ id: string }> }
) {

  const { id } = await context.params

  await prisma.patient.delete({
    where: { id }
  })

  return Response.json({
    success: true
  })
}

//  Edit Patient
export async function PUT(
  req: Request,
  context: { params: Promise<{ id: string }> }
) {

  const { id } = await context.params

  const body = await req.json()

  const updated = await prisma.patient.update({
    where: { id },
    data: {
      name: body.name,
      age: body.age,
      gender: body.gender
    }
  })

  return Response.json(updated)
}