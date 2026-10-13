import { requireStaff, jsonError } from "../../../lib/auth";
export const runtime = "nodejs";
export async function GET(request) {
  try {
    const { db, staff } = await requireStaff(request);
    const { data, error } = await db.from("rn_jobs")
      .select("id,customer,site,date,start_time,pump,status,volume_m3")
      .eq("org_id", staff.org_id).order("date", { ascending: true }).limit(100);
    if (error) throw error;
    return Response.json({ jobs: data || [] }, { headers: { "Cache-Control": "no-store" } });
  } catch (error) { return jsonError(error); }
}
// No POST/PUT/DELETE route: AI and users cannot write jobs in this pilot.
