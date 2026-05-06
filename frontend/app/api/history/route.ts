import { prisma } from "@/lib/prisma"

export async function GET() {
  try {

    const data = await prisma.prediction.findMany({
      include: {
        patient: true
      },
      orderBy: {
        createdAt: "desc"
      }
    })

    return Response.json(data)

  } catch (err) {
    console.error(err)
    return Response.json({ error: "Failed" }, { status: 500 })
  }
}