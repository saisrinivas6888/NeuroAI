export async function POST(req: Request) {
  try {
    const { filePath } = await req.json()

    if (!filePath) {
      return Response.json({ error: "No filePath" }, { status: 400 })
    }

    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        filePath
      })
    })

    const data = await res.json()

    console.log(" FINAL RESPONSE:", data)

    return Response.json(data)

  } catch (err) {
    console.error(err)
    return Response.json({ error: "Failed" }, { status: 500 })
  }
}