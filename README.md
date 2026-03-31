# Ubuntu Package to Team Lookup

A command-line utility I wrote that queries Ubuntu's package/team ownership mapping and can tell you which team owns a package, or which packages a team owns, so you know who to reach out to when you need support or assistance.

#### Questions this answers:

- Who owns this specific package?
- What packages does this team own?
- What are all the packaging teams?

This is meant to be fast, simple, and light on dependencies. No caching, no config files, no magic.

Data source:

http://reports.qa.ubuntu.com/m-r-package-team-mapping.json

------------------------------------------------------------------------

## Why this exists

I regularly need to find out which team owns a package (or vice-versa) when filing bugs or asking questions about issues filed on Launchpad. grep'ing JSON by hand gets old quickly and isn't a good use of the file format. This wraps that dataset in a tiny Python script with readable output.

The goal was to keep this clean, simple, minimal, no configuration or state left behind, and for the code to be immediately readable.

------------------------------------------------------------------------

## Requirements

- Python 3.8 or later
- click
- requests
- rich

Install dependencies, either using your package management tools or just use `pip` in a virtualenv or `uv` runtime:

``` bash
pip install click requests rich
```

Or install the tool directly as a package (provides a `package-to-team` entry point):

``` bash
pip install .
```

------------------------------------------------------------------------

## Usage

``` bash
$ ./package_to_team.py
Usage: package_to_team.py [OPTIONS]

Options:
  -p, --package TEXT  Search the team who owns <package> (repeatable)
  -t, --team TEXT     List all packages owned by <team> (repeatable)
  --all               Show everything
  --teams             Dump all teams' names
  --help              Show this message and exit.
```

Only one option group should be used at a time. The script enforces this and will exit with an error if multiple conflicting options are passed. Both `--package` and `--team` can be repeated to query multiple values in a single call.

The script exits with code `1` if any query produces no results, making it safe to use in shell scripts and pipelines.

------------------------------------------------------------------------

## Options

### --package, -p

Search for packages whose names contain a substring and show owning team(s). Repeat the flag to query multiple packages in one call.

``` bash
./package_to_team.py --package cloud-init
./package_to_team.py --package cloud-init --package snapd
```

Multiple matches output:

    $ ./package_to_team.py --package cloud-init

    ┌Matches for "cloud-init"───────────────┐
    │ Package               │ Team          │
    ├───────────────────────┼───────────────┤
    │ cloud-init            │ ubuntu-server │
    │ cloud-initramfs-tools │ ubuntu-server │
    └───────────────────────┴───────────────┘

No matches:

    No package matching "does-not-exist"

------------------------------------------------------------------------

### --team, -t

Search for team names and list their packages. Repeat the flag to query multiple teams in one call.

``` bash
./package_to_team.py --team foundations
./package_to_team.py --team foundations --team server
```

Single match output:

    $ ./package_to_team.py --team foundations

    ┌Packages owned by foundations-bugs─┐
    │ Package                           │
    ├───────────────────────────────────┤
    │ amd64-microcode                   │
    │ apport                            │
    │ apport-symptoms                   │
    │ apt                               │
    │ apt-clone                         │

    [...]

Multiple matching teams:

    $ ./package_to_team.py --team cloud

    ┌───────────────────────────────┐
    │ Package                       │
    ├───────────────────────────────┤
    │ azure-vm-utils                │
    │ google-compute-engine-oslogin │
    │ google-guest-agent            │
    │ google-osconfig-agent         │
    └───────────────────────────────┘

No matches:

    Team name not found: "foobar"

------------------------------------------------------------------------

### --teams

Dump all team names (one per line)

``` bash
./package_to_team.py --teams
```

Example output:

    $ ./package_to_team.py --teams
    canonical-hw-cert
    canonical-mainstream
    canonical-support
    [...]
    ubuntu-security
    ubuntu-server
    ubuntu-tegra
    unsubscribed

------------------------------------------------------------------------

### --all

Show the entire mapping

``` bash
./package_to_team.py --all
```

Output:

    $ ./package_to_team.py --all
    
    ┌────────────────────────┬─────────────────────────────────────────────────┐
    │ Team                   │ Packages                                        │
    ├────────────────────────┼─────────────────────────────────────────────────┤

    [...]

    │ pkg-ime                │ gyp                                             │
    │                        │ libpinyin                                       │
    │                        │ mozc                                            │
    │                        │ ninja-build                                     │
    │                        │ tegaki-zinnia-japanese                          │
    │                        │ zinnia                                          │
    │ snappy-dev             │ golang-check.v1                                 │
    │                        │ golang-github-coreos-go-systemd                 │
    │                        │ golang-github-gosexy-gettext                    │
    │                        │ golang-github-mvo5-goconfigparser               │
    │                        │ golang-github-mvo5-uboot-go                     │
    │                        │ golang-github-peterh-liner                      │
    │                        │ golang-go-flags                                 │
    │                        │ golang-pb                                       │
    │                        │ golang-pty                                      │
    │                        │ golang-websocket                                │
    │                        │ initramfs-tools-ubuntu-core                     │
    │                        │ snapd                                           │
    │                        │ ubuntu-core-config                              │
    │                        │ ubuntu-core-launcher                            │
    │                        │ xdelta3                                         │
    [...]


## Contributing

If you want a feature, just ask! PRs are always welcome and encouraged.

------------------------------------------------------------------------

## License

GPL v3.0