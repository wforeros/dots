// Gives every new space the same three tabs: Agents, Code, Commands.
// There is no "space created" event in the app, so this reads spaces() on render
// and keeps the ids it already handled in shared state.
import { View, div } from "gpui-kit";
import { machines, run, setShared, shared, spaces } from "herdr";

const SEEN = "space-tabs.seen";

export default class SpaceTabs extends View {
  render(_cx) {
    // Before the machines answer, spaces() is empty: initializing then would
    // make every existing space look new.
    if (machines().some((m) => m.layout === "loading")) return div();

    const seen = shared(SEEN);
    const list = Array.isArray(seen) ? seen : null;
    const known = new Set(list ?? []);
    const fresh = spaces().filter((s) => !known.has(s.id));

    if (list === null) {
      // First run: existing spaces keep the tabs they have.
      setShared(SEEN, fresh.map((s) => s.id));
    } else if (fresh.length) {
      setShared(SEEN, [...list, ...fresh.map((s) => s.id)]);
      for (const s of fresh) {
        const first = s.tabs[0];
        if (first) run("tab.rename", { id: first.id, name: "Agents" });
        run("tab.new", { space: s.id, name: "Code" });
        run("tab.new", { space: s.id, name: "Commands" });
        if (first && s.active) run("tab.select", { id: first.id });
      }
    }
    return div();
  }
}
