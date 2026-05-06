import { prisma } from "@/lib/prisma"

export async function POST(req: Request) {
  try {
    const formData = await req.formData()

    const file = formData.get("file") as File
    const patientId = formData.get("patientId") as string

    if (!file || !patientId) {
      return Response.json({ error: "Missing data" }, { status: 400 })
    }

    //  Send EEG to FastAPI
    const pythonForm = new FormData()
    pythonForm.append("file", file)

    const response = await fetch("http://127.0.0.1:8000/preprocess", {
      method: "POST",
      body: pythonForm
    })

    const data = await response.json()

    if (!data.file_path) {
      return Response.json({ error: "Processing failed" }, { status: 500 })
    }

    //  SAVE ONLY PATH (no file saving anymore)
    await prisma.eEGRecord.create({
      data: {
        fileName: data.file_path.split("\\").pop(),
        filePath: data.file_path,   //  backend path
        patientId,
        userId: "temp_user"
      }
    })

    return Response.json({ success: true })

  } catch (err) {
    console.error(err)
    return Response.json({ error: "Failed" }, { status: 500 })
  }
}