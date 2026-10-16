"""Jev translation-checking R&D. See README.md."""

import argparse


def main() -> None:
    from jevqa import agenda, backends, report, run

    p = argparse.ArgumentParser(prog="jevqa")
    sub = p.add_subparsers(dest="cmd", required=True)

    def conditions(sp):
        sp.add_argument("--target", required=True, choices=sorted(agenda.TARGETS))
        sp.add_argument("--backend", default="jev", help="jev | jev:jev-preview | openrouter[:model] | dryrun")
        sp.add_argument("--no-approved", action="store_true", help="leave target-language tW headwords out of the state")
        sp.add_argument("--no-renderings", action="store_true", help="leave the aligned target words out of the state")
        sp.add_argument("--with-ult", action="store_true", help="also give the English ULT verse (the Masalit team's source text)")

    r = sub.add_parser("run", help="ask a checker every question for a target (plus planted faults)")
    conditions(r)
    r.add_argument("--no-mutants", action="store_true", help="real verses only, no planted faults")
    r.add_argument("--workers", type=int, default=8)
    t = sub.add_parser("route", help="tier the real verses: auto-log, explain + recheck, human queue")
    conditions(t)
    t.add_argument("--no-mutants", action="store_true", help="route a run made with --no-mutants")
    t.add_argument("--t-auto", type=float, default=0.9)
    o = sub.add_parser("report", help="write runs/<target>/report.md comparing every backend run so far")
    o.add_argument("--target", required=True, choices=sorted(agenda.TARGETS))
    a = p.parse_args()

    if a.cmd == "report":
        print(report.write(a.target))
        return
    cond = run.Condition(mutants=not a.no_mutants, approved=not a.no_approved,
                         renderings=not a.no_renderings, source=a.with_ult)
    if a.cmd == "run":
        run.run(a.target, backends.make(a.backend, run.RUNS / a.target), cond, a.workers)
    elif a.cmd == "route":
        run.route(a.target, backends.make(a.backend), cond, a.t_auto)
