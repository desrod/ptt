# Ubuntu Package to Team Lookup

Just a quick shell utility I wrote that queries Ubuntu's package/team ownership mapping and can tell you which team owns a package, or which package is owned by a team, so you know who to reach out to when you need support or assistance.

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

- Python 3.x or later
- click
- requests
- terminaltables

Install dependencies, either using your package management tools or just use `pip` in a virtualenv or `uv` runtime: 

``` bash
pip install click requests terminaltables
```

------------------------------------------------------------------------

## Usage

``` bash
$ ./package-to-team.py
Usage: package-to-team.py [OPTIONS]

Options:
  -p, --package TEXT  Search the team who owns <package>
  -t, --team TEXT     List all packages owned by <team>
  --all               Show everything
  --teams             Dump all teams' names
  --help              Show this message and exit.
```

Only one option should be used at a time to avoid confusion. I've added guards in the script to prevent clobbering multiple options being passed at once.

------------------------------------------------------------------------

## Options

### --package, -p

Search for packages whose names contain a substring and show owning team(s)

``` bash
./package-to-team.py --package cloud-init
```

Multiple matches output:

    $ ./package-to-team.py --package cloud-init

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

Search for team names and list their packages

``` bash
./package-to-team.py --team foundations
```

Single match output:

    $ ./package-to-team.py --team foundations

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

    $ ./package-to-team.py --team cloud

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
./package-to-team.py --teams
```

Example output:

    $ ./package-to-team.py --teams
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
./package-to-team.py --all
```

Output:

    $ ./package-to-team.py --all
    
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