import FabGate from "@/components/sections/FabGate";
import { ROUTES } from "@/components/nav/nav";

export default function Page() {
  return <FabGate route={ROUTES.find((r) => r.href === "/brain")!} />;
}
