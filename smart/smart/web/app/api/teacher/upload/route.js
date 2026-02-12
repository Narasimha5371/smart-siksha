import { NextResponse } from "next/server";

export async function POST(request) {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";
  const formData = await request.formData();

  const resp = await fetch(`${apiBase}/teacher/upload-curriculum`, {
    method: "POST",
    body: formData,
  });

  const data = await resp.json();
  return NextResponse.json(data, { status: resp.status });
}
