import { prisma } from "@/lib/prisma"

export async function POST(req: Request) {
  try {
    const { patientId, filePath, prediction, confidence } = await req.json()

    console.log(" SAVING:", patientId, prediction)

    //  ADD VALIDATION HERE
    if (
      !patientId ||
      !prediction ||
      typeof confidence !== "number" ||
      isNaN(confidence)
    ) {
      console.error(" Invalid data:", { patientId, prediction, confidence })
      return Response.json({ error: "Invalid data" }, { status: 400 })
    }

    await prisma.prediction.create({
      data: {
        patientId,
        filePath,
        prediction,
        confidence
      }
    })

    return Response.json({ success: true })

  } catch (err) {
    console.error(" SAVE ERROR:", err)
    return Response.json({ error: "Failed" }, { status: 500 })
  }
}