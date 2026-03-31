#!/usr/bin/env python3
import sys

import click
import requests
from rich.console import Console
from rich.table import Table

package_url = "http://reports.qa.ubuntu.com/m-r-package-team-mapping.json"
console     = Console()
err_console = Console(stderr=True)


def fetch_data():
    try:
        response = requests.get(package_url, timeout=(5, 15))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        err_console.print(
            "Error: Could not connect to the server. Check your network connection.",
            style="bold red",
        )
        sys.exit(1)
    except requests.exceptions.Timeout:
        err_console.print("Error: Request timed out.", style="bold red")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        err_console.print(
            f"Error: HTTP {e.response.status_code} from server.", style="bold red"
        )
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        err_console.print(f"Error: {e}", style="bold red")
        sys.exit(1)


COLUMN_STYLES = {
    "Package": "green",
    "Team": "yellow",
    "Packages": "green",
}


def show_table(rows, title=None):
    table = Table(title=title, show_header=True, header_style="bold cyan")
    for col in rows[0]:
        table.add_column(col, style=COLUMN_STYLES.get(col))
    for row in rows[1:]:
        table.add_row(*row)
    console.print(table)


@click.command(no_args_is_help=True)
@click.option(
    "--package",
    "-p",
    multiple=True,
    help="Search the team who owns <package> (repeatable)",
)
@click.option(
    "--team", "-t", multiple=True, help="List all packages owned by <team> (repeatable)"
)
@click.option("--all", "show_all", is_flag=True, help="Show everything")
@click.option("--teams", "list_teams", is_flag=True, help="Dump all teams' names")
def main(package, team, show_all, list_teams):
    active = sum([bool(package), bool(team), show_all, list_teams])
    if active > 1:
        raise click.UsageError(
            "Options --package, --team, --all, and --teams are mutually exclusive."
        )

    data = fetch_data()
    exit_code = 0

    # Dump just the team names
    if list_teams:
        for team_name in sorted(data.keys()):
            console.print(team_name, style="yellow")
        sys.exit(0)

    # Find by package(s), now supports multiples
    if package:
        inv = {pkg: team_name for team_name, pkgs in data.items() for pkg in pkgs}
        for query_str in package:
            query = query_str.casefold()
            matches = sorted((pkg, inv[pkg]) for pkg in inv if query in pkg.casefold())
            if not matches:
                console.print(
                    f'No package matching "[bold]{query_str}[/bold]"', style="yellow"
                )
                exit_code = 1
            elif len(matches) == 1:
                pkg, team_name = matches[0]
                console.print(
                    f'Package "[green]{pkg}[/green]" is owned by "[yellow]{team_name}[/yellow]"'
                )
            else:
                show_table(
                    [["Package", "Team"]] + matches, f'Matches for "{query_str}"'
                )
        sys.exit(exit_code)

    # Find by team(s)
    if team:
        for query_str in team:
            query = query_str.casefold()
            teams = {
                team_name: pkgs
                for team_name, pkgs in data.items()
                if query in team_name.casefold()
            }
            if not teams:
                console.print(
                    f'Team name not found: "[bold]{query_str}[/bold]"', style="yellow"
                )
                exit_code = 1
            elif len(teams) == 1:
                team_name, pkgs = next(iter(teams.items()))
                show_table(
                    [["Package"]] + [[p] for p in sorted(pkgs)],
                    f"Packages owned by {team_name}",
                )
            else:
                rows = [
                    [team_name, "\n".join(sorted(pkgs))]
                    for team_name, pkgs in sorted(teams.items())
                ]
                show_table(
                    [["Team", "Packages"]] + rows, f'Teams matching "{query_str}"'
                )
        sys.exit(exit_code)

    # Show all
    if show_all:
        rows = [
            [team_name, "\n".join(sorted(pkgs))]
            for team_name, pkgs in sorted(data.items())
        ]
        show_table([["Team", "Packages"]] + rows)


if __name__ == "__main__":
    main()
