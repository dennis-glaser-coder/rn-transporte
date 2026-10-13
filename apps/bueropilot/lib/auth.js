import { createClient } from "@supabase/supabase-js";

export class ApiError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

export async function requireStaff(request) {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !anon) throw new ApiError(503, "Anmeldung ist noch nicht eingerichtet.");
  const header = request.headers.get("authorization") || "";
  const token = header.startsWith("Bearer ") ? header.slice(7).trim() : "";
  if (!token || token.length > 8192) throw new ApiError(401, "Bitte anmelden.");

  // Only user-scoped anon client; RLS applies to every database read.
  const db = createClient(url, anon, {
    global: { headers: { Authorization: "Bearer " + token } },
    auth: { persistSession: false, autoRefreshToken: false }
  });
  const { data: authData, error: authError } = await db.auth.getUser(token);
  const user = authData?.user;
  if (authError || !user) throw new ApiError(401, "Sitzung abgelaufen. Bitte neu anmelden.");

  const { data: staff, error } = await db.from("rn_staff")
    .select("org_id, role, enabled")
    .eq("user_id", user.id).eq("enabled", true).limit(1).maybeSingle();
  if (error || !staff) throw new ApiError(403, "Kein freigegebener RN-Mitarbeiterzugang.");
  return { db, user, staff };
}

export function jsonError(error) {
  const status = error instanceof ApiError ? error.status : 500;
  return Response.json({ error: status === 500 ? "Serverfehler. Bitte erneut versuchen." : error.message }, {
    status,
    headers: { "Cache-Control": "no-store" }
  });
}
