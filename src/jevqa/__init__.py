"""Jev translation-checking R&D. See README.md."""

import argparse


def main() -> None:
    from jevqa import agenda, backends, report, run

    p = argparse.ArgumentParser(prog="jevqa")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="ask a checker every question for a target (plus seeded faults)")
    r.add_argument("--target", required=True, choices=sorted(agenda.TARGETS))
    r.add_argument("--backend", default="jev", help="jev | jev:jev-preview | openrouter[:model] | dryrun")
    r.add_argument("--no-mutants", action="store_true", help="real verses only, no seeded faults")
    r.add_argument("--workers", type=int, default=8)
    r.add_argument("--no-approved", action="store_true", help="leave target-language tW headwords out of the state")
    r.add_argument("--with-ult", action="store_true", help="also give the English ULT verse (the Masalit team's source text)")
    t = sub.add_parser("route", help="tier the real verses: auto-log, explain + recheck, human queue")
    t.add_argument("--target", required=True, choices=sorted(agenda.TARGETS))
    t.add_argument("--backend", default="jev")
    t.add_argument("--t-auto", type=float, default=0.9)
    o = sub.add_parser("report", help="write runs/<target>/report.md comparing every backend run so far")
    o.add_argument("--target", required=True, choices=sorted(agenda.TARGETS))
    a = p.parse_args()

    if a.cmd == "run":
        b = backends.make(a.backend, run.RUNS / a.target)
        approved = not a.no_approved
        cases = run.cases_for(a.target, not a.no_mutants, approved, a.with_ult)
        run.run(a.target, b, cases, a.workers, approved, a.with_ult)
    elif a.cmd == "route":
        run.route(a.target, backends.make(a.backend), a.t_auto)
    elif a.cmd == "report":
        print(report.write(a.target))
