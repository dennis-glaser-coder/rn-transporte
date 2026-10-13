// RN BüroPilot deployment smoke tests (static checks, no customer data).
import assert from "node:assert/strict";
import {readFileSync, existsSync} from "node:fs";
import {Script, runInNewContext} from "node:vm";

const read = path => readFileSync(path, "utf8");
const root = "bueropilot/";
const html = read(root + "index.html");
const sources = ["app.js","enhancements.js","fleet.js","voice.js","operations.js","documents.js"];
const assets = ["app.css","config.js","index.html",...sources];
const errors = [];
function test(name, fn) {
  try {fn(); console.log("OK  " + name);}
  catch (error) {errors.push(name + ": " + error.message);console.error("FAIL " + name + ": " + error.message);}
}

for (const file of assets) test("file " + file, () => assert.ok(existsSync(root + file)));
for (const file of sources) test("JavaScript syntax " + file, () => {new Script(read(root + file), {filename:file})});
const app = read(root + "app.js");
const enhanced = read(root + "enhancements.js");
const fleet = read(root + "fleet.js");

test("registered views have HTML panels", () => {
  const match = app.match(/views=\[([^\]]+)\]/);
  assert.ok(match, "views missing");
  const views = JSON.parse("[" + match[1] + "]");
  for (const view of views) assert.ok(html.includes('id="' + view + 'View"'), "missing view: " + view);
});
test("static HTML references and dynamically created controls", () => {
  const found = new Set([...html.matchAll(/id="([^"]+)"/g)].map(x => x[1]));
  for (const file of ["enhancements.js","operations.js","documents.js"]) for (const x of read(root+file).matchAll(/id="([^"]+)"/g)) found.add(x[1]);
  for (const file of sources) {
    for (const match of read(root + file).matchAll(/\$\("([^"]+)"\)/g)) {
      assert.ok(found.has(match[1]), "missing control " + match[1] + " referenced in " + file);
    }
  }
});
test("script and stylesheet assets linked", () => {
  for (const file of ["app.js","enhancements.js","fleet.js","voice.js","config.js","operations.js","documents.js"])
    assert.match(html, new RegExp('src="\\./'+file.replace(".", "\\.")+'(?:\\?v=[0-9]+)?"'));
  assert.ok(html.includes('href="./app.css?v='));
});
test("trailer connections remain RLS protected", () => {
  assert.match(fleet, /db\.rpc\("rn_connect_trailer"/);
  assert.ok(fleet.includes("if(live&&canWrite)"));
  assert.ok(fleet.includes("localStorage.setItem(previewKey"));
});
test("timesheet CSV export validates meaningful fields", () => {
  assert.match(enhanced, /Number\.isFinite\(hours\)/);
  assert.match(enhanced, /confirm\.checked/);
  assert.match(enhanced, /photo\.files/);
});
test("calendar selected date navigates to the correct week", () => {
  const begin=app.indexOf("function goToCalendarDate("),end=app.indexOf("function parseDelimited(",begin);
  assert.ok(begin>=0&&end>begin);
  let rendered=0;
  const ctx={window:{},weekOffset:0,renderWeek:()=>rendered++,
    dateISO:d=>[d.getFullYear(),String(d.getMonth()+1).padStart(2,"0"),String(d.getDate()).padStart(2,"0")].join("-")};
  runInNewContext(app.slice(begin,end),ctx);
  ctx.window.RNBuroPilotGoToCalendarDate("2026-10-13");
  assert.equal(rendered,1,"valid day should navigate to calendar week");
  ctx.window.RNBuroPilotGoToCalendarDate("2026-99-99");
  assert.equal(rendered,1,"invalid day must not navigate");
});

test("protected business workflows are wired", () => {
  const operations=read(root+"operations.js"),documents=read(root+"documents.js");
  for (const name of ["rn_quote_to_job","rn_job_advance","rn_quotes","rn_customers","rn_employees"]) assert.ok(operations.includes(name),name);
  for (const name of ["rn_toll_imports","rn_timesheets","rn_invoice_drafts","rn_customer_sites"]) assert.ok(documents.includes(name),name);
  assert.ok(operations.includes("window.RNBuroPilotReloadJobs"),"dashboard refresh missing");
  assert.ok(documents.includes("window.RNBuroPilotCSV"),"CSV integration missing");
});

test("CSV separator detection handles comma-heavy fields", () => {
  const begin = app.indexOf("function parseDelimited(");
  const end = app.indexOf("async function csvFile(", begin);
  assert.ok(begin > 0 && end > begin);
  const context = {};
  runInNewContext(app.slice(begin, end) + ";this.csvTest={parseDelimited,delimiter};", context);
  const {parseDelimited,delimiter} = context.csvTest;
  const cases = [
    {csv:"Datum;Kunde;Maut\n13.10.2026;Kunde, GmbH, NL, De;123,45\n14.10.2026;Firma, GmbH, NL, De;4,50\n",sep:";",cols:3},
    {csv:'ID,Date,Note\n1,2026-10-12,"test, field"\n',sep:",",cols:3},
    {csv:"ID\tDatum\tMaut\n1\t2026-10-12\t1,45\n",sep:"\t",cols:3},
    {csv:'A;B;C\n"mit; Semikolon";2;3\n',sep:";",cols:3}
  ];
  for (const c of cases) {
    assert.equal(delimiter(c.csv),c.sep,"wrong separator");
    for (const row of parseDelimited(c.csv,c.sep)) assert.equal(row.length,c.cols,"inconsistent fields");
  }
});

if (errors.length) {
  console.error(errors.length + " RN BüroPilot smoke checks failed.");
  process.exitCode = 1;
} else console.log("RN BüroPilot: all static smoke checks passed. Runtime, login and production processes still need end-to-end tests.");
