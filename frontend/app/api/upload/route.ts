import { writeFile } from "fs/promises"
import path from "path"
import { prisma } from "../../../lib/prisma"

export async function POST(req: Request) {
  try {
    const formData = await req.formData()

    const file = formData.get("file") as File
    const patientId = formData.get("patientId") as string
    const userId = formData.get("userId") as string

    if (!file || !patientId || !userId) {
      return Response.json({ error: "Missing data" }, { status: 400 })
    }

    // convert file to buffer
    const bytes = await file.arrayBuffer()
    const buffer = Buffer.from(bytes)

    // ensure uploads folder exists
    const uploadDir = path.join(process.cwd(), "uploads")

    // create unique filename
    const fileName = `${Date.now()}-${file.name}`
    const filePath = path.join(uploadDir, fileName)

    // save file
    await writeFile(filePath, buffer)

    // save record in DB
    await prisma.eEGRecord.create({
      data: {
        fileName,
        filePath,
        patientId,
        userId
      }
    })

    return Response.json({ success: true })

  } catch (err) {
    console.error(err)
    return Response.json({ error: "Upload failed" }, { status: 500 })
  }
}