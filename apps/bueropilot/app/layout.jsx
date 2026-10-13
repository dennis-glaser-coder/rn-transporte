import "./styles.css";

export const metadata = {
  title: "RN BüroPilot | Mitarbeiterzugang",
  description: "Interne Betriebsverwaltung",
  robots: { index: false, follow: false }
};

export default function Layout({ children }) {
  return <html lang="de"><body>{children}</body></html>;
}
