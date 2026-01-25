#!/usr/bin/env python3
import click
import requests
from terminaltables import SingleTable

package_url = "http://reports.qa.ubuntu.com/m-r-package-team-mapping.json"


@click.command(no_args_is_help=True)
@click.option("--package", "-p", help="Search the team who owns <package>")
@click.option("--team", "-t", help="List all packages owned by <team>")
@click.option("--all", "show_all", is_flag=True, help="Show everything")
@click.option("--teams", "list_teams", is_flag=True, help="Dump all teams' names")
def main(package, team, show_all, list_teams):
    data = requests.get(package_url, timeout=(5, 15)).json()

    def show(rows, title=None):
        click.echo(SingleTable(rows, title).table)

    # Dump just the team names
    if list_teams:
        for tm in sorted(data.keys()):
            click.echo(tm)
        return

    # Find by packages
    if package:
        inv = {pkg: tm for tm, pkgs in data.items() for pkg in pkgs}
        query = package.casefold()
        matches = sorted((pkg, inv[pkg]) for pkg in inv if query in pkg.casefold())

        if not matches:
            click.echo(f'No package matching "{package}"')
        elif len(matches) == 1:
            pkg, tm = matches[0]
            click.echo(f'Package "{pkg}" is owned by "{tm}"')
        else:
            show([["Package", "Team"]] + matches, f'Matches for "{package}"')
        return

    # Find by team
    if team:
        query = team.casefold()
        teams = {tm: pkgs for tm, pkgs in data.items() if query in tm.casefold()}
        # Avoid some messy table outputs if the team provided
        # doesn't exist, or is misspelled
        if not teams:
            click.echo(f'Team name not found: "{team}"')
        elif len(teams) == 1:
            tm, pkgs = next(iter(teams.items()))
            show([["Package"]] + [[p] for p in sorted(pkgs)], f"Packages owned by {tm}")
        else:
            rows = [[tm, "\n".join(sorted(pkgs))] for tm, pkgs in sorted(teams.items())]
            show([["Team", "Packages"]] + rows, f'Teams matching "{team}"')
        return

    # Just show all of it
    if show_all:
        rows = [[tm, "\n".join(sorted(pkgs))] for tm, pkgs in sorted(data.items())]
        show([["Team", "Packages"]] + rows)

if __name__ == "__main__":
    main()